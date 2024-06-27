import os
import logging
import pytest
import boto3
from moto import mock_aws
from db_framework.DynamoDBProvider import DynamoDBProvider 

@pytest.fixture()
def aws_credentials():
    """Mocked AWS Credentials"""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    yield

@pytest.fixture()
def aws(aws_credentials):
    with mock_aws():
        yield boto3.resource("dynamodb", region_name="eu-west-2")
        
        
@pytest.fixture
def database(aws) -> DynamoDBProvider:
    logger = logging.getLogger("DynamoDbProvider")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return DynamoDBProvider(table="test_table", logger=logger)
        

@pytest.fixture
def create_table():
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
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
        with table.batch_writer() as batch:
            batch.put_item(Item={"id": "1", "name": "test1"})
            batch.put_item(Item={"id": "2", "name": "test2"})
            batch.put_item(Item={"id": "3", "name": "test3"})
        yield
        table.delete()
        


