from unittest import TestCase
from collections import defaultdict
import json

from PageRank import PageRank

data = None
with open('./tests/test_input.json', 'r') as infile:
  data = json.load(infile)

class PageRankTest(TestCase):

  def test_mapper(self):
    mr_input = data['page_rank']['mapper_input']
    results = {}
    mr_job = PageRank(['./test_input.json', '--rank-threshold=0.1'])

    results = [(k, v) for input_key, input_val in mr_input.items() for k, v in mr_job.mapper(input_key, input_val)]
    expectation = [(k, v) for k, v in data['page_rank']['mapper_output']]

    differences = [item for item in results if item not in expectation]

    self.assertEqual(len(differences), 0)

  def test_reducer(self):
    map_output = data['page_rank']['mapper_output']
    mr_input = defaultdict(list)

    for key, val in map_output:
      mr_input[key].append(val)

    results = {}
    mr_job = PageRank(['./test_input.json', '--rank-threshold=0.1'])

    results = [(k, v) for map_key, map_val in mr_input.items() for k, v in mr_job.reducer(map_key, map_val)]
    expectation = [(k, tuple(v)) for k, v in data['page_rank']['reducer_output']]

    differences = [item for item in results if item not in expectation]

    self.assertEqual(len(differences), 0)

if __name__ == '__main__':
    unittest.main()
