import json
import os
from decimal import Decimal

import boto3
import pytest
from moto import mock_dynamodb2


@pytest.fixture(scope="session", autouse=True)
def environ(request):
    os.environ["IDEMPOTENCY_STORE_TABLE_NAME"] = "hogehoge"
    os.environ["LAMBDA_FUNCTION_NAME_ENV"] = "test-lambda"


@pytest.fixture()
def mock_dynamodb_table(monkeypatch):
    mock_dynamodb2().start()
    mock_table_name = os.getenv("IDEMPOTENCY_STORE_TABLE_NAME")

    dynamodb = boto3.resource("dynamodb")
    dynamodb.create_table(
        TableName=mock_table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}, {"AttributeName": "sk", "KeyType": "RANGE"}],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )

    yield dynamodb.Table(mock_table_name)

    mock_dynamodb2().stop()


def test_idempotency(mock_dynamodb_table):
    import lambda_app.index as app

    event = {"hoge_id": 1}
    response = app.handler(event, {})
    for _ in range(10):
        assert response == app.handler(event, {})

    items = mock_dynamodb_table.scan()["Items"]
    for item in items:
        assert item["sk"]
