import time
from cProfile import Profile
from timeit import default_timer
from typing import Dict, Optional

from py_grpc_profile.adapter.interfaces import Adapter


class CProfileAdapter(Adapter):
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

    def run(self, behavior, request_or_iterator, servicer_context, metadata: Dict):
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
                service=metadata["grpc_service_name"],
                method=metadata["grpc_method_name"],
                elapsed=elapsed * 1000.0,
                time=time.time(),
            )
            profile.dump_stats(filename)
        return response_or_iterator
