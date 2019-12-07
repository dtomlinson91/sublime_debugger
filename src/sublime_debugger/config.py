from typing import Callable, Union
import os
import toml

from sublime_debugger.library import export
from sublime_debugger.__header__ import __header__ as header


__all__: list = []


@export
class Config:

    """Handles the config options for the module and stores config variables
    to be shared.

    Attributes
    ----------
    config_file : dict
        Contains the config options. See
        :meth:`~sublime_debugger.config.Config.read_config`
        for the data structure.
    deferred_messages : list
        A list containing the messages to be logged once the logger has been
        instantiated.
    module_name : str
        A string representing the module name. This is added in front of all
        envrionment variables and is the title of the `config.toml`.

    Parameters
    ----------
    path : str
        Path to config file
    """

    def __init__(self, path: str) -> None:
        """
        See :class:`~sublime_debugger.config.config.Config` for parameters.
        """
        self.deferred_messages = []
        self.config_file = self.read_config(path)
        self.module_name = header.lower()

    def read_config(self, path: str) -> Union[dict, None]:
        """Reads the toml config file from `path` if it exists.

        Parameters
        ----------
        path : str
            Path to config file. Should not contain `config.toml`

            Example: ``path = '~/.config/sublime_debugger'``

        Returns
        -------
        Union[dict, None]
            Returns a dict if the file is found else returns nothing.

            The dict contains a key for each header. Each key corresponds to a
            dictionary containing a key, value pair for each config under
            that header.

            Example::

                [sublime_debugger]

                [sublime_debugger.foo]
                foo = bar

            Returns a dict:

                ``{'sublime_debugger' : {foo: {'foo': 'bar'}}}``
        """

        path += 'config.toml' if path[-1] == '/' else '/config.toml'
        path = os.path.expanduser(path)
        try:
            with open(path, 'r+') as config_file:
                config_file = toml.load(config_file)
            self.defer_log(f'Config file found at {path}')
            return config_file
        except FileNotFoundError:
            self.defer_log(f'Config file not found at {path}')
            pass

    def get(
        self, key: str, default: str = None, cast: Callable = None
    ) -> Union[str, None]:
        """Retrives the config variable from either the `config.toml` or an
        environment variable. Will default to the default value if nothing
        is found

        Parameters
        ----------
        key : str
            Key to the configuration variable. Should be in the form
            `sublime_debugger.variable` or `sublime_debugger.header.variable`.
            When loaded, it will be accessable at
            `Config.sublime_debugger_variable` or
            `Config.sublime_debugger_header_variable`.
        default : str, optional
            The default value if nothing is found. Defaults to `None`.
        cast : Callable, optional
            The type of the variable. E.g `int` or `float`. Should reference
            the type object and not as string. Defaults to `None`.

        Returns
        -------
        Any
            Will return the config variable if found, or the default.
        """
        env_key = f"{header.upper()}_{key.upper().replace('.', '_')}"

        try:
            # look in the config.toml
            try:
                # look for subsections
                section, name = key.lower().split('.')
                value = self.config_file[self.module_name][section][name]
                self.defer_log(f'{env_key} found in config.toml')
            except ValueError:
                # look under top level module header
                name = key.lower()
                value = self.config_file[self.module_name][name]
                self.defer_log(f'{env_key} found in config.toml')
            finally:
                try:
                    # return if found in config.toml
                    return cast(value) if cast else value
                except UnboundLocalError:
                    # pass if nothing was found
                    pass
        except KeyError:
            self.defer_log(f'{env_key} not found in config.toml')
        except TypeError:
            self.defer_log(f'{env_key} not found in config.toml')

        # look for an environment variable
        value = os.environ.get(env_key)

        if value is not None:
            self.defer_log(f'{env_key} found in an environment variable')
        else:
            # fall back to default
            self.defer_log(f'{env_key} not found in an environment variable.')
            value = default
            self.defer_log(f'{env_key} set to default {default}')
        return cast(value) if cast else value

    def defer_log(self, msg: str) -> None:
        """Populates a list `Config.deferred_messages` with all the events to
        be passed to the logger later if required.

        Parameters
        ----------
        msg : str
            The message to be logged.
        """
        self.deferred_messages.append(msg)

    def reset_log(self) -> None:
        """Empties the list `Config.deferred_messages`.
        """
        del self.deferred_messages
        self.deferred_messages = []
