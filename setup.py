# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='teagmail',
    version='0.0.1',
    description='python GmailApi library',
    long_description=readme,
    url='https://github.com/qqgg231/teagmail',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
)