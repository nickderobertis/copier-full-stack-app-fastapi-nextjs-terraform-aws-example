import boto3
from mypy_boto3_ssm import SSMClient


def get_client() -> SSMClient:
    return boto3.client("ssm")


# TODO: Don't hard-code global region
def get_global_client(global_region: str = "us-west-1") -> SSMClient:
    return boto3.client("ssm", region_name=global_region)
