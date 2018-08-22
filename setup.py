from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='dna-common',
    url='https://github.com/hypoport/ep-dna-common',
    author='Jens Hanack',
    author_email='jens.hanack@europace.de',
    # Needed to actually package something
    packages=['dna-common'],
    # Needed for dependencies
    install_requires=['boto3'],
    version='0.1',
    description='Installierbares Python Package für Hilfsfunktionen im Umgang mit dem Data Lake, Data Warehouse und AWS',
    long_description=open('README.txt').read(),
)
