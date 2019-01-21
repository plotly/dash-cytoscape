import io
import json
import os
from setuptools import setup


with open(os.path.join('dash_cytoscape', 'package.json')) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    author_email=package['author-email'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package['description'] if 'description' in package else package_name,
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'dash',
        'dash-html-components',
        'dash_renderer',
    ],
    url='https://dash.plot.ly/cytoscape'
)
