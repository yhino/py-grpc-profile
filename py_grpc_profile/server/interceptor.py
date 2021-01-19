import time
from cProfile import Profile
from timeit import default_timer
from typing import Callable, Optional, Tuple

import grpc
from grpc import HandlerCallDetails, ServerInterceptor


class ProfileInterceptor(ServerInterceptor):
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

    def intercept_service(
        self, continuation: Callable, handler_call_details: HandlerCallDetails
    ):
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

        return wrap_rpc_handler(continuation(handler_call_details), profile_wrapper)


def split_method_call(handler_call_details: HandlerCallDetails) -> Tuple[str, str]:
    parts = handler_call_details.method.split("/")
    if len(parts) < 3:
        return "", ""
    grpc_service_name, grpc_method_name = parts[1:3]
    return grpc_service_name, grpc_method_name


def wrap_rpc_handler(handler, fn):
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

    return handler_factory(
        behavior=fn(behavior_fn),
        request_deserializer=handler.request_deserializer,
        response_serializer=handler.response_serializer,
    )
