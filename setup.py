import setuptools

with open('README.rst') as file:

    readme = file.read()

name = 'lineopt'

version = '0.0.3'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    url = url,
    py_modules = [name],
    license = 'MIT',
    description = 'Command line based invoke framework.',
    long_description = readme,
    install_requires = [
        'flagopt'
    ],
    extras_require = {
        'docs': [
            'sphinx'
        ]
    }
)
