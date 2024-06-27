import boto3
import logging
from typing import Any, Dict
from .Interface import DatabaseInterface
from .decorators import catch_exceptions

class DynamoDBProvider(DatabaseInterface):
    def __init__(self, table: str, logger: logging.Logger):
        self.dynamodb = boto3.resource('dynamodb', "eu-west-2")
        self.table = self.dynamodb.Table(table)
        self.logger = logger
    
    @catch_exceptions
    def create(self, item: Dict[str, Any]) -> None:
        self.table.put_item(Item=item)
    
    @catch_exceptions
    def read(self, key: Dict[str, Any]) -> Dict[str, Any]:
        res = self.table.get_item(Key=key)
        return res.get("Item", {})
    
    @catch_exceptions
    def update(self, key: Dict[str, Any], update_values: Dict[str, Any]) -> None:
        update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in update_values)
        expression_attribute_values = {f":{k}": v for k, v in update_values.items()}
        expression_attribute_names = {f"#{k}": k for k in update_values}
        self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )
    
    @catch_exceptions
    def delete(self, key: Dict[str, Any]) -> None:
        self.table.delete_item(Key=key)
    