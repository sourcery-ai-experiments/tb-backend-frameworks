import boto3
import logging
from user_framework.Interface import UserInterface
from decorators import catch_exceptions


class CognitoUserProvider(UserInterface):
    def __init__(self, user_pool_id: str, client_id: str, region_name: str, logger: logging.Logger) -> None:
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.client = boto3.client("cognito-idp", region_name=region_name)
        self.logger = logger
    
    @catch_exceptions
    def create_user(self, email: str) -> None:
        self.client.admin_create_user(UserPoolId=self.user_pool_id, 
                                      Username=email,
                                      UserAttributes=[
                                          {"Name": "email", "Value": email},
                                          {"Name": "email_verified", "Value": "true"}])
    
    @catch_exceptions
    def read_user(self, email: str) -> None:
        return self.client.admin_get_user(UserPoolId=self.user_pool_id, Username=email)
    
    @catch_exceptions
    def delete_user(self, email: str) -> None:
        self.client.admin_delete_user(UserPoolId=self.user_pool_id, Username=email)
    
    @catch_exceptions
    def resend_temp_password(self, email: str) -> None:
        self.client.admin_create_user(UserPoolId=self.user_pool_id, 
                                      Username=email, 
                                      UserAttributes=[
                                          {"Name": "email", "Value": email},
                                          {"Name": "email_verified", "Value": "true"}],
                                      MessageAction="RESEND")
    
    @catch_exceptions
    def disable_user(self, user_id: str) -> None:
        pass