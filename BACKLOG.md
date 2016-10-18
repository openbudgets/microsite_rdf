+ build first level query
+ build second level query (n-ary level, it'll be generic enough) to go deeper
  into a city's dimensions
- build networkX digraph to traverse hierarchy
    - build graph
    - find root nodes
    - start traversing somehow with each HTTP request
- check why all "specific dimensions" queries return empty stuff. There's
  something useful in exploring.rq
- build middleware to handle requests from the webapp through the scripts that
  execute SPARQL queries
    + build "deeper" dimensions route in flask app
- build web application to navigate the levels
    - add city selector
- get to the transactions (observations) level, somehow
