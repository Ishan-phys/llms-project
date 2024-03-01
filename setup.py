from setuptools import find_packages, setup

setup(
    name='my_package',
    version='0.1.0',
    author='Ishan Srivastava',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'langchain==0.1.0',
        'python-dotenv==0.19.0'
    ]
)