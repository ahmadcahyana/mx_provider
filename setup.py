from setuptools import find_packages, setup

setup(
    name='mx_provider',
    packages=find_packages(include=['mx_provider']),
    version='0.1.0',
    description='Get the mail server provider for a domain',
    author='Ahmad Cahyana',
    install_requires=[
        'tld',
        'dnspython',
        'pytest',
        'pytest-runner',
    ],
    setup_requires=['pytest-runner'],
    test_suite='tests',
)