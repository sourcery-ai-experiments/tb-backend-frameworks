import boto3
from botocore.exceptions import ClientError
import logging
from typing import Any, Dict
from .Interface import DatabaseInterface

class DynamoDBProvider(DatabaseInterface):
    def __init__(self, table: str, logging_level: str):
        self.dynamodb = boto3.resource('dynamodb', "eu-west-2")
        self.table = self.dynamodb.Table(table)
        self.logger = logging.getLogger("DynamoDbProvider")
        self.logger.setLevel(logging_level)
    
    
    def create(self, item: Dict[str, Any]) -> None:
        try: 
            self.logger.debug(f"Attempting to create item {item}")
            res = self.table.put_item(Item=item)
            self.logger.debug(f"Created item: {item}, res: {res}")
        except ClientError as e:
            self.logger.error(f"Error creating item with key: {item}, error: {e}")
    
    def read(self, key: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.logger.debug(f"Attempting to read item with key: {key}")
            res = self.table.get_item(Key=key)
            self.logger.debug(f"Read item with key: {key}")
            
            return res.get("Item", {})
        except ClientError as e:
            self.logger.error(f"Failed to read item with key: {key} - error: {e}")
            

    def update(self, key: Dict[str, Any], update_values: Dict[str, Any]) -> None:
        try:
            self.logger.debug(f"Attempting to update item with key: {key} to {update_values}")
            update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in update_values)
            expression_attribute_values = {f":{k}": v for k, v in update_values.items()}
            expression_attribute_names = {f"#{k}": k for k in update_values}
            self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names
            )
            self.logger.debug(f"Updated item with key: {key} to {update_values}")
        except ClientError as e:
            self.logger.error(f"Error updating item with key: {key} to {update_values}, error: {e}")

    def delete(self, key: Dict[str, Any]) -> None:
        self.table.delete_item(Key=key)
    