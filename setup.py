# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.install import install

#version
VERSION = '0.0.1'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    name='teagmail',
    version=VERSION,
    description='python GmailApi library',
    long_description=readme,
    url='https://github.com/qqgg231/teagmail',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
)