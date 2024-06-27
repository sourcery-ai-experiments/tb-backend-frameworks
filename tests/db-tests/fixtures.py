import os
import pytest
import boto3
from moto import mock_aws
from db_framework.DynamoDBProvider import DynamoDBProvider 

@pytest.fixture(scope="function")
def aws_credentials() -> None:
    """Mocked AWS Credentials"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def aws(aws_credentials):
    with mock_aws():
        yield boto3.resource("dynamodb", region_name="eu-west-2")
        
        
@pytest.fixture
def database() -> DynamoDBProvider:
    return DynamoDBProvider("test_table")
        

@pytest.fixture
def create_table(database):
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.create_table(
            TableName="test_table",
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName="test_table")
        database.create({"id": "1", "name": "test1"})
        database.create({"id": "2", "name": "test2"})
        database.create({"id": "3", "name": "test3"})
        yield
        table.delete()
        


