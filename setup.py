from setuptools import setup, find_packages

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='dnacommon',
    url='https://github.com/hypoport/ep-dna-common',
    author='Jens Hanack',
    author_email='jens.hanack@europace.de',
    # Needed to actually package something
    packages=find_packages(exclude=['tests', 'scripts']),
    # Needed for dependencies
    install_requires=['boto3',
                      'dataclasses',
                      'sqlalchemy',
                      'python-aws-dataclasses',
                      'sqlalchemy-redshift',
                      'python-aws-dataclasses',
                      'pynamodb',
                      'PyJWT',
                      'pycrypto'
                      ],
    version='1.0',
    description='Installierbares Python Package für Hilfsfunktionen im Umgang mit dem Data Lake, Data Warehouse und AWS',
    # long_description=open('README.md').read(),
)
