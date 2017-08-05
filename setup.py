import os

from setuptools import setup

ROOT = os.path.dirname(os.path.realpath(__file__))


setup(
    # Meta data
    name='user_agent',
    version='0.1.9',
    author="Gregory Petukhov",
    author_email='lorien@lorien.name',
    maintainer="Gregory Petukhov",
    maintainer_email='lorien@lorien.name',
    url='https://github.com/lorien/user_agent',
    description='User-Agent generator',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    download_url='http://pypi.python.org/pypi/user_agent',
    keywords="user agent browser navigator",
    license="MIT License",
    # Package files
    packages=['user_agent'],
    include_package_data=True,
    install_requires=['six'],
    entry_points={
        'console_scripts': [
            'ua = user_agent.cli:script_ua',
        ],
    },
    # Topics
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        #'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
