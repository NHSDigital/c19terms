from setuptools import setup
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

setup(
    name='covid_19_terms',
    version=metadata.version('pip'),
    packages=['covid_19_terms'],
    long_description="UK JSON COVID SNOMED CT codes from \"COVID-19 Vaccination Codes\" https://hscic.kahootz.com/connect.ti/t_c_home/view?objectId=16878800",
    long_description_content_type='text/markdown',
    package_dir={
        'covid_19_terms': 'covid_19_terms'
    },
    package_data={
        'covid_19_terms': ['terms.json']
    },
    install_requires=[
        'importlib-metadata >= 1.0 ; python_version < "3.8"',
    ],
)
