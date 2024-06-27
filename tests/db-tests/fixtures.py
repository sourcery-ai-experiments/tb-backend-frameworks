import os
import pytest
import boto3
from moto import mock_aws
from ...src.db_framework.DynamoDBProvider import DynamoDBProvider 

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
def table_name() -> str:
    return "test_table"


@pytest.fixture
def create_table(table_name): 
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.create_table(
            TableName=table_name,
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
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        yield
        table.delete()
        
@pytest.fixture
def database(table_name) -> DynamoDBProvider:
    return DynamoDBProvider(table_name)

