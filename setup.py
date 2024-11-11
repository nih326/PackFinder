from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()


setup(
    name="PackFinder",
    version="3.0",
    description="Django app to find roommates built for NCSU students",
    long_description=long_description,
    author="Chaitralee Datar, Ananya Patankar, Yash Shah",
    license="MIT",
    keywords="PackFinder",
    packages=find_packages(),
    install_requires=[],
)
