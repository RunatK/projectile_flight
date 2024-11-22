from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='projectile_flight',
  version='0.0.1',
  author='rinat_kuchaev',
  author_email='rkuchaev.2011@gmail.com',
  description='This is the simplest module for quick calculation of projectile contact with the surface.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/RunatK/projectile_flight',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='projectile',
  project_urls={
    'GitHub': 'https://github.com/RunatK/projectile_flight'
  },
  python_requires='>=3.6'
)