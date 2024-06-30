import logging
from typing import Protocol, runtime_checkable
from abc import abstractmethod

@runtime_checkable
class SubscriptionInterface(Protocol):
    def __init__(self, logger: logging.Logger) -> None:
        ...

    @abstractmethod
    def start_subscription(self, email: str, subscription_id: str, order_number: str, tier: str, sale_timestamp: str) -> None:
        ...
        
    @abstractmethod
    def pause_subscription(self, subscription_id: str) -> None:
        ...
        
    @abstractmethod
    def cancel_subscription(self, subscription_id: str) -> None:
        ...
 
    @abstractmethod
    def restart_subscription(self, ) -> None:
        ...
