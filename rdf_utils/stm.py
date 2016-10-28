import re
import sys
import json
import urllib
import requests


class STM(object):  # SPARQL Template Manager
    @staticmethod
    def get_predicate(elem, predicate):
        return elem[predicate]['value']

    @staticmethod
    def pretty_print(result):
        print(json.dumps(result, indent=2, sort_keys=True))

    @staticmethod
    def parse_response(response, s, p, o):
        """
        Parse response from get_data() into dictionaries of triples
        :param response: response from method get_data
        :param s: (string) variable used as subject in the query
        :param p: (string) variable used as predicate in the query
        :param o: (string) variable used as object in the query
        :return: list of dictionaries containing all triples inside the response
        """
        return list(STM.parse_response_gen(response, s, p, o))

    @staticmethod
    def parse_response_gen(response, s, p, o):
        """
        Parse response from get_data() into dictionaries of triples
        :param response: response from method get_data
        :param s: (string) variable used as subject in the query
        :param p: (string) variable used as predicate in the query
        :param o: (string) variable used as object in the query
        :return: generator producing dictionaries containing all triples inside
                 the response
        """
        return (
            {s: elem[s]['value'],
             p: elem[p]['value'],
             o: elem[o]['value']
             }
            for elem in response['results']['bindings']
        )

    @staticmethod
    def execute_query(query):
        """
        Take a SPARQL query and execute it against the HTTP SPARQL endpoint
        :param query: valid SPARQL query
        :return: json-ified response from the server or None if there were
                 errors handling the request
        """
        query = urllib.parse.quote_plus(query)
        # api = \
        #     'http://eis-openbudgets.iais.fraunhofer.de/fuseki/sparql?query=%s'
        api = 'http://eis-openbudgets.iais.fraunhofer.de/virtuoso/sparql?' \
              'format=json&query=%s'
        response = requests.get(api % query)
        # print(response.content)
        return response.json() if response else None

    @staticmethod
    def insert_variables(query, vars_list):
        """
        Take a query string with template tags like {% variable %} and substitute
        those tags with the strings contained insito vars_list
        :param query: string with template tags
        :param vars_list: list of strings representing variables' names
        :return: query with template tags replaced with variable names.
                 Ex: query = 'SELECT ?s WHERE { ?s {% predicate %} {% object %}'
                     vars_list = ['skos:broader', 'someObject']
                     return = 'SELECT ?s WHERE { ?s skos:broader someObject'
        """
        result = str(query)

        for var in vars_list:
            result = re.sub(r'{%.*?%}', var, result, 1)
        return result

    @staticmethod
    def get_data(filename, vars_list=None):
        """
        Take the string from an .rq file, insert variables where the template
        tags are located and get the result of executing this completed query
        :param filename: (string) name of the .rq file containing a SPARQL query
                         with template tags to be substituted
        :param vars_list: ([strings]) list of variables names to be inserted
                          into the query
        :return: dictionary with results
        """
        sparql_query = ''.join(open(filename, 'r').readlines())

        if vars_list:
            sparql_query = STM.insert_variables(sparql_query, vars_list)

        print(sparql_query)
        output = STM.execute_query(sparql_query)
        # STM.pretty_print(output)
        return output

    @staticmethod
    def predicates_list(response):
        """
        Grab all predicates indicated by 'p' in the response
        :param response: result of a call to the get_data method
        :return: list of predicates
        """
        try:
            return [STM.get_predicate(e, 'p')
                    for e in response['results']['bindings']]
        except TypeError:
            return []


if __name__ == '__main__':
    output = STM.get_data(sys.argv[1], sys.argv[2:])
    STM.pretty_print(output)
