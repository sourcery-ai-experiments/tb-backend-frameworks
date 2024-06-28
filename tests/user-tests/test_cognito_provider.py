from user_framework.Interface import UserInterface

def test_cognito_user_provider_conformance(identity_provider: UserInterface) -> None:
    assert isinstance(identity_provider, UserInterface)

def test_create_user(identity_provider: UserInterface) -> None:
    pass

def test_read_user(identity_provider: UserInterface) -> None:
    pass
    
def test_resend_temp_password(identity_provider: UserInterface) -> None:
    pass
    
def test_disable_user(identity_provider: UserInterface) -> None:
    pass
    
def test_delete_user(identity_provider: UserInterface) -> None:
    pass


    