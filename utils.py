def double_quote(string):
    return '"{}"'.format(string)


def next_link(city, dimension):
    """
    Produce a valid link to get deeper into the hierarchy of a city's
    dimensions
    :param city: (string) name of the city
    :param dimension: (string) URI of a dimension of the city
    :return: (string) a link for redirection purposes
    """
    return 'http://localhost:5000/{city}/{dimension}' \
        .format(city=city.replace('"', ''),
                dimension='<{}>'.format(dimension))