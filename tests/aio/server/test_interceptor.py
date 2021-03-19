import asyncio

import grpc
import pytest
from example.echo.echo_pb2 import EchoMessage
from pytest_grpc.plugin import FakeChannel


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from example.echo.echo_pb2_grpc import add_EchoServicer_to_server

    return add_EchoServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from example.async_server import EchoService

    return EchoService()


@pytest.fixture(scope="module")
def _grpc_server(grpc_addr, grpc_interceptors):
    server = grpc.aio.server(interceptors=grpc_interceptors)
    yield server


@pytest.fixture(scope="module")
@pytest.mark.asyncio
async def grpc_server(_grpc_server, grpc_addr, grpc_add_to_server, grpc_servicer):
    grpc_add_to_server(grpc_servicer, _grpc_server)
    _grpc_server.add_insecure_port(grpc_addr)
    await _grpc_server.start()
    yield _grpc_server
    await _grpc_server.stop(grace=None)


@pytest.fixture(scope="module")
@pytest.mark.asyncio
def grpc_create_channel(request, grpc_addr, grpc_server):
    def _create_channel(credentials=None, options=None):
        if request.config.getoption("grpc-fake"):
            return FakeChannel(grpc_server, credentials)
        if credentials is not None:
            return grpc.aio.secure_channel(grpc_addr, credentials, options)
        return grpc.aio.insecure_channel(grpc_addr, options)

    return _create_channel


@pytest.fixture(scope="module")
@pytest.mark.asyncio
async def grpc_channel(grpc_create_channel):
    async with grpc_create_channel() as channel:
        yield channel


@pytest.fixture(scope="module")
@pytest.mark.asyncio
def grpc_stub(grpc_channel):
    from example.echo.echo_pb2_grpc import EchoStub

    return EchoStub(grpc_channel)


@pytest.fixture(scope="module")
def grpc_interceptors():
    from py_grpc_profile.aio.server.interceptor import ProfileInterceptor

    return (ProfileInterceptor(),)


@pytest.mark.asyncio
async def test_intercept_service(grpc_stub):
    request = EchoMessage(msg="Hello")
    response = await grpc_stub.Echo(request)

    assert response.msg == request.msg.upper()
