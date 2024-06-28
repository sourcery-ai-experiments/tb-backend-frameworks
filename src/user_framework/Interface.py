from typing import Protocol, runtime_checkable
from abc import abstractmethod

@runtime_checkable
class UserInterface(Protocol):
    def __init__(self, user_pool_id: str, client_id: str, region_name: str) -> None:
        ...

    @abstractmethod
    def create_user(self, email: str) -> None:
        ...
        
    @abstractmethod
    def read_user(self, email: str) -> None:
        ...
        
    @abstractmethod
    def resend_temp_password(self, email: str) -> None:
        ...

    @abstractmethod
    def disable_user(self, user_id: str) -> None:
        ...
    
    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        ...
