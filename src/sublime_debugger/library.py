# Change sublime_debug
from __future__ import annotations
import sys
from typing import Any, TypeVar, Type, TYPE_CHECKING

if TYPE_CHECKING:
    import logging


config_inst_t = TypeVar('config_inst_t', bound='sublime_debug.config.Config')


def export(fn: callable) -> callable:
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        mod.__all__.append(fn.__name__)
    else:
        mod.__all__ = [fn.__name__]
    return fn


def set_config(
    config_inst: Type[config_inst_t],
    key: str,
    default: str = None,
    cast: Any = None,
) -> None:
    """Sets the config variable on the instance of a class.

    Parameters
    ----------
    config_inst : Type[config_inst_t]
        Instance of the :class:`~sublime_debug.config.Config` class.
    key : str
        The key referencing the config variable.
    default : str, optional
        The default value.
    cast : Any, optional
        The type of the variable.
    """
    config_var = key.lower().replace('.', '_')
    setattr(config_inst, config_var, config_inst.get(key, default, cast))


# Create function to print cached logged messages and reset
def process_cached_logs(
    config_inst: Type[config_inst_t],
    logger: logging.Logger
):
    """Prints the cached messages from :class:`~sublime_debug.config.Config`
    and resets the cache.

    Parameters
    ----------
    config_inst : Type[config_inst_t]
        Instance of :class:`~sublime_debug.config.Config`.
    logger : logging.Logger
        Instance of the logger.
    """
    for msg in config_inst.deferred_messages:
        logger.info(msg)
    config_inst.reset_log()
