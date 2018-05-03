'''Cloud ML Engine package configuration.'''
from setuptools import setup, find_packages

REQUIRED_PACKAGES = ['pandas>=0.22.0', 'xgboost==0.71'] # keras, h5py, lightgbm

setup(name='talkingdata_xgboost',
      version='1.0',
      packages=find_packages(),
      include_package_data=True,
      description='talkingdata_xgboost for Kaggle compret',
      author='Jirawat Boonkumnerd',
      author_email='jo06942@gmail.com',
      license='MIT',
      install_requires=REQUIRED_PACKAGES,
      zip_safe=False)
