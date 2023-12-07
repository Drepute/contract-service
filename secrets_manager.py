import json
import os

import boto3
from botocore.exceptions import ClientError


def handle_exception(e):
    if e.response["Error"]["Code"] == "DecryptionFailureException":
        # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response["Error"]["Code"] == "InternalServiceErrorException":
        # An error occurred on the server side.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response["Error"]["Code"] == "InvalidParameterException":
        # You provided an invalid value for a parameter.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response["Error"]["Code"] == "InvalidRequestException":
        # You provided a parameter value that is not valid for the current state of the resource.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response["Error"]["Code"] == "ResourceNotFoundException":
        # We can't find the resource that you asked for.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e


def get_boto_client():
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
    return client


def get_secret(secret_name):
    client = get_boto_client()
    password = None
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if get_secret_value_response is not None:
            password = get_secret_value_response["SecretString"]
    except ClientError as e:
        handle_exception(e)
    if password is not None:
        return json.loads(password)
    else:
        return dict()
