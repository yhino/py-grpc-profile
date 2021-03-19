import pytest
from example.echo.echo_pb2 import EchoMessage


@pytest.fixture(scope="module")
def grpc_add_to_server():
    from example.echo.echo_pb2_grpc import add_EchoServicer_to_server

    return add_EchoServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    from example.server import EchoService

    return EchoService()


@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    from example.echo.echo_pb2_grpc import EchoStub

    return EchoStub(grpc_channel)


@pytest.fixture(scope="module")
def grpc_interceptors():
    from py_grpc_profile.server.interceptor import ProfileInterceptor

    return [ProfileInterceptor()]


def test_intercept_service(grpc_stub):
    request = EchoMessage(msg="Hello")
    response = grpc_stub.Echo(request)

    assert response.msg == request.msg.upper()
