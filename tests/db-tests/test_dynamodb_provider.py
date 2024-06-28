import pytest
from typing import Generator
from unittest.mock import patch
from botocore.exceptions import ClientError
from db_framework.DynamoDBProvider import DynamoDBProvider
from db_framework.Interface import DatabaseInterface

def test_dynamodb_provider_conformance(database: DatabaseInterface) -> None:
    assert isinstance(database, DatabaseInterface)

def test_create_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    item = {"id": "4", "name": "test4"}
    with patch.object(database.table, 'put_item') as mock_put_item:
        database.create(item)
        mock_put_item.assert_called_once_with(Item=item)

def test_read_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    item = {"id": "1", "name": "test1"}
    with patch.object(database.table, 'get_item', return_value={"Item": item}) as mock_get_item:
        read_item = database.read({"id": "1"})
        mock_get_item.assert_called_once_with(Key={"id": "1"})
        assert item == read_item

def test_update_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    update_values = {"name": "updated_name2"}
    with patch.object(database.table, 'update_item') as mock_update_item:
        database.update({"id": "2"}, update_values)
        mock_update_item.assert_called_once_with(
            Key={"id": "2"},
            UpdateExpression="SET #name=:name",
            ExpressionAttributeValues={":name": "updated_name2"},
            ExpressionAttributeNames={"#name": "name"}
        )

def test_delete_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    with patch.object(database.table, 'delete_item') as mock_delete_item:
        database.delete({"id": "3"})
        mock_delete_item.assert_called_once_with(Key={"id": "3"})
        
def test_create_item_empty(database: DynamoDBProvider) -> None:
    with patch.object(database.table, 'put_item') as mock_put_item:
        database.create({})
        mock_put_item.assert_not_called()

def test_read_item_not_found(database: DynamoDBProvider) -> None:
    with patch.object(database.table, 'get_item', return_value={}) as mock_get_item:
        read_item = database.read({"id": "nonexistent"})
        mock_get_item.assert_called_once_with(Key={"id": "nonexistent"})
        assert read_item == {}

def test_update_item_missing_key(database: DynamoDBProvider) -> None:
    with pytest.raises(ClientError):
        database.update({}, {"name": "updated_name"})

def test_delete_item_missing_key(database: DynamoDBProvider) -> None:
    with pytest.raises(ClientError):
        database.delete({})