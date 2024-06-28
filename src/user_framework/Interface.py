from typing import Protocol, runtime_checkable

@runtime_checkable
class UserInterface(Protocol):
    def __init__(self, user_pool_id: str, client_id: str, region_name: str) -> None:
        ...

    def create_user(self, email: str) -> None:
        ...

    def resend_temp_password(self, email: str) -> None:
        ...

    def disable_user(self, user_id: str) -> None:
        ...
    
    def delete_user(self, user_id: str) -> None:
        ...
