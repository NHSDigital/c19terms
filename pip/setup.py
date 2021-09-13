import os
from setuptools import setup

setup(
    name='covid_19_terms',
    version=f'{os.environ["RELEASE_VERSION"]}',
    packages=['covid_19_terms'],
    package_dir={
        'covid_19_terms': 'covid_19_terms'
    },
    package_data={
        'covid_19_terms': ['terms.json']
    }
)
