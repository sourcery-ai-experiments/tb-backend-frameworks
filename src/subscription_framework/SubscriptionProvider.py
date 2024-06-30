import boto3
import logging
from subscription_framework.Interface import SubscriptionInterface
from decorators import catch_exceptions


class SubscriptionProvider(SubscriptionInterface):
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        
    def start_subscription(self, email: str, subscription_id: str, order_number: str, tier: str, sale_timestamp: str) -> None:
        pass
    def cancel_subscription(self, subscription_id: str) -> None:
        pass
    def pause_subscription(self, subscription_id: str) -> None:
        pass
    def restart_subscription(self) -> None:
        pass