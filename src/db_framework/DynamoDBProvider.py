import boto3
from typing import Any, Dict
from .Interface import DatabaseInterface

class DynamoDBProvider(DatabaseInterface):
    def __init__(self, table: str):
        self.dynamodb = boto3.resource('dynamodb', "eu-west-2")
        self.table = self.dynamodb.Table(table)
    
    def create(self, item: Dict[str, Any]) -> None:
        pass
    
    def read(self, key: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def update(self, key: Dict[str, Any]) -> None:
        pass

    def delete(self, key: Dict[str, Any]) -> None:
        pass
    