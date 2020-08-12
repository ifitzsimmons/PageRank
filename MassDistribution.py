from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

ALPHA = .15 # Googles number

class MassDistribution(MRJob):
  '''
  MRJob Class for distributing lost mass across non-dangling nodes.
  Also add dampening with alpha=.15, run once node rankings have converged
  '''

  INPUT_PROTOCOL = JSONProtocol

  def configure_args(self):
    ''' Set command line args for MassDistribution

    --total-nodes: int
      count of all the nodes in the graph

    --lost-mass: float
      Sum of the rank of all dangling nodes
    '''

    super(MassDistribution, self).configure_args()
    self.add_passthru_arg(
      '--total-nodes', type=int,
      help="Specify the total number of nodes"
    )
    self.add_passthru_arg(
      '--lost-mass', type=float,
      help="Specify the mass of lost rank"
    )

  def mapper(self, node_id, node):
    ''' Map function for Mass Distribution

    This method applies the lost mass and dampening to non-dangling
    nodes and filters out dangling nodes.

    PARAMETERS
    ----------
    node_id: int
      ID of the webpage

    node: list<list<int>, float>
      A list where the first item is an adjaceny list (list of outgoing links) and
      the second item is the current rank of the node.

    YIELDS
    ------
    int, int:
      Node ID and its final ranking
    '''

    # Remove dangling nodes
    if node_id == 'lost' or len(node[0]) == 0:
      return

    node_rank = node[1]
    new_rank = ALPHA/self.options.total_nodes + (1 - ALPHA) * (self.options.lost_mass/self.options.total_nodes + node_rank)

    yield node_id, new_rank

if __name__ == "__main__":
  MassDistribution.run()