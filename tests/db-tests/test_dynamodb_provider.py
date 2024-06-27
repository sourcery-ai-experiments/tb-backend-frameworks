from typing import Generator
from db_framework.DynamoDBProvider import DynamoDBProvider

def test_create_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    """
    Test creation of a new item in DynamoDB.

    Asserts that an item can be created using the DynamoDBProvider instance,
    and verifies that the created item matches the expected item.
    """
    item = {"id": "4", "name": "test4"}
    database.create(item)
    created_item = database.read({"id": "4"})
    assert item == created_item
    

def test_read_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    """
    Test reading an item from DynamoDB.

    Asserts that an item previously created in the DynamoDB table can be read
    successfully using the DynamoDBProvider instance.
    """
    item = {"id": "1", "name": "test1"}
    read_item = database.read({"id": "1"})
    assert item == read_item
    
    

def test_update_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    """
    Test updating an item in DynamoDB.

    Asserts that an existing item in the DynamoDB table can be updated
    successfully using the DynamoDBProvider instance, and verifies that
    the updated item matches the expected updated values.
    """
    item = {"id": "2", "name": "updated_name2"}
    database.update({"id": "2"}, {"name": "updated_name2"})
    updated_item = database.read({"id": "2"})
    assert item == updated_item
    

def test_delete_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    """
    Test deleting an item from DynamoDB.

    Asserts that an existing item in the DynamoDB table can be deleted
    successfully using the DynamoDBProvider instance, and verifies that
    the item is no longer present in the table.
    """
    database.delete({"id": "3"})
    deleted_item = database.read({"id": "3"})
    assert deleted_item == {}
