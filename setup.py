import re

from setuptools import setup

with open("src/easyflask/__init__.py", encoding="utf-8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='easyflask',
    version=version,
    install_requires=[
        'aniso8601>=8.0.0',
        'click>=7.1.2',
        'Flask>=1.1.2',
        'Flask-RESTful>=0.3.8',
        'itsdangerous>=1.1.0',
        'Jinja2>=2.11.2',
        'MarkupSafe>=1.1.1',
        'pytz>=2020.1',
        'six>=1.15.0',
        'Werkzeug>=1.0.1'
    ]
)
