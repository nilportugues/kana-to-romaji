# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='kanatoromaji',
    version='0.1',
    author='Nil Portugués Calderó',
    author_email='contact@nilportugues.com',
    url='http://nilportugues.com/',
    license='BSD',
    packages=find_packages(exclude=('tests', 'docs', 'venv')),
    install_requires=[
        'virtualenv',
        'Flask',
        'flask-restplus==0.9.2',
        'flask-restful-swagger-2==0.35',
        'urllib3==1.22',
        'pykakasi',
        'mecab-python3'
    ],
    include_package_data=True,
    package_data={
        'static': ['*.dic', '*.aff'],
    },

)

# EOF


