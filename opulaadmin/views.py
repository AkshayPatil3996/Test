import time
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import connection,connections, DatabaseError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def admin_registration_view(request):
    if request.method == 'POST':
        form = AuthenticationModelForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            am_mobile_no = form.cleaned_data.get('am_mobile_no')
            confirm_password = form.cleaned_data.get('confirm_password')

    
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('admin_register')  

            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
                return redirect('admin_register')  

            user = form.save(commit=False)

            try:
                admin_role = RoleManagementModel.objects.get(id=1)
                user.am_role = admin_role
            except RoleManagementModel.DoesNotExist:
                messages.error(request, "Admin role not found. Please contact an administrator.")
                return redirect('admin_register')

            user.set_password(password)
            
            user.is_superuser = True
            user.is_staff = True

            user.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('admin_register') 

    else:
        form = AuthenticationModelForm() 

    return render(request, 'auth/register.html', {'form': form})



def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)

        if form.is_valid():
            with connections['default'].cursor() as cursor:
                cursor.execute("SET search_path TO admin_management, public, master;")

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # print("email------", email)
            # print('password----', password)

            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_staff and user.is_superuser:
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect('dashboard') 
                else:
                    messages.error(request, "You are not an admin. Access denied.")
                    return redirect('admin_login')  
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                return redirect('admin_login') 
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect('admin_login') 

    else:
        form = AdminLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})



def tenant_registration(request):
    if request.method == 'POST':
        user_form = AuthenticationModelForm(request.POST)
        tenant_form = TenantModelForm(request.POST)

        if user_form.is_valid() and tenant_form.is_valid():
            user_data = user_form.cleaned_data
            tenant_data = tenant_form.cleaned_data

            user = create_authentication_model(user_data)

            tenant_data.update({
                'tm_auth': user,
                'tm_db_name': f"{user.first_name.lower()}_{str(uuid.uuid4()).replace('-', '')}",
                'tm_db_user': generate_tm_db_user(user),
                'tm_db_password': encrypt_password(user_data['password']),
                'tm_domain_name': tenant_form.cleaned_data.get('tm_domain_name', ''),
            })

            tenant = create_tenant_model(user, tenant_data)

            if tenant:
                messages.success(request, 'User and Tenant created successfully!')
                return redirect('login')  
            else:
                messages.error(request, 'Failed to create tenant.')
        else:
            messages.error(request, 'There was an error with your form submission.')

    else:
        user_form = AuthenticationModelForm()
        tenant_form = TenantModelForm()

    return render(request, 'auth/register.html', {
        'user_form': user_form,
        'tenant_form': tenant_form
    })

# Login view

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SET search_path TO admin_management, public, master;")

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                session_key = request.session.session_key
                if not session_key:
                    request.session.create()  
                print(f"Session key after login: {session_key}")

                response = redirect('dashboard')
                response.set_cookie(
                    settings.SESSION_COOKIE_NAME, 
                    session_key, 
                    max_age=settings.SESSION_COOKIE_AGE, 
                    expires=settings.SESSION_COOKIE_AGE + int(time.time()),  
                    domain=settings.SESSION_COOKIE_DOMAIN  
                )

                if request.user.is_authenticated:
                    try:
                        tenant = TenantModel.objects.using('default').get(tm_auth=user)
                        print(f"Tenant found: {tenant.tm_domain_name}")

                        if tenant.tm_domain_name:
                            tenant_prefix = tenant.tm_domain_name
                            tenant_url = f"http://{tenant_prefix}.{settings.OPULA_DOMAIN}/dashboard"  # Assuming subdomain structure
                            return redirect(tenant_url)

                    except TenantModel.DoesNotExist:
                        print("Tenant model not found for the provided user.")
                        messages.error(request, 'Tenant information not found.')
                        return redirect('login')

                else:
                    messages.error(request, 'Authentication failed. Please try again.')
                    return redirect('login')

            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')

        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'There was an error processing your request. Please try again later.')
            return redirect('login')

    return render(request, 'auth/login.html')



# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             # Step 1: Connect to the default database and set search_path to include both schemas
#             with connections['default'].cursor() as cursor:
#                 cursor.execute("SET search_path TO admin_management, public;")  # Add 'public' schema along with 'admin_management'

#             # Step 2: Authenticate the user with the provided credentials
#             user = authenticate(request, username=email, password=password)

#             if user is not None:
#                 # Log the user in
#                 login(request, user)

#                 # Step 3: Check if the user is authenticated
#                 if request.user.is_authenticated:
#                     try:
#                         # Step 4: Attempt to find the tenant associated with the authenticated user
#                         tenant = TenantModel.objects.using('default').get(tm_auth=user)
#                         print(f"Tenant found: {tenant.tm_domain_name}")

#                         # Step 5: Redirect the user to the tenant's dashboard
#                         if tenant.tm_domain_name:
#                             tenant_prefix = tenant.tm_domain_name
#                             tenant_url = f"http://{tenant_prefix}.{settings.OPULA_DOMAIN}/dashboard"  # Assuming subdomain structure
#                             return redirect(tenant_url)

#                     except TenantModel.DoesNotExist:
#                         # Handle case where tenant model does not exist for the authenticated user
#                         print("Tenant model not found for the provided user.")
#                         messages.error(request, 'Tenant information not found.')
#                         return redirect('login')

#                 else:
#                     # If the user is not authenticated after login (shouldn't happen)
#                     messages.error(request, 'Authentication failed. Please try again.')
#                     return redirect('login')

#             else:
#                 # If authentication fails, show error message
#                 messages.error(request, 'Invalid email or password.')
#                 return redirect('login')

#         except Exception as e:
#             # Handle any exceptions related to the database connection or other issues
#             print(f"Error: {e}")
#             messages.error(request, 'There was an error processing your request. Please try again later.')
#             return redirect('login')

#     # If the request method is not POST, render the login page
#     return render(request, 'test/login.html')




# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print('hello----')

#         user = authenticate(request, username=email, password=password)
#         print('hello----1')
        
#         if user is not None:
#             login(request, user)
#             print('hello----2')

#             try:
               
#                 get_user = AuthenticationModel.objects.get(email=email)
#                 get_tenant = TenantModel.objects.get(tm_auth__email=email)

             
#                 db_name = get_tenant.tm_db_name
#                 db_user = get_tenant.tm_db_user
#                 db_password = get_tenant.tm_db_password

             
#                 if db_name and db_user and db_password:
#                     if 'default' in connections:
#                         connections['default'].close()
#                     connections.databases['default'] = {
#                         'ENGINE': 'django.db.backends.postgresql',  
#                         'NAME': db_name,
#                         'USER': db_user,
#                         'PASSWORD': db_password,
#                         'HOST': '127.0.0.1',  
#                         'PORT': '5432',  
#                     }

#                     try:
#                         with connections['default'].cursor() as cursor:
#                             cursor.execute("SELECT 1")
#                             cursor.fetchone()  
#                         print("Connection to tenant's database successful.")
#                     except DatabaseError as e:
#                         print(f"Error connecting to tenant's database: {e}")
#                         messages.error(request, 'Could not connect to the tenant\'s database. Please try again later.')
#                         return redirect('login')  
#                 else:
#                     print("Tenant DB settings not found, falling back to default database connection.")

#             except TenantModel.DoesNotExist:
#                 print("Tenant model not found for the provided email.")
#                 messages.error(request, 'Tenant information not found.')
#                 return redirect('login')

#             if get_tenant.tm_domain_name:
#                 tenant_prefix = get_tenant.tm_domain_name  
#                 base_domain = "localhost:8000"  
#                 tenant_url = f"http://{tenant_prefix}.{base_domain}/"  
                
#                 return redirect(tenant_url)

#             messages.success(request, 'You have logged in successfully!')
#             return redirect('home')

#         else:
#             messages.error(request, 'Invalid email or password.')
#             return redirect('login')

#     return render(request, 'test/login.html')



# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'You have logged out successfully!')
    return redirect('login') 


def create_authentication_model(user_data):
    static_role = RoleManagementModel.objects.get(id=2)  
    user = AuthenticationModel(
        email=user_data['email'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        password=user_data['password'],
        am_mobile_no=user_data['am_mobile_no'],
        am_role=static_role
    )
    user.set_password(user_data['password'])  
    user.save()
    return user

def generate_tm_db_user(user):
    email_prefix = user.email.split('@')[0]
    domain_name = user.email.split('@')[1].split('.')[0]
    return f"{email_prefix}{domain_name}"

def encrypt_password(password):
    fernet = Fernet(settings.FERNET_KEY)
    return fernet.encrypt(password.encode()).decode()

def create_tenant_model(user, tenant_data):
    tenant = TenantModel(**tenant_data)
    tenant.save()
    return tenant




def home(request):
    return render(request, 'auth/login.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')



def tenant_list_and_update_view(request):
    role_obj = RoleManagementModel.objects.get(id=2)
    tenants = AuthenticationModel.objects.filter(am_role=role_obj)
    tenant_domains = TenantModel.objects.filter(tm_auth__in=tenants)

    if request.method == 'POST':
        tenant_id = request.POST.get('tenant_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_no = request.POST.get('mobile_no')
        email = request.POST.get('email')  

        try:
            tenant = AuthenticationModel.objects.get(id=tenant_id)
            if first_name:
                tenant.first_name = first_name
            if last_name:
                tenant.last_name = last_name
            if mobile_no:
                tenant.am_mobile_no = mobile_no
            if email:
                tenant.email = email  
            tenant.save()

            response_data = {
                'success': True,
                'message': 'Tenant information updated successfully!',
            }
            return JsonResponse(response_data)

        except AuthenticationModel.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Tenant not found!'}, status=404)

    tenant_data = tenants.values('id', 'email', 'first_name', 'last_name', 'am_mobile_no', 'am_role', 'am_is_deleted', 'am_created_at', 'am_updated_at')

    tenant_datas = []
    for tenant in tenant_data:
      
        tenant_domain = tenant_domains.filter(tm_auth=tenant['id']).first()

        context = {
            "tenant_data": tenant,
            "domains": tenant_domain
        }
        tenant_datas.append(context)

    paginator = Paginator(tenant_datas, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'tenantmanagement/tenantList.html', {'tenant_data_list': page_obj})


def tenant_profile_view(request, pk):
    get_tenant = get_object_or_404(AuthenticationModel, id=pk)

    tenant_obj = TenantModel.objects.get(tm_auth=get_tenant.id)
 
    all_data = {
        "auth_obj": get_tenant,
        "tenant_obj": tenant_obj
    }
    
    return render(request, 'tenantmanagement/tenantProfile.html', {"data": all_data})

def tenant_employee_list_view(request):
    return render(request, 'tenantemployeemanagement/tenantEmployeeList.html')

def tenant_employee_profile_view(request):
    return render(request, 'tenantemployeemanagement/tenantEmployeeProfile.html')

def admin_tenant_manage_view(request, pk):
    get_tenant = get_object_or_404(AuthenticationModel, id=pk)
    print("Sdf",get_tenant)
    return render(request, 'tenantmanagement/tenantManage.html', {"data": get_tenant})


def staff_list_view(request):
    role_obj = RoleManagementModel.objects.get(id=1)
    
    staffs = AuthenticationModel.objects.filter(am_role=role_obj, is_staff=True, is_superuser=True, am_is_deleted=False)
    
 
    staff_data = staffs.values(
        'id', 'email', 'first_name', 'last_name', 'am_mobile_no', 'am_role', 'am_is_deleted', 'am_created_at', 'am_updated_at'
    )

 
    staff_datas = []
    for staff in staff_data:
        context = {
            "staff_data": staff,
        }
        staff_datas.append(context)


    paginator = Paginator(staff_datas, 10)  
    page_number = request.GET.get('page', 1)

    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'staffmanagement/staffList.html', {'staff_data_list': page_obj})


def privacy_policy_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            form = PrivacyPolicyForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success'})

        elif action == 'update':
            privacy_id = request.POST.get('id')
            title = request.POST.get('ppm_title')
            content = request.POST.get('ppm_content')
            privacy = PrivacyPolicyModel.objects.get(id=privacy_id)
            privacy.ppm_title = title
            privacy.ppm_content = content
            privacy.save()
            return JsonResponse({'status': 'success'})

        elif action == 'delete':
            term_id = request.POST.get('id')
            try:
                term = PrivacyPolicyModel.objects.get(id=term_id)
                term.delete()  
                return JsonResponse({'status': 'success'})
            except PrivacyPolicyModel.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Policy not found'})

    privacy = PrivacyPolicyModel.objects.all()
    form = PrivacyPolicyForm()
    return render(request, 'privacypolicy.html', {'form': form, 'privacy': privacy})


def terms_and_conditions_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            form = TermsAndConditionForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success'})

        elif action == 'update':
            term_id = request.POST.get('id')
            title = request.POST.get('tacm_title')
            content = request.POST.get('tacm_content')
            term = TermsAndConditionmodel.objects.get(id=term_id)
            term.tacm_title = title
            term.tacm_content = content
            term.save()
            return JsonResponse({'status': 'success'})

        elif action == 'delete':
            term_id = request.POST.get('id')
            term = TermsAndConditionmodel.objects.get(id=term_id)
            term.delete()
            return JsonResponse({'status': 'success'})

    terms = TermsAndConditionmodel.objects.all()
    form = TermsAndConditionForm()
    return render(request, 'termsandcondition.html', {'form': form, 'terms': terms})



def miscellaneous_view(request):

    job_skill_form = JobSkillForm()
    industry_form = IndustryForm()

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'add_job_skill':
            job_skill_form = JobSkillForm(request.POST) 
            if job_skill_form.is_valid():
                job_skill_form.save()
                return JsonResponse({'status': 'success', 'message': 'Job Skill added successfully!'})

        elif action == 'add_industry':
            industry_form = IndustryForm(request.POST)  
            if industry_form.is_valid():
                industry_form.save()
                return JsonResponse({'status': 'success', 'message': 'Industry added successfully!'})

        elif action == 'update_job_skill':
            job_skill_id = request.POST.get('id')
            skill_name = request.POST.get('jsm_skill')
            job_skill = JobSkillModel.objects.get(id=job_skill_id)
            job_skill.jsm_skill = skill_name
            job_skill.save()
            return JsonResponse({'status': 'success', 'message': 'Job Skill updated successfully!'})

        elif action == 'update_industry':
            industry_id = request.POST.get('id')
            industry_name = request.POST.get('industry_name')
            industry = IndustryMasterModel.objects.get(id=industry_id)
            industry.im_industry = industry_name
            industry.save()
            return JsonResponse({'status': 'success', 'message': 'Industry updated successfully!'})

        elif action == 'delete_job_skill':
            job_skill_id = request.POST.get('id')
            job_skill = JobSkillModel.objects.get(id=job_skill_id)
            job_skill.delete()
            return JsonResponse({'status': 'success', 'message': 'Job Skill deleted successfully!'})

        elif action == 'delete_industry':
            industry_id = request.POST.get('id')
            industry = IndustryMasterModel.objects.get(id=industry_id)
            industry.delete()
            return JsonResponse({'status': 'success', 'message': 'Industry deleted successfully!'})

    job_skills = JobSkillModel.objects.all()
    industries = IndustryMasterModel.objects.all()

    return render(request, 'miscellaneous.html', {
        'job_skill_form': job_skill_form,
        'industry_form': industry_form,
        'job_skills': job_skills,
        'industries': industries
    })



def hiring_create_view(request):
    if request.method == 'POST':
        pass
    return render(request, 'hiring/createHiring.html')

def hiring_job_list_view(request):
    return render (request, 'hiring/jobList.html')




