from PageRank import PageRank
from MassDistribution import MassDistribution

import argparse
from pprint import pprint
import shutil

# Where to put output from each iteration
OUTDIR = './output/output_round_'

def add_arguments():
  '''Add command line argument for PageRank calculation string

  --input-file: str
    file of graph nodes

  --rank-threshold: float
    Defines threshold at which we consider PageRank for a particular page
    converged
  '''

  parser.add_argument("--input-file", required=True,
          help=("File or files with node structure"))
  parser.add_argument("--rank-threshold", required=True,
          help=("Convergence Threshold"))

def get_mr_job(iteration, threshold):
  '''Returns MRJob depending on iteration

  First iteration uses the input file, every iteration after that
  will use the previous iterations output until Rank converges

  PARAMETERS
  ----------
  iteration: int
    current PageRank iteration

  threshold: float
    Defines convergence threshold for rank

  RETURNS
  -------
  PageRank: MRJob
    PageRank job
  '''

  output = f'--output-dir={OUTDIR}{iterations}'
  if not iterations:
    return PageRank([json_file, output, threshold])
  else:
    input_dir = f'{OUTDIR}{iterations-1}'
    return PageRank([input_dir, output, threshold])


if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  add_arguments()
  args = parser.parse_args()

  json_file = args.input_file
  threshold = args.rank_threshold
  threshold_arg = f'--rank-threshold={threshold}'

  unconverged_nodes = True
  iterations = 0
  lost_mass = 0

  ''' Iterative ranking without lost mass distribution or dampening'''
  while unconverged_nodes:
    mr_job = get_mr_job(iterations, threshold_arg)

    with mr_job.make_runner() as runner:
      runner.run()
      counters = runner.counters()
      pprint(counters)

      total_nodes =counters[0]['mapper_rank']['total_nodes']

      try:
        # If there are unconverged nodes, move to next iteration
        unconverged_nodes = counters[0]['reducer1']['unconverged_nodes'] > 0
        iterations += 1
      except:
        # if there are no unconverged_nodes, move on to mass distribution and balancing
        unconverged_nodes = False

        for k, v in mr_job.parse_output(runner.cat_output()):
          if k == 'lost':
            lost_mass = v[1]


  ''' Mass Distribution and Dampening '''
  input_dir = f'{OUTDIR}{iterations}'
  total_nodes_arg = f'--total-nodes={total_nodes}'
  lost_mass_arg = f'--lost-mass={lost_mass}'

  mr_job2 = MassDistribution([input_dir, total_nodes_arg, lost_mass_arg])
  with mr_job2.make_runner() as runner2:
    runner2.run()

    output2 = runner2.get_output_dir()
    for k, v in mr_job2.parse_output(runner2.cat_output()):
      print(k, v)

  # ToDo - add this on sys.exit of any kind
  shutil.rmtree('./output', ignore_errors=True)