from cryptography.fernet import Fernet
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError




KEY = b'StLUwP5ur5ZnP7rSGL85zpq7uPn0mbY5yi93hYAzi1w='  
fernet = Fernet(KEY)

def encrypt_password(password: str) -> str:
  
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password.decode()  

def decrypt_password(encrypted_password: str) -> str:
  
    decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
    return decrypted_password


def get_tokens_for_user(user):
   
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }






