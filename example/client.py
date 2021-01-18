import logging

import grpc
from example.echo.echo_pb2 import EchoMessage
from example.echo.echo_pb2_grpc import EchoStub


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = EchoStub(channel)
        response = stub.Echo(EchoMessage(msg="Hi!!"))
    print("received: " + response.msg)


if __name__ == "__main__":
    logging.basicConfig()
    run()
