try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata  # type: ignore

__version__: str = importlib_metadata.version(__name__)  # type: ignore
