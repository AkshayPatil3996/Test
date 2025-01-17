import threading


thread_local = threading.local()

class TenantDatabaseRouter:
    def db_for_read(self, model, **hints):
     
        tenant_db = getattr(thread_local, 'tenant_db', None)
        if tenant_db:
            return tenant_db 
        return 'default'  

    def db_for_write(self, model, **hints):
       
        tenant_db = getattr(thread_local, 'tenant_db', None)
        if tenant_db:
            return tenant_db  
        return 'default'  

    def allow_relation(self, obj1, obj2, **hints):
  
        tenant_db = getattr(thread_local, 'tenant_db', None)
        if tenant_db:
            if obj1._state.db == tenant_db and obj2._state.db == tenant_db:
                return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        
        tenant_db = getattr(thread_local, 'tenant_db', None)
        if db == tenant_db:
            return True 
        if db == 'default': 
            return app_label == 'admin'  
        return False  


# class AdminSchemaRouter:
#     def db_for_read(self, model, **hints):
#         # Define database for read operations
#         if model._meta.app_label in ['auth', 'sessions', 'admin', 'contenttypes', 'messages']:
#             return 'default'
#         elif model._meta.app_label == 'admin_management':
#             return 'admin_management'
#         elif model._meta.app_label == 'master':
#             return 'master'
#         elif model._meta.app_label == 'opulatenant':
#             return model.tenant_db_name  # Assuming tenant_db_name is a valid database name for the model
#         return 'default'

#     def db_for_write(self, model, **hints):
#         # Define database for write operations
#         if model._meta.app_label in ['auth', 'sessions', 'admin', 'contenttypes', 'messages']:
#             return 'default'
#         elif model._meta.app_label == 'admin_management':
#             return 'admin_management'
#         elif model._meta.app_label == 'master':
#             return 'master'
#         elif model._meta.app_label == 'opulatenant':
#             return model.tenant_db_name  # Assuming tenant_db_name is a valid database name for the model
#         return 'default'

#     def allow_relation(self, obj1, obj2, **hints):
#         # Allow relations between models within the same app or contenttypes app
#         if obj1._meta.app_label == obj2._meta.app_label:
#             return True
#         if 'contenttypes' in [obj1._meta.app_label, obj2._meta.app_label]:
#             return True
#         return False

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         # This method ensures migrations are applied to the correct schema
#         if app_label in ['auth', 'sessions', 'admin', 'contenttypes', 'messages']:
#             return db == 'default'  # These apps should only migrate on the 'default' database
#         elif app_label == 'admin_management':
#             return db == 'admin_management'  # Models in 'admin_management' should migrate on 'admin_management'
#         elif app_label == 'master':
#             return db == 'master'  # Models in 'master' should migrate on 'master'
#         elif app_label == 'opulatenant':
#             # Allow migrations for 'tenantprofilemanagement' and 'tenantemployeemanagement' in 'admin_management'
#             if db == 'admin_management':
#                 return model_name in ['tenantprofilemanagement', 'tenantemployeemanagement']
#             # Ensure other models for 'opulatenant' go to the correct database
#             return db != 'admin_management'
#         return db == 'admin_management'  # Default behavior for models not matching any app




class AdminSchemaRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['auth', 'sessions', 'admin', 'contenttypes', 'messages']:
            return 'default'
        elif model._meta.app_label == 'admin_management':
            return 'admin_management'
        elif model._meta.app_label == 'master':
            return 'master'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['auth', 'sessions', 'admin', 'contenttypes', 'messages']:
            return 'default'
        elif model._meta.app_label == 'admin_management':
            return 'admin_management'
        elif model._meta.app_label == 'master':
            return 'master'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        if 'contenttypes' in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['auth', 'sessions', 'admin', 'contenttypes', 'messages']:
            return db == 'default'
        elif app_label == 'admin_management':
            return db == 'admin_management'
        elif app_label == 'master':
            return db == 'master'
        elif app_label == 'opulatenant':
            db == 'admin_management'
        return db == 'default'
    

class TenantSchemaRouter:
    def db_for_read(self, model, **hints):
       
        if hasattr(thread_local, 'db_config'):
            tenant_db_config = thread_local.db_config
            if tenant_db_config:
                return tenant_db_config['NAME']  

  
        if model._meta.app_label == 'opulatenant':
            return 'default'
        elif model._meta.app_label == 'employee_management':
            return 'employee_management'
        elif model._meta.app_label == 'management':
            return 'management'
        return 'default'

    def db_for_write(self, model, **hints):
       
        if hasattr(thread_local, 'db_config'):
            tenant_db_config = thread_local.db_config
            if tenant_db_config:
                return tenant_db_config['NAME'] 


        if model._meta.app_label == 'opulatenant':
            return 'default'
        elif model._meta.app_label == 'employee_management':
            return 'employee_management'
        elif model._meta.app_label == 'management':
            return 'management'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
       
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        if 'contenttypes' in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
       
        if hasattr(thread_local, 'db_config'):
            tenant_db_config = thread_local.db_config
            if tenant_db_config:
                if db == tenant_db_config['NAME']:
                    return True

        if app_label in ['opulatenant']:
            return db == 'default'
        elif app_label == 'employee_management':
            return db == 'employee_management'
        elif app_label == 'management':
            return db == 'management'
        
        return db == 'default'




# class TenantSchemaRouter:
#     """
#     Database router for routing models to tenant-specific databases based on tm_db_name.
#     """
#     def db_for_read(self, model, **hints):
#         """
#         Routes database queries for tenant models to their specific database.
#         """
#         # If the model belongs to the tenant, use tenant database name dynamically
#         if hasattr(model, 'tenant_db_name') and model.tenant_db_name:
#             tenant_db_name = model.tenant_db_name
#             return tenant_db_name  # Dynamically route to tenant database
#         return 'default'  # Default database for other models

#     def db_for_write(self, model, **hints):
#         """
#         Routes write operations for tenant models to their specific database.
#         """
#         if hasattr(model, 'tenant_db_name') and model.tenant_db_name:
#             tenant_db_name = model.tenant_db_name
#             return tenant_db_name  # Dynamically route to tenant database
#         return 'default'  # Default database for other models

#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if both objects belong to the same database or certain apps.
#         """
#         # Allow relations only if both models belong to the same tenant or shared models
#         if hasattr(obj1, 'tenant_db_name') and hasattr(obj2, 'tenant_db_name'):
#             if obj1.tenant_db_name == obj2.tenant_db_name:
#                 return True
#         return False

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Routes migrations for models to the correct tenant database.
#         """
#         # If the model is part of a tenant and the database matches, allow migration
#         if app_label == 'opulatenant':
#             tenant_db_name = hints.get('instance', None)  # Get the tenant instance
#             if tenant_db_name:
#                 return db == tenant_db_name  # Ensure migration happens in the correct database
#         return db == 'default'  # Default database for other models













