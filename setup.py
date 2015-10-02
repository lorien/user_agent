from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    name='user_agent',
    version='0.0.7',
    description='User-Agent generator',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    packages=find_packages(exclude=['script']),
    install_requires=['six'],
    license="MIT",
    keywords="user agent browser navigator",
    author="jamb0ss, Gregory Petukhov",
    author_email='lorien@lorien.name',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        #'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        #'Development Status :: 5 - Production/Stable',
        #'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        #'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
