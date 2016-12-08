from itertools import islice
import networkx as nx
from rdf_utils.stm import STM


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
        group = {}
        next_group = 0
        response = STM.get_data(query_file, [city, year])

        for elem in response['results']['bindings']:
            amount = elem['amount']['value']
            observation = elem['observation']['value']
            abstract_class = elem['abstract_class']['value']
            concrete_class = elem['concrete_class']['value']

            # parse labels
            try:
                abstract_class_label = elem['abstract_class_label']['value']
            except KeyError:
                abstract_class_label = abstract_class
            try:
                concrete_class_label = ''# elem['concrete_class_label']['value']
                concrete_class_prefLabel = elem['concrete_class_prefLabel']['value']
            except KeyError:
                concrete_class_label = concrete_class
                concrete_class_prefLabel = concrete_class

            self.add_edge(abstract_class, concrete_class)
            self.add_edge(concrete_class, observation)

            if group.get(abstract_class) is None:
                group[abstract_class] = next_group
                next_group += 1

            self.node[abstract_class]['group'] = abstract_class
            self.node[abstract_class]['label'] = abstract_class_label
            self.node[concrete_class]['group'] = abstract_class
            self.node[concrete_class]['label'] = concrete_class_prefLabel
            self.node[observation]['group'] = 'observation'
            self.node[observation]['label'] = observation
            self.node[observation]['amount'] = float(amount)
            if self.node[concrete_class].get('amount'):
                self.node[concrete_class]['amount'] += \
                    self.node[observation]['amount']
            else:
                self.node[concrete_class]['amount'] = \
                    self.node[observation]['amount']
            if self.node[abstract_class].get('amount'):
                self.node[abstract_class]['amount'] += \
                    self.node[concrete_class]['amount']
            else:
                self.node[abstract_class]['amount'] = \
                    self.node[concrete_class]['amount']

        # trick to restrict the amount of shown observations to only 20
        selected_observations = \
            islice(filter(lambda x: self.node[x]['group'] == 'observation',
                          self.nodes_iter()),
                   None, 20)

        for observation in selected_observations:
            self.node[observation]['group'] = 'selected_observations'

    def add_obeu_dimension_edges(self, city, year, query_file):
        """
        Query the SPARQL Template Manager (STM) to add required edges to the
        graph
        :param city: (string) city name
        :param year: (string) year to be used as filter
        :param query_file: (string) name of the file containing the SPARQL query
                           to be used
        :return: None
        """
        response = STM.get_data(query_file, [city, year])

        # add edge from u to v if u is a broader property of v or v is a
        # narrower property of u

        for elem in response['results']['bindings']:
            broader = elem['broader']['value']
            narrower = elem['narrower']['value']
            self.add_edge(broader, narrower)
            self.node[broader]['label'] = broader
            self.node[broader]['group'] = 'not specified'
            self.node[broader]['amount'] = 0 if self.node[broader].get(
                'amount') is None else self.node[broader]['amount']
            self.node[narrower]['label'] = narrower
            self.node[narrower]['group'] = 'not specified'
            self.node[narrower]['amount'] = 0 if self.node[narrower].get(
                'amount') is None else self.node[narrower]['amount']



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

    # nx.draw(g)
    # plt.savefig('observations-hierarchy-graph.png')
    # plt.show()

    g2 = OBEUGraph()
    g2.add_obeu_observation_edges(
        city='Aragon',
        year='2015',
        query_file='queries/exploring.rq')

    g3 = OBEUGraph()
    g3.add_obeu_observation_edges(
        city='Aragon',
        year='2015',
        query_file='queries/exploring2.rq')

    pass  # this is not a mistake, here goes a breakpoint in PyCharm ;)
