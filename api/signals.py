import psycopg2
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError
import logging
from django.core.management import call_command
from django.db import connections
from opulaadmin.models import *
from api.models import *
import re
import psycopg2
from psycopg2 import sql
from django.db import transaction
from cryptography.fernet import Fernet
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)

FERNET_KEY = 'StLUwP5ur5ZnP7rSGL85zpq7uPn0mbY5yi93hYAzi1w='



@receiver(post_save, sender=TenantModel)
def create_tenant_database(sender, instance, created, **kwargs):
    if created:
        tm_db_name = instance.tm_db_name
        tm_db_user = instance.tm_db_user
        tm_db_password = instance.tm_db_password  
        tm_domain_name = instance.tm_domain_name

        fernet = Fernet(settings.FERNET_KEY)
        decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        conn.autocommit = True
        cursor = conn.cursor()

        try:
            cursor.execute("SET search_path TO admin_management;")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(tm_db_name)))
            print(f"Database {tm_db_name} created successfully.")

            cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(tm_db_user)), [decrypted_password])
            print(f"User {tm_db_user} created successfully.")

            cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                sql.Identifier(tm_db_name), sql.Identifier(tm_db_user)
            ))
            print(f"Granted all privileges to {tm_db_user}.")

            cursor.execute(sql.SQL("ALTER DATABASE {} OWNER TO {}").format(
                sql.Identifier(tm_db_name), sql.Identifier(tm_db_user)
            ))
            print(f"{tm_db_user} is now the owner of database {tm_db_name}.")

            cursor.execute(sql.SQL("ALTER USER {} WITH SUPERUSER").format(sql.Identifier(tm_db_user)))
            print(f"User {tm_db_user} is now a superuser.")

            tenant_conn = psycopg2.connect(
                dbname=tm_db_name,
                user=tm_db_user,
                password=decrypted_password,
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT']
            )
            tenant_conn.autocommit = True
            tenant_cursor = tenant_conn.cursor()

            tenant_cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS management"))
            tenant_cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS employee_management"))
            print("Schemas 'management' and 'employee_management' created successfully.")

            tenant_cursor.execute(sql.SQL("ALTER SCHEMA management OWNER TO {}").format(sql.Identifier(tm_db_user)))
            tenant_cursor.execute(sql.SQL("ALTER SCHEMA employee_management OWNER TO {}").format(sql.Identifier(tm_db_user)))
            print(f"User {tm_db_user} is now the owner of schemas.")

            tenant_cursor.execute(sql.SQL("GRANT USAGE ON SCHEMA management TO {}").format(sql.Identifier(tm_db_user)))
            tenant_cursor.execute(sql.SQL("GRANT USAGE ON SCHEMA employee_management TO {}").format(sql.Identifier(tm_db_user)))
            tenant_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA management TO {}").format(sql.Identifier(tm_db_user)))
            tenant_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA management TO {}").format(sql.Identifier(tm_db_user)))
            tenant_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA employee_management TO {}").format(sql.Identifier(tm_db_user)))
            tenant_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA employee_management TO {}").format(sql.Identifier(tm_db_user)))

            print(f"Granted permissions on schemas 'management' and 'employee_management' to {tm_db_user}.")

            domain_name = f"{tm_domain_name}.{settings.OPULA_DOMAIN}"
            tenant_cursor.execute(sql.SQL("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = %s) THEN
                        CREATE DOMAIN {} AS TEXT;
                    END IF;
                END
                $$;
            """).format(sql.Identifier(domain_name)), [domain_name])
            print(f"Domain {domain_name} created successfully.")


           
            tenant_cursor.execute(sql.SQL("""
        ALTER TABLE management.some_table
        ALTER COLUMN some_column TYPE {} USING some_column::TEXT;
    """).format(sql.Identifier(domain_name)))

            tenant_cursor.execute(sql.SQL("""
        ALTER TABLE employee_management.some_table
        ALTER COLUMN some_column TYPE {} USING some_column::TEXT;
    """).format(sql.Identifier(domain_name)))
            # tenant_cursor.execute(sql.SQL("ALTER SCHEMA management SET DOMAIN TO {}").format(sql.Identifier(domain_name)))
            # tenant_cursor.execute(sql.SQL("ALTER SCHEMA employee_management SET DOMAIN TO {}").format(sql.Identifier(domain_name)))
            print(f"Assigned domain {domain_name} to schemas 'management' and 'employee_management'.")

            print(f"Running migrations for the 'opulatenant' app in database {tm_db_name}...")
            call_command('migrate', database=tm_db_name, app_label='opulatenant')

            print("Migrations for 'opulatenant' completed successfully.")

            tenant_cursor.close()
            tenant_conn.close()

        except Exception as e:
            print(f"Error creating tenant database or setting up schemas: {e}")
        finally:
            # Cleanup connections
            cursor.close()
            conn.close()




# @receiver(post_save, sender=TenantModel)
# def create_tenant_database(sender, instance, created, **kwargs):
#     if created:
#         tm_db_name = instance.tm_db_name
#         tm_db_user = instance.tm_db_user
#         tm_db_password = instance.tm_db_password  

#         # Decrypt the password
#         fernet = Fernet(settings.FERNET_KEY)
#         decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#         # Connect to the default database (Django's default DB)
#         conn = psycopg2.connect(
#             dbname=settings.DATABASES['default']['NAME'],
#             user=settings.DATABASES['default']['USER'],
#             password=settings.DATABASES['default']['PASSWORD'],
#             host=settings.DATABASES['default']['HOST'],
#             port=settings.DATABASES['default']['PORT']
#         )
#         conn.autocommit = True
#         cursor = conn.cursor()

#         try:
#             # 1. Create the tenant database
#             cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(tm_db_name)))
#             print(f"Database {tm_db_name} created successfully.")

#             # 2. Create the user for the tenant
#             cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(tm_db_user)), [decrypted_password])
#             print(f"User {tm_db_user} created successfully.")

#             # 3. Grant privileges to the user
#             cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
#                 sql.Identifier(tm_db_name), sql.Identifier(tm_db_user)
#             ))
#             print(f"Granted all privileges to {tm_db_user}.")

#             # 4. Make the user the owner of the tenant database
#             cursor.execute(sql.SQL("ALTER DATABASE {} OWNER TO {}").format(
#                 sql.Identifier(tm_db_name), sql.Identifier(tm_db_user)
#             ))
#             print(f"{tm_db_user} is now the owner of database {tm_db_name}.")

#             # 5. Make the user a superuser (so they can manage schemas and tables)
#             cursor.execute(sql.SQL("ALTER USER {} WITH SUPERUSER").format(sql.Identifier(tm_db_user)))
#             print(f"User {tm_db_user} is now a superuser.")

#             # 6. Connect to the newly created tenant database
#             tenant_conn = psycopg2.connect(
#                 dbname=tm_db_name,
#                 user=tm_db_user,
#                 password=decrypted_password,
#                 host=settings.DATABASES['default']['HOST'],
#                 port=settings.DATABASES['default']['PORT']
#             )
#             tenant_conn.autocommit = True
#             tenant_cursor = tenant_conn.cursor()

#             # 7. Create the required schemas
#             tenant_cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS management"))
#             tenant_cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS employee_management"))
#             print("Schemas 'management' and 'employee_management' created successfully.")

#             # 8. Assign ownership of the schemas to the tenant user
#             tenant_cursor.execute(sql.SQL("ALTER SCHEMA management OWNER TO {}").format(sql.Identifier(tm_db_user)))
#             tenant_cursor.execute(sql.SQL("ALTER SCHEMA employee_management OWNER TO {}").format(sql.Identifier(tm_db_user)))
#             print(f"User {tm_db_user} is now the owner of schemas.")

#             # 9. Grant permissions on schemas to the tenant user
#             tenant_cursor.execute(sql.SQL("GRANT USAGE ON SCHEMA management TO {}").format(sql.Identifier(tm_db_user)))
#             tenant_cursor.execute(sql.SQL("GRANT USAGE ON SCHEMA employee_management TO {}").format(sql.Identifier(tm_db_user)))
#             tenant_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA management TO {}").format(sql.Identifier(tm_db_user)))
#             tenant_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA management TO {}").format(sql.Identifier(tm_db_user)))
#             tenant_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA employee_management TO {}").format(sql.Identifier(tm_db_user)))
#             tenant_cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA employee_management TO {}").format(sql.Identifier(tm_db_user)))

#             print(f"Granted permissions on schemas 'management' and 'employee_management' to {tm_db_user}.")

#             # 10. Run migrations for the 'opulatenant' app
#             print(f"Running migrations for the 'opulatenant' app in database {tm_db_name}...")
#             call_command('migrate', database=tm_db_name, app_label='opulatenant')

#             print("Migrations for 'opulatenant' completed successfully.")

#             # Close the tenant connection
#             tenant_cursor.close()
#             tenant_conn.close()

#         except Exception as e:
#             print(f"Error creating tenant database or setting up schemas: {e}")
#         finally:
#             # Cleanup connections
#             cursor.close()
#             conn.close()

            

        
# @receiver(post_save, sender=TenantModel)
# def create_tenant_database(sender, instance, created, **kwargs):
#     if created:
#         tm_db_name = instance.tm_db_name
#         tm_db_user = instance.tm_db_user
#         tm_db_password = instance.tm_db_password  

     
#         fernet = Fernet(settings.FERNET_KEY)
#         decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#         conn = psycopg2.connect(
#             dbname=settings.DATABASES['default']['NAME'],
#             user=settings.DATABASES['default']['USER'],
#             password=settings.DATABASES['default']['PASSWORD'],
#             host=settings.DATABASES['default']['HOST'],
#             port=settings.DATABASES['default']['PORT']
#         )
#         conn.autocommit = True
#         cursor = conn.cursor()

#         try:      
#             cursor.execute(f"CREATE DATABASE {tm_db_name};")
#             print(f"Database {tm_db_name} created successfully.")

#             cursor.execute(f"CREATE USER {tm_db_user} WITH PASSWORD '{decrypted_password}';")
#             print(f"User {tm_db_user} created successfully.")

#             cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {tm_db_name} TO {tm_db_user};")

#             cursor.execute(f"GRANT USAGE ON SCHEMA public TO {tm_db_user};")
#             cursor.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {tm_db_user};")
#             cursor.execute(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {tm_db_user};")

#             print(f"User {tm_db_user} has full access to {tm_db_name} database.")

#         except Exception as e:
#             print(f"Error creating tenant database: {e}")
#         finally:
#             cursor.close()
#             conn.close()





