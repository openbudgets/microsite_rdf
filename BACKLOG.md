+ build first level query
+ build second level query (n-ary level, it'll be generic enough) to go deeper
  into a city's dimensions
+ build networkX digraph to traverse hierarchy
+ extend the graph:
  + add transactions as new nodes
  + label them as transactions to differentiate them from dimensions
  + connect them to their respective dimensions
+ build "deeper" dimensions route in flask app
- build web application to navigate the levels
    - add city selector
