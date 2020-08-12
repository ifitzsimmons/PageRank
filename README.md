# HW2b: PageRank

## Algorithm:
```math
P(n) = \frac{\alpha}{|G|} + (1 - \alpha)\sum\frac{P(m)}{C(m)}
```

### PageRank.py
`PageRank.py` performs the "simple" PageRank algorithm without distribution of lost mass due to dangling nodes and "dampening" (probability that a user will randomly jump from one page to another without following a link):
```math
P(n) = \sum_{m \epsilon L(n)}{\frac{P(m)}{C(m)}}
```
Where $P(n)$ is the rank of the current node, $L(n)$ describes the set of pages that link to $n$, $P(m)$ is the rank of the incoming node and $C(m)$ is the number of links on page $m$.

### MassDistrobution.py

There are some issues with the algorithm defined in the book. One large problem that I found is that, with a smaller number of nodes, as the rankings converge they grow smaller and smaller, and  they start out small enough as is. So, when performing the following function:
```math
p\prime = \frac{\alpha}{|G|} + (1 - \alpha) (\frac{m}{|G|} + p)
```
the result may be dominated by $\frac{\alpha}{|G|}$.

In the above function, $\alpha$ represents the probability that a web surfer will "randomly" jump from one page to the next, $m$ represents the lost mass (sum of the rank of all dangling nodes), $p$ is the rank calculated in step one `PageRank.py`, and $p\prime$ represents the final ranking after lost mass distribution and dampening.


### Questions

1. When are you supposed to remove the dangling nodes? If we redistribute the node mass on each pass, shouldn't we then remove the dangling nodes? But you can't do that, because the calculated `lost` mass won't be too accurate.
2. If the algorithm is iterative and requires two `MRJob` processes, how do we know when a node rank changes? If we calculate the rank in two separate jobs, the only way I could think to do this would be to store the last rank output in memory, and then compare the object written to memory to the output of the 2nd job on each pass, but that is wildly inefficient.

## Code
To run the PageRank algorithm, run the following from the command line in this directory:
```command
$ python PageRankDriver.py <json_file> <rank_change_treshold>
```

The arguments are pretty self explanatory, `rank_change_treshold` is the threshold at which we consider a node to be converged. Increasing the rank threshold will increase the runtime of PageRank.

The `json` file should be in the following format:
```json
node_id<int> \t [adj_list<list<int>>, rank<float>]
```

There is a sample json file in this directory -> `.preprocessed_web-Google.json`. This is a large graph (almost 1 million nodes), and will take some time with small thresholds.

### Sample
```
$ python PageRankDriver.py sample.json 1e-5
```

## Dependencies
To install package dependencies, run the following command from the top-level directory:
```
python setup.py install
```

## Tests
Code coverage is currently limited to `PageRank.py` and does not even full cover that. Test code can be found in the `tests` directory and can be run with the following command from the top level directory:
```
$ python setup.py test
```