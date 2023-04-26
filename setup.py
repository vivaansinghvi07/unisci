from setuptools import setup

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name='uniconvert',
    version='1.0.0',
    author='Vivaan Singhvi',
    author_email='singhvi.vivaan@gmail.com',
    description='Units Conversions, and Science Package',
    long_description=description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['unisci'],
    python_requires='>=3.8',
    include_package_data=True
)