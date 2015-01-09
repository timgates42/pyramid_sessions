# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

pkg_version = '0.1.0'


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open('requirements.txt').read()

testing_extras = open('test_requirements.txt').read()

setup(
    name='pyramid_sessions',
    version=pkg_version,
    description='Multiple session support for the Pyramid Web Framework',
    long_description=readme + '\n\n' + history,
    author='Julian Paul Glass',
    author_email='joulez@magemx.com',
    url='https://github.com/joulez/pyramid_sessions',
    packages=[
        'pyramid_sessions',
    ],
    package_dir={'pyramid_sessions':
                 'pyramid_sessions'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pyramid_sessions',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "License :: BSD",
    ],
    extras_require={
        'testing': testing_extras },
    test_suite='pyramid_sessions.tests',
    tests_require=['WebTest'])
