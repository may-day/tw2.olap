#-*- coding:utf-8 -*-
from setuptools import setup, find_packages

# Odd hack to get tests running smoothly on py2.7
try:
    import multiprocessing
    import logging
except:
    pass

setup(
    name='tw2.olap',
    version='0.0.1',
    description='ToscaWidgets 2 OLAP Elements.',
    long_description=open('README').read(),
    author='Norman Krämer',
    author_email='kraemer.norman@gmail.com',
    url='https://github.com/may-day/tw2.olap',
    license='Apache Software License 2.0',
    install_requires=[
        "tw2.core",
        "olap",
        ],
    packages=find_packages(exclude=['tests']),
    namespace_packages = ['tw2'],
    zip_safe=False,
    include_package_data=True,
    tests_require = [
        'nose',
        'BeautifulSoup',
        'FormEncode',
        'WebTest',
        'strainer',

        'mako',
        'genshi',
    ],
    test_suite = 'nose.collector',
    entry_points="""
        [tw2.widgets]
        # Register your widgets so they can be listed in the WidgetBrowser
        widgets = tw2.olap.table
    """,
    keywords = [
        'toscawidgets.widgets',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: ToscaWidgets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
