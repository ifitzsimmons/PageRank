import setuptools

setuptools.setup(
  name='PageRank',
  version='0.1',
  description='PageRank with MRJob',
  long_description='PageRank based on Google\'s PageRank algorithm, including lost mass and dampening.',
  author='Ian Fitzsimmons',
  packages=setuptools.find_packages(),
  test_suite='nose.collector',
  tests_require=['nose', 'mrjob'],
  include_package_data=True,
  zip_safe=False
)