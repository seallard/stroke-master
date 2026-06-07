"""Object storage for raw per-sample streams (S3-compatible).

Raw streams are the heavy data and live here (compressed), keyed by activity; Postgres
only stores the object key plus derived aggregates. boto3 is sync, so calls are run in a
thread to keep the async event loop free.
"""

import asyncio

import boto3

from .config import get_settings


def _client():
    s = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=s.s3_endpoint or None,
        aws_access_key_id=s.s3_access_key_id or None,
        aws_secret_access_key=s.s3_secret_access_key or None,
    )


def stream_key(activity_id: str) -> str:
    return f"streams/{activity_id}.parquet"


async def put_stream(key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
    s = get_settings()
    await asyncio.to_thread(
        lambda: _client().put_object(
            Bucket=s.s3_bucket, Key=key, Body=data, ContentType=content_type
        )
    )
    return key


async def get_stream(key: str) -> bytes:
    s = get_settings()
    obj = await asyncio.to_thread(lambda: _client().get_object(Bucket=s.s3_bucket, Key=key))
    return await asyncio.to_thread(obj["Body"].read)
