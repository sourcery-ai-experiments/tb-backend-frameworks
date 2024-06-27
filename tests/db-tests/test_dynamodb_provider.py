
from typing import Generator
from db_framework.DynamoDBProvider import DynamoDBProvider

def test_create_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    item = {"id": "4", "name": "test4"}
    database.create(item)
    created_item = database.read({"id": "4"})
    assert item == created_item
    

def test_read_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    item = {"id": "1", "name": "test1"}
    read_item = database.read({"id": "1"})
    assert item == read_item
    
    

def test_update_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    item = {"id": "2", "name": "updated_name2"}
    database.update(item)
    updated_item = database.read({"id": "2"})
    assert item == updated_item
    

def test_delete_item(database: DynamoDBProvider, create_table: Generator[None, None, None]) -> None:
    database.delete({"id": "3"})
    deleted_item = database.read({"id": "3"})
    assert deleted_item == {}

