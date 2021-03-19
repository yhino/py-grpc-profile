import asyncio
import logging
import time

import grpc
from example.echo.echo_pb2 import EchoMessage
from example.echo.echo_pb2_grpc import EchoServicer, add_EchoServicer_to_server

from py_grpc_profile.aio.server.interceptor import ProfileInterceptor


class EchoService(EchoServicer):
    def Echo(self, request, context):
        logging.info(f"start: {self.__class__.__name__}")
        time.sleep(1)
        logging.info(f"finish: {self.__class__.__name__}")
        return EchoMessage(msg=request.msg.upper())


async def serve():
    server = grpc.aio.server(
        interceptors=(ProfileInterceptor(),),
    )
    add_EchoServicer_to_server(EchoService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
