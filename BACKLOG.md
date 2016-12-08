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
+ color things differently (one color for each abstract classification)
+ add labels to the graph presented, trying in this order rdfs:label,
  skos:prefLabel, skos:altLabel and, finally, the URI if all the others fail
- join query in exploring.rq with the obeu-graph thing, this way we can build
  the hierarchy using the function of obeu-edges-dimensions
- check why some nodes are lost when adding labels
- build web application to navigate the levels
    + add city selector (URL)
    + add year selector (URL)
    - improve city selector (some HTML element perhaps?)
    - improve year selector
- when one of those classes is clicked it could add nodes of observations
  corresponding to that particular class
