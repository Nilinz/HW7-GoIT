from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['clean-folder = clean_folder:clean:main']
    },
    install_requires=[
        'zupfile',
        'os',
        'shutil'
    ],
    author='Viktoriia T',
    author_email='greyhort@gmail.com',
    url='https://github.com/Nilinz/GoIT-HW7',
    description='A tool for cleaning up a folder by sorting files and unpacking archives',
    license='MIT',
)
