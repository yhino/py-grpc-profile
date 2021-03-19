from typing import Awaitable, Callable, Optional

import grpc

from py_grpc_profile.adapter import Adapter, CProfileAdapter
from py_grpc_profile.server.interceptor import get_rcp_handler, split_method_call


class ProfileInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, profiler: Optional[Adapter] = None):
        if profiler is None:
            profiler = CProfileAdapter()
        self.profiler = profiler

    async def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], Awaitable[grpc.RpcMethodHandler]
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        handler = await continuation(handler_call_details)
        behavior, handler_factory = get_rcp_handler(handler)

        def _intercept(request_or_iterator, servicer_context):
            grpc_service_name, grpc_method_name = split_method_call(
                handler_call_details
            )

            return self.profiler.run(
                behavior,
                request_or_iterator,
                servicer_context,
                {
                    "grpc_service_name": grpc_service_name,
                    "grpc_method_name": grpc_method_name,
                },
            )

        return handler_factory(
            behavior=_intercept,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )
