import functools
import inspect

from pydantic import validate_arguments
from plab.config import CONFIG


def measurement_without_validator(func):
    """measurement decorator.

    Adds a measurement name based on input parameters
    logs measurement metadata into CONFIG
    """

    @functools.wraps(func)
    def _measurement(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        arguments = ", ".join(args_repr + kwargs_repr)

        if args:
            raise ValueError(
                f"measurement supports only Keyword args for `{func.__name__}({arguments})`"
            )

        assert callable(
            func
        ), f"{func} got decorated with @measurement! @measurement decorator is only for functions"
        sig = inspect.signature(func)
        measurement = func(*args, **kwargs)
        settings = {}
        settings.update(
            **{
                p.name: p.default
                for p in sig.parameters.values()
                if not callable(p.default)
            }
        )
        settings.update(**kwargs)
        CONFIG.settings = settings

        return measurement

    return _measurement


def measurement(func, *args, **kwargs):
    return measurement_without_validator(validate_arguments(func), *args, **kwargs)
