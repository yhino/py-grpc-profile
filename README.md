<h1 align="center">py-grpc-profile</h1>
<p align="center">
Profile the grpc server.<br>
Provide a grpc interceptor to profile each request in the cProfile module.
</p>

<p align="center">
    <a href="https://github.com/yhino/py-grpc-profile/actions/workflows/build.yml"><img src="https://github.com/yhino/py-grpc-profile/actions/workflows/build.yml/badge.svg" alt="build"></a>
    <a href="https://codecov.io/gh/yhino/py-grpc-profile"><img src="https://codecov.io/gh/yhino/py-grpc-profile/branch/main/graph/badge.svg?token=KWABCP5TYT"/></a>
    <a href="https://pypi.org/project/py-grpc-profile/"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/py-grpc-profile"></a>
</p>

## Installation

```shell
$ pip install -U py-grpc-profile
```

## Example

Load the module and set the interceptors.

```python
from concurrent import futures

import grpc
from py_grpc_profile.server.interceptor import ProfileInterceptor

# ...

server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=10),
    interceptors=[ProfileInterceptor()],
)

# ...
```

The complete code is available in [example](https://github.com/yhino/py-grpc-profile/tree/main/example). You can find more details there.

## License

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyhino%2Fpy-grpc-profile.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyhino%2Fpy-grpc-profile?ref=badge_shield)


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyhino%2Fpy-grpc-profile.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyhino%2Fpy-grpc-profile?ref=badge_large)
