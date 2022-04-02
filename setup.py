from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in farmley/__init__.py
from farmley import __version__ as version

setup(
	name="farmley",
	version=version,
	description="OMS for order management",
	author="Sunny",
	author_email="sunny.shubham@farmley.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
