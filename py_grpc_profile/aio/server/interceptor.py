import time
from cProfile import Profile
from timeit import default_timer
from typing import Awaitable, Callable, Optional

import grpc

from py_grpc_profile.server.interceptor import split_method_call, wrap_rpc_handler


class ProfileInterceptor(grpc.aio.ServerInterceptor):
    DEFAULT_FILENAME_FORMAT = (
        "grpc-server-{service}-{method}-{elapsed:.0f}ms-{time:.0f}.prof"
    )

    def __init__(
        self,
        filename_format: Optional[str] = None,
    ):
        self.filename_format = (
            self.DEFAULT_FILENAME_FORMAT if filename_format is None else filename_format
        )

    async def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        grpc_service_name, grpc_method_name = split_method_call(handler_call_details)

        def profile_wrapper(behavior):
            def new_behavior(request_or_iterator, servicer_context):
                profile = Profile()
                start = default_timer()
                profile.enable()

                try:
                    response_or_iterator = behavior(
                        request_or_iterator,
                        servicer_context,
                    )
                finally:
                    profile.disable()
                    elapsed = default_timer() - start
                    filename = self.filename_format.format(
                        service=grpc_service_name,
                        method=grpc_method_name,
                        elapsed=elapsed * 1000.0,
                        time=time.time(),
                    )
                    profile.dump_stats(filename)
                return response_or_iterator

            return new_behavior

        return wrap_rpc_handler(
            await continuation(handler_call_details), profile_wrapper
        )
