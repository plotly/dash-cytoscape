import io
import json
import os
from setuptools import setup, find_packages


with open(os.path.join('dash_cytoscape', 'package.json')) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    author_email=package['author-email'],
    packages=find_packages(include=[package_name, package_name + ".*"]),
    include_package_data=True,
    license=package['license'],
    description=package['description'] if 'description' in package else package_name,
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://dash.plotly.com/cytoscape',
    install_requires=[
        'dash',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database :: Front-Ends',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
