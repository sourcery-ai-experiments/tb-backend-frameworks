import boto3
import logging
from typing import Any, Dict
from .Interface import DatabaseInterface
from .decorators import catch_exceptions

class DynamoDBProvider(DatabaseInterface):
    """
    DynamoDBProvider is an implementation of the DatabaseInterface for AWS DynamoDB.

    It provides methods for performing basic CRUD operations on a specified DynamoDB table.
    """

    def __init__(self, table: str, logger: logging.Logger):
        """
        Initialize the DynamoDBProvider.

        :param table: The name of the DynamoDB table.
        :param logger: A logger instance for logging messages.
        """
        self.dynamodb = boto3.resource('dynamodb', "eu-west-2")
        self.table = self.dynamodb.Table(table)
        self.logger = logger
    
    @catch_exceptions
    def create(self, item: Dict[str, Any]) -> None:
        """
        Create a new item in the DynamoDB table.

        :param item: A dictionary representing the item to be created.
        """
        self.table.put_item(Item=item)
    
    @catch_exceptions
    def read(self, key: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read an item from the DynamoDB table.

        :param key: A dictionary representing the key of the item to be read.
        :return: A dictionary representing the retrieved item, or an empty dictionary if the item is not found.
        """
        res = self.table.get_item(Key=key)
        return res.get("Item", {})
    
    @catch_exceptions
    def update(self, key: Dict[str, Any], update_values: Dict[str, Any]) -> None:
        """
        Update an existing item in the DynamoDB table.

        :param key: A dictionary representing the key of the item to be updated.
        :param update_values: A dictionary representing the attributes to be updated and their new values.
        """
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
        """
        Delete an item from the DynamoDB table.

        :param key: A dictionary representing the key of the item to be deleted.
        """
        self.table.delete_item(Key=key)
