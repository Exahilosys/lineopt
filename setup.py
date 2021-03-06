import setuptools

with open('README.rst') as file:

    readme = file.read()

name = 'lineopt'

version = '0.1.0'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Command line based invoke framework.',
    long_description = readme
)
