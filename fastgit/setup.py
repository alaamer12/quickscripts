from setuptools import setup

setup(
    name='fastgit',
    version='0.10',
    packages=['utils'],
    url='',
    license='MIT',
    author='amr2023',
    author_email='',
    description='gitt',
    entry_points={
            'console_scripts': [
                'python run main.py = main:main',  # Assuming main.py contains a main function
            ],
        },
)
