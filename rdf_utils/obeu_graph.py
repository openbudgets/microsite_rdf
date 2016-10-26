import networkx as nx
from stm import STM


class OBEUGraph(nx.DiGraph):
    def add_obeu_edges(self, city, query_file):
        """
        Query the SPARQL Template Manager (STM) to add required edges to the
        graph
        :param city: (string) city name
        :param query_file: (string) name of the file containng the SPARQL query
                           to be used
        :return: None
        """
        self.city = '"{}"'.format(city)
        response = STM.get_data(query_file, [self.city, self.city])

        # add edge from u to v if u is a broader property of v or v is a
        # narrower property of u

        for elem in response['results']['bindings']:
            if 'broader' in elem['p']['value']:
                self.add_edge(elem['dim']['value'], elem['s']['value'])
            elif 'narrower' in elem['p']['value']:
                self.add_edge(elem['s']['value'], elem['dim']['value'])

    def root_nodes_gen(self):
        """
        Find root nodes of the graph
        :return: generator yielding root nodes of the graph
        """
        return (node
                for node, in_degree in self.in_degree().items()
                if in_degree == 0)

    def root_nodes(self):
        """
        Find root nodes of the graph
        :return: list containing root nodes
        """
        return list(self.root_nodes_gen())


if __name__ == '__main__':
    g = OBEUGraph()
    g.add_obeu_edges(city='bonn', query_file='queries/dimensions-of-city.rq')
    # get graph roots because they're top level dimensions of this city
    top_dimensions = g.root_nodes()
    pass
