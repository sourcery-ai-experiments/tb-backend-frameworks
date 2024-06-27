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
            

    def update(self, key: Dict[str, Any]) -> None:
        pass

    def delete(self, key: Dict[str, Any]) -> None:
        pass
    