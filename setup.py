"""A setuptools based setup module."""
from os import path
from setuptools import setup, find_packages
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
     long_description = f.read()

setup(
     name='fantasy-analytics',
     version='0.0.1',
     description='ESPN Fantasy Basketball Analytics Platform',
     long_description=long_description,
     long_description_content_type='text/markdown',
     url='https://github.com/themarathoncontinues/fantasy-analytics',
     author='Mitchell Bregman, Leon Kozlowski',
     author_email='mitchbregs@gmail.com, leonkozlowski@gmail.com',
     classifiers=[
         'Development Status :: 3 - Alpha',
         'Intended Audience :: Developers',
         'Topic :: Software Development :: Build Tools',
         'Programming Language :: Python :: 3.6'
     ],
     keywords='Fantasy Basketball Analytics',
     packages=find_packages(),
     install_requires=[
	 	'requests',
		'prefect',
		'flask',
		'python-dotenv',
		'prefect[viz]'
	 ]
)
