from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT = "-e ."


def get_requirements (file_path:str) -> List[str]:
    '''
    Function Description
    INPUT: A string of filepath of requirements/requires text file.
    RETURN: A list of requirments.
    '''
    
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [require.replace("\n", "") for require in requirements]
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements


setup(
    name='student_performance_indicator',
    version='0.0.1',
    author='Vineet kumar',
    author_email='krvinay9250@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)