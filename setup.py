# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['sublime_debugger']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{u'console_scripts': ['sublime-debugger = sublime_debugger.console:cli']}

setup_kwargs = {
    'name': 'sublime-debugger',
    'version': '1.0',
    'description': '',
    'long_description': None,
    'author': 'dtomlinson',
    'author_email': 'dtomlinson@williamhill.co.uk',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
