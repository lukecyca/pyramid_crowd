from setuptools import setup

setup(
    name='pyramid_crowd',
    description='Pyramid authentication policy for Atlassian Crowd ',
    version='0.1',
    author='Luke Cyca',
    author_email='me@lukecyca.com',
    url='https://github.com/lukecyca/pyramid_crowd',

    packages=['pyramid_crowd'],
    install_requires=[
        #'Crowd',
        'pyramid',
    ],
)
