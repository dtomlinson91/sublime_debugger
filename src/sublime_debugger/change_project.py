import json
from os.path import expanduser

import sublime_debugger
from sublime_debugger.library import export


__all__: list = []


@export
class SetEnvironment:
    """class to handle finding the sublime project file and updating the
    debugging python path with the current  variable

    Attributes
    ----------
    sublime_project_dict : dict
        sublime project loaded in a dict
    sublime_project_path : str
        path to the sublime project file
    virtualenv_path : str
        path to the active virtualenv
    """

    def __init__(self) -> None:
        self.sublime_project_path = (
            sublime_debugger.CONFIG.sublime_project_file
        )
        self.virtualenv_path = sublime_debugger.CONFIG.sublime_virtualenv
        super().__init__

    @staticmethod
    def _clean_path(path: str) -> str:
        """checks `path` and inserts a `/` if missing

        Parameters
        ----------
        path : str
            path to check

        Returns
        -------
        str
            returns `path` with a `/` on the end
        """
        path += '/' if path[-1] != '/' else ''
        return path

    def _read_sublime_project(self):
        """reads the sublime project file and loads into a dict
        """
        with open(expanduser(self.sublime_project_path), 'r') as project:
            self.sublime_project_dict = json.load(project)
        return self

    def _set_virtualenv(self, os: str = 'mac'):
        """facilities updating `self.sublime_project_dict` with the virtualenv
        """
        if os == 'mac':
            self.__get_mac_dict()
        return self

    def __get_mac_dict(self):
        """updates `self.sublime_project_dict` with the virtualenv for mac"""
        _python_path = self._clean_path(self.virtualenv_path) + 'bin/python'
        self.sublime_project_dict['settings']['debug.configurations'][0][
            'osx'
        ]['pythonPath'] = _python_path
        return self

    def _save_to_project(self):
        """updates the sublime project file"""
        with open(expanduser(self.sublime_project_path), 'w') as project:
            json.dump(self.sublime_project_dict, project, indent=4)
        return self

    def update_debugger_path(self):
        """update the sublime project file debugging path with the current
        `$VIRTUAL_ENV` environment variable"""
        self._read_sublime_project()
        self._set_virtualenv()
        self._save_to_project()


# if __name__ == '__main__':
#     import typing
#     print(typing.get_type_hints(SetEnvironment().update_debugger_path))
