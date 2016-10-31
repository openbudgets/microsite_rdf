import networkx as nx
from stm import STM


class OBEUGraph(nx.DiGraph):
    def add_obeu_observation_edges(self, city, year, query_file):
        """
        Query the SPARQL Template Manager (STM) to add required edges to the
        graph
        Two types of edges will be added:
            - Edge (u, v) := u is the abstract class of the concrete class v
            - Edge (v, w) := v is a concrete classification of observation w

        :param city: (string) city name
        :param year: (string) stringified number representing the year to query
        :param query_file: (string) name of the file containing the SPARQL query
                           to be used
        :return: None
        """
        amounts = {}
        response = STM.get_data(query_file, [city, year])

        for elem in response['results']['bindings']:
            self.add_edge(elem['abstract_class']['value'],
                          elem['concrete_class']['value'])
            self.add_edge(elem['concrete_class']['value'],
                          elem['observation']['value'])

            self.node[elem['observation']['value']]['amount'] = \
                float(elem['amount']['value'])

    def add_obeu_dimension_edges(self, city, query_file):
        """
        Query the SPARQL Template Manager (STM) to add required edges to the
        graph
        :param city: (string) city name
        :param query_file: (string) name of the file containing the SPARQL query
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
    g.add_obeu_observation_edges(
        city='Aragon',
        year='2015',
        query_file='queries/all-about-observations-from-city-in-a-year.rq')
    # get graph roots because they're top level dimensions of this city
    top_dimensions = g.root_nodes()
    pass  # this is not a mistake, here goes a breakpoint in PyCharm ;)
