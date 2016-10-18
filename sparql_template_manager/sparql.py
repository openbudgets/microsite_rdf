import re
import sys
import json
import urllib
import requests


class STM(object):
    @staticmethod
    def get_subject(elem):
        return elem['s']['value']

    @staticmethod
    def get_predicate(elem):
        return elem['p']['value']

    @staticmethod
    def get_object(elem):
        return elem['o']['value']

    @staticmethod
    def collect_amounts(_list):
        return \
            [
                (STM.get_subject(elem), STM.get_predicate(elem),
                 STM.get_object(elem))
                for elem in _list
            ]

    @staticmethod
    def pretty_print(result):
        print(json.dumps(result, indent=2, sort_keys=True))

    @staticmethod
    def execute_query(query):
        """
        Take a SPARQL query and execute it against the HTTP SPARQL endpoint
        :param query: valid SPARQL query
        :return: json-ified response from the server or None if there were errors
                 handling the request
        """
        query = urllib.parse.quote_plus(query)
        #api = 'http://eis-openbudgets.iais.fraunhofer.de/fuseki/sparql?query=%s'
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
        sparql_query = ''.join(open(filename, 'r').readlines())

        if vars_list:
            sparql_query = STM.insert_variables(sparql_query, vars_list)

        print(sparql_query)
        output = STM.execute_query(sparql_query)
        STM.pretty_print(output)
        return output

    @staticmethod
    def predicates_list(response):
        try:
            return [STM.get_predicate(e)
                    for e in response['results']['bindings']]
        except TypeError:
            return []

    @staticmethod
    def next_link(city, dimension):
        return 'http://localhost:5000/{city}/{dimension}'\
            .format(city=city.replace('"', ''),
                    dimension='<{}>'.format(dimension))


if __name__ == '__main__':
    STM.get_data(sys.argv[1], sys.argv[2:])
