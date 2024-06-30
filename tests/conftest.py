import os
import logging
import pytest
import boto3
from moto import mock_aws
from db_framework.DynamoDBProvider import DynamoDBProvider 
from db_framework.Interface import DatabaseInterface
from user_framework.CognitoUserProvider import CognitoUserProvider
from user_framework.Interface import UserInterface
from subscription_framework.SubscriptionProvider import SubscriptionProvider
from subscription_framework.Interface import SubscriptionInterface

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
def logger_factory():
    """Logger factory fixture"""
    def _create_logger(name="DefaultLogger"):
        logger = logging.getLogger(name)
        logger.setLevel(logging.FATAL)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
    
        if not logger.handlers:
            logger.addHandler(handler)
        return logger
    yield _create_logger
    
@pytest.fixture()
def dynamo_db(aws_credentials):
    """Mock dynamodb service with moto."""
    with mock_aws():
        yield boto3.resource("dynamodb")
        
@pytest.fixture()
def cognito(aws_credentials):
    with mock_aws():
        """Mock congito service with moto"""
        yield boto3.client("cognito-idp")
        
@pytest.fixture
def database(dynamo_db, logger_factory) -> DatabaseInterface:
    """DynamoDBProvider instance."""
    logger = logger_factory("DynamoDbProvider")
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
def identity_provider(cognito, logger_factory) -> UserInterface:
    """Creates cogntio userpool and client id for with cognito identity provider"""
    client = boto3.client('cognito-idp', region_name='eu-west-2')
    user_pool_id = client.create_user_pool(PoolName='test_pool')['UserPool']['Id']
    client_id = client.create_user_pool_client(UserPoolId=user_pool_id, ClientName="test_client")
    for user in ["test1@example.com", "test2@exmple.com"]:
        client.admin_create_user(UserPoolId=user_pool_id,
                                Username=user,
                                MessageAction="SUPPRESS",
                                UserAttributes=[
                                    {'Name': 'email', 'Value': user},
                                    {'Name': 'email_verified', 'Value': "true"}],
        )
    logger = logger_factory("CognitoProvider")
    return CognitoUserProvider(user_pool_id, client_id, "eu-west-2", logger)
    
    
@pytest.fixture
def subscription(logger_factory) -> SubscriptionInterface:
    """Creates subscription provider"""
    logger = logger_factory("SubscriptionProvider")
    return SubscriptionProvider(logger)
    
    
