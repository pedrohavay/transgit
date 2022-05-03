#!/usr/bin/env python
import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

    def find_packages(where='.'):
        # os.walk -> list[(dirname, list[subdirs], list[files])]
        return [folder.replace(os.sep, ".").strip(".")
                for (folder, _, files) in os.walk(where)
                if "__init__.py" in files]

setup(
    name='transgit',
    version='0.0.1',
    url='https://pedrohavay.com',
    description='Open source tool to export Gitlab repositories to Github.',
    keywords='Git,Github,Gitlab',
    author='Pedro Havay',
    author_email='admin@pedrohavay.com',
    maintainer='Pedro Havay',
    platforms=['any'],
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "transgit = transgit.cli:main",
        ]
    },
    install_requires=[
        "click",
        "colorama",
        "requests",
        "git-filter-repo"
    ],
    extras_require={
        'complete': [
            # 'pyOpenSSL'
        ],
    }
)
