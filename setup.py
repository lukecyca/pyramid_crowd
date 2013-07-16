from setuptools import setup

setup(
    name='pyramid_crowd',
    description='Pyramid authentication policy for Atlassian Crowd ',
    version='0.1',
    author='Luke Cyca',
    author_email='me@lukecyca.com',
    url='https://github.com/lukecyca/pyramid_crowd',
    license='BSD',

    packages=['pyramid_crowd'],
    install_requires=[
        'Crowd',
        'pyramid',
        'mock',
        'nose',
    ],

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        "Framework :: Pyramid",
    ]

)
