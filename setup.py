from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    hyphen = '-e .'
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if hyphen in requirements:
            requirements.remove(hyphen)
    return requirements

setup(
    name='mLproject',
    version='5.0.0',    
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    description='A machine learning project for data analysis and modeling.',
    author='Tushar',
    author_email='tusharpatidar2006@gmail.com'
)