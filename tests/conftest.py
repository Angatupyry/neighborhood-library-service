import grpc
import pytest_asyncio


@pytest_asyncio.fixture
async def grpc_channel():
    channel = grpc.aio.insecure_channel("localhost:50051")
    try:
        yield channel
    finally:
        await channel.close()
