'''Cloud ML Engine package configuration.'''
from setuptools import setup, find_packages

REQUIRED_PACKAGES = ['pandas>=0.22.0','lightgbm'] # keras, h5py

setup(name='talkingdata_lstm',
      version='1.0',
      packages=find_packages(),
      include_package_data=True,
      description='talkingdata_lstm for Kaggle compret',
      author='Jirawat Boonkumnerd',
      author_email='jo06942@gmail.com',
      license='MIT',
      install_requires=REQUIRED_PACKAGES,
      zip_safe=False)
