from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Google Driver File Search',
    version='0.1.0',
    description="Application to search for document's content inside Google drive",
    long_description=readme,
    author='Nishith R Kashyap',
    author_email='nishithkp175@gmail.com',
    url='https://github.com/NishithKashyap/Google-Driver-File-Search',
    license=license,
    packages=find_packages(exclude=('test', 'docs'))
)