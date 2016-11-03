+ build first level query
+ build second level query (n-ary level, it'll be generic enough) to go deeper
  into a city's dimensions
+ build networkX digraph to traverse hierarchy
+ extend the graph:
  + add transactions as new nodes
  + label them as transactions to differentiate them from dimensions
  + connect them to their respective dimensions
+ build "deeper" dimensions route in flask app
+ aggregate amounts on concrete classes and propagate to abstract classes
+ plot something with visjs
+ only load classes nodes
- when one of those classes is clicked it could add nodes of observations
  corresponding to that particular class
- color things differently (one color for each category, maybe based on some
  classification the user selects? for exm, the adm classification is selected,
  then everything takes a diff color, depending on its category in that class)
- build web application to navigate the levels
    - add city selector
    - add year selector
