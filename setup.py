from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name='unisci',
    version='1.5.0',
    author='Vivaan Singhvi',
    author_email='singhvi.vivaan@gmail.com',
    description='Units Conversions, and Science Package',
    long_description=description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.8',
    include_package_data=True,
    project_urls={
        "Documentation": "https://unisci.readthedocs.io/en/latest/"
    },
    install_requires=requirements
)