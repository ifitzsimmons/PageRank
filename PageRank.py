from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

class PageRank(MRJob):
  '''
  MRJob Class for performing initial PageRank. Does not include
  lost mass or dampening.
  '''

  INPUT_PROTOCOL = JSONProtocol

  def configure_args(self):
    ''' Set command line args for PageRank

    --rank-threshold: float
      Defines threshold at which we consider PageRank for a particular page
      converged
    '''

    super(PageRank, self).configure_args()
    self.add_passthru_arg(
      '--rank-threshold', type=float,
      help="Point at which we consider a node rank to be converged"
    )

  def mapper(self, node_id, node):
    ''' Map function for PageRank

    This method takes key, value inputs and yields either the key with the same
    value OR the key with a specific rank for an outgoing link

    PARAMETERS
    ----------
    node_id: int
      ID of the webpage

    node: list<list<int>, float>
      A list where the first item is an adjaceny list (list of outgoing links) and
      the second item is the current rank of the node.

    YIELDS
    ------
    int, list<list<int>, float>:
      To maintain node structure, each node must yield itself

    int, int:
      Node ID from the adjacency link and the outgoing rank of the
      current node (currentRank/len(adj_list))

    str, int:
      To account for lost_mass from dangling nodes, all nodes with no entries
      in the adjacency list are emitted with a key of 'lost' and the current
      rank
    '''

    if node_id == 'lost':
      return

    self.increment_counter('mapper_rank', 'total_nodes', 1)

    adj_list, node_rank = node

    yield node_id, [adj_list, node_rank]

    if not len(adj_list):
      yield 'lost', node_rank
      return


    outgoing_rank = node_rank / len(adj_list)

    for linked_node in adj_list:
      yield linked_node, outgoing_rank

  def reducer(self, node_id, node_rank):
    ''' Reduce function for PageRank

    Sums up all ranks from backlinks for each node and emits the node
    with its adjacency list and new ranks.

    PARAMETERS
    ----------
    node_id: int | str
      ID of the webpage of 'list' for dangling nodes

    node_rank: list<int | list<list<int>, float>>
      int:
        Rank from the current nodes backlink
      list<list<int>, float>:
        Nodes previously calculated rank along with its adjacency list

    YIELDS
    ------
    int, list<list<int>, float>:
      Node ID with newly calculated rank along with its adjacency list
    '''

    new_rank = 0
    prev_rank = 0
    adj_list = []

    # Should be called for all keys except for 'lost'
    includes_node = False

    for rank in node_rank:
      if type(rank) == list:
        adj_list, prev_rank = rank
        includes_node = True
      elif type(rank) in [int, float]:
        new_rank += rank
      else:
        string = f'Unknown value: {rank} passed to reducer_rank_nodes'
        raise Exception(string)

    if abs(new_rank - prev_rank) > self.options.rank_threshold:
      ''''If the rank changed more than the provided threshold, mark it as unconverged.'''
      self.increment_counter('reducer1', 'unconverged_nodes', 1)

    if node_id != 'lost' and includes_node:
      yield node_id, (adj_list, new_rank)


if __name__ == "__main__":
  PageRank.run()