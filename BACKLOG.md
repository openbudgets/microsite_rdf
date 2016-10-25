+ build first level query
+ build second level query (n-ary level, it'll be generic enough) to go deeper
  into a city's dimensions
+ build networkX digraph to traverse hierarchy
- extend the graph to add transactions as new nodes, connected to their
  respective dimensions and labeled as transactions to differentiate them from
  dimensions
- get to the transactions (observations) level, somehow
- build middleware to handle requests from the webapp through the scripts that
  execute SPARQL queries
    + build "deeper" dimensions route in flask app
- build web application to navigate the levels
    - add city selector
