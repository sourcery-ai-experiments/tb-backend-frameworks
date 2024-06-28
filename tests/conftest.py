import os
import logging
import pytest
import boto3
from moto import mock_aws
from db_framework.DynamoDBProvider import DynamoDBProvider 
from user_framework.CognitoUserProvider import CognitoUserProvider

@pytest.fixture()
def aws_credentials():
    """Mocked AWS Credentials."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    yield
    
@pytest.fixture()
def logger():
    "Python logger"
    logger = logging.getLogger("DynamoDbProvider")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
    
@pytest.fixture()
def dynamo_db(aws_credentials):
    """Mock AWS service with moto."""
    with mock_aws():
        yield boto3.resource("dynamodb")
        
@pytest.fixture()
def cognito(aws_credentials):
    with mock_aws():
        yield boto3.client("cognito-idp")
        
@pytest.fixture
def database(dynamo_db, logger) -> DynamoDBProvider:
    """DynamoDBProvider instance."""
    return DynamoDBProvider(table="test_table", logger=logger)

@pytest.fixture
def create_table():
    """Create a DynamoDB table with mock data."""
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
        
    
@pytest.fixture
def identity_provider(cognito, logger):
    client = boto3.client('cognito-idp', region_name='eu-west-2')
    user_pool_id = client.create_user_pool(PoolName='test_pool')['UserPool']['Id']
    client_id = client.create_user_pool_client(UserPoolId=user_pool_id, ClientName="test_client")
    for user in ["test1@test.com", "test2@test.com"]:
        client.admin_create_user(UserPoolId=user_pool_id,
                                Username=user,
                                MessageAction="SUPPRESS",
                                UserAttributes=[
                                    {'Name': 'email', 'Value': user},
                                    {'Name': 'email_verified', 'Value': "true"}],
        )
    
    yield CognitoUserProvider(user_pool_id, client_id, "eu-west-2", logger)
    
    
