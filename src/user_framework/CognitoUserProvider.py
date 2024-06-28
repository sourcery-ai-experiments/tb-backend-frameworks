import boto3
from user_framework.Interface import UserInterface


class CognitoUserProvider(UserInterface):
    def __init__(self, user_pool_id: str, client_id: str, region_name: str) -> None:
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self. client = boto3.client("cognito-idp", region_name=region_name)
        
    def create_user(self, email) -> None:
        pass
    
    def read_user(self, email: str) -> None:
        pass
    
    def delete_user(self, user_id) -> None:
        pass
    
    def resend_temp_password(self, email) -> None:
        pass
    
    def disable_user(self, user_id) -> None:
        pass