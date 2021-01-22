import asyncio
import logging

import grpc
from example.echo.echo_pb2 import EchoMessage
from example.echo.echo_pb2_grpc import EchoStub


async def run():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = EchoStub(channel)
        response = await stub.Echo(EchoMessage(msg="Hello"))
    print("received: " + response.msg)


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
