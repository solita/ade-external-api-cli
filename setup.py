from setuptools import setup

setup(
    name='ext',
    version='0.1.0',
    py_modules=['ext'],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'ext = ext:ext',
        ],
    },
)