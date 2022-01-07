from setuptools import setup, find_packages

metadata = {"__pkgname__": "quanvia"}

with open("README.md", "r") as fh:
    long_description = "This package helps describe the potential use cases for Quantum Computing."

with open(f'{metadata["__pkgname__"]}/__init__.py') as f:
    exec(f.readline(), metadata)

with open('requirements.txt', 'r') as req:
    requirements = [i.replace('\n', '') for i in req]

setup(
    name=metadata["__pkgname__"],
    description='Quanvia QC use cases portfolio',
    version=metadata["__version__"],
    author='Quanvia',
    author_email='contact@quanvia.com',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True
)