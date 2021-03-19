from typing import Callable, Optional, Tuple

import grpc

from py_grpc_profile.adapter import Adapter, CProfileAdapter


class ProfileInterceptor(grpc.ServerInterceptor):
    def __init__(self, profiler: Optional[Adapter] = None):
        if profiler is None:
            profiler = CProfileAdapter()
        self.profiler = profiler

    def intercept_service(
        self,
        continuation: Callable[[grpc.HandlerCallDetails], grpc.RpcMethodHandler],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        handler = continuation(handler_call_details)
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


def split_method_call(handler_call_details: grpc.HandlerCallDetails) -> Tuple[str, str]:
    parts = handler_call_details.method.split("/")
    if len(parts) < 3:
        return "", ""
    grpc_service_name, grpc_method_name = parts[1:3]
    return grpc_service_name, grpc_method_name


def get_rcp_handler(handler: grpc.RpcMethodHandler):
    if handler is None:
        return None

    if handler.request_streaming and handler.response_streaming:
        behavior_fn = handler.stream_stream
        handler_factory = grpc.stream_stream_rpc_method_handler
    elif handler.request_streaming and not handler.response_streaming:
        behavior_fn = handler.stream_unary
        handler_factory = grpc.stream_unary_rpc_method_handler
    elif not handler.request_streaming and handler.response_streaming:
        behavior_fn = handler.unary_stream
        handler_factory = grpc.unary_stream_rpc_method_handler
    else:
        behavior_fn = handler.unary_unary
        handler_factory = grpc.unary_unary_rpc_method_handler

    return behavior_fn, handler_factory
