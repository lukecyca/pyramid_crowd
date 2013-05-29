from setuptools import setup

setup(
    name='pyramid_multiauth',
    version='0.1',
    author='Luke Cyca',
    author_email='me@lukecyca.com',
    packages=['pyramid_multiauth'],
    install_requires=[
        'Crowd',
    ],
)
