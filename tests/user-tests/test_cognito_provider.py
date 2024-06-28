from unittest.mock import patch
from user_framework.Interface import UserInterface

def test_cognito_user_provider_conformance(identity_provider: UserInterface) -> None:
    assert isinstance(identity_provider, UserInterface)

def test_create_user(identity_provider: UserInterface) -> None:
    with patch.object(identity_provider.client, 'admin_create_user') as mock_create_user:
        identity_provider.create_user("test3@example.com")
        mock_create_user.assert_called_once_with(
            UserPoolId=identity_provider.user_pool_id,
            Username="test3@example.com",
            UserAttributes=[
                {'Name': 'email', 'Value': "test3@example.com"},
                {'Name': 'email_verified', 'Value': "true"}
            ]
        )   

def test_read_user(identity_provider: UserInterface) -> None:
    with patch.object(identity_provider.client, 'admin_get_user', return_value={'Username': "test1@example.com"}) as mock_get_user:
        user = identity_provider.read_user("test1@example.com")
        mock_get_user.assert_called_once_with(
            UserPoolId=identity_provider.user_pool_id,
            Username="test1@example.com"
        )
        username = user["Username"]
        assert username == "test1@test.com"

def test_resend_temp_password(identity_provider: UserInterface) -> None:
    with patch.object(identity_provider.client, 'admin_create_user') as mock_resend_password:
        old_user_attrs = identity_provider.read_user("test1@example.com")["UserAttributes"]
        identity_provider.resend_temp_password("test1@example.com")
        new_user_attrs = identity_provider.read_user("test1@example.com")["UserAttributes"]
        old_sub = next(attr['Value'] for attr in old_user_attrs if attr['Name'] == 'sub')
        new_sub = next(attr['Value'] for attr in new_user_attrs if attr['Name'] == 'sub')
        mock_resend_password.assert_called_once_with(
            UserPoolId=identity_provider.user_pool_id,
            Username="test1@example.com",
            MessageAction='RESEND',
            UserAttributes=[
                {'Name': 'email', 'Value': "test1@example.com"},
                {'Name': 'email_verified', 'Value': "true"}
            ],
        )
        assert old_sub != new_sub
        
        


def test_disable_user(identity_provider: UserInterface) -> None:
    with patch.object(identity_provider.client, 'admin_disable_user') as mock_disable_user:
        identity_provider.disable_user("test_user_id")
        mock_disable_user.assert_called_once_with(
            UserPoolId=identity_provider.user_pool_id,
            Username="test_user_id"
        )

def test_delete_user(identity_provider: UserInterface) -> None:
    with patch.object(identity_provider.client, 'admin_delete_user') as mock_delete_user:
        identity_provider.delete_user(Username="test1@example.com")
        mock_delete_user.assert_called_once_with(
            UserPoolId=identity_provider.user_pool_id,
            Username="test_user_id"
        )
    