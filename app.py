from flask import Flask, render_template
from rdf_utils.obeu_graph import OBEUGraph

app = Flask(__name__)
app.debug = True


@app.route('/<city>/<year>')
def index(city, year):
    """
    Shows visualizations of a *city* in a particular *year*, given that the
    corresponding dataset is loaded inside the SPARQL server
    :param city: name of the city as it appears in the dataset
    :param year: corresponding year to be used as filter
    :return: render_template() answer
    """
    g = OBEUGraph()
    # g.add_obeu_dimension_edges(
    #     city=city,
    #     year=year,
    #     query_file='/home/piero/Documents/fraunhofer/obeu-explorer/rdf_utils/queries/'
    #                'exploring.rq')
    g.add_obeu_observation_edges(
        city=city,
        year=year,
        query_file='/home/piero/Documents/fraunhofer/obeu-explorer/rdf_utils/'
                   'queries/all-about-observations-from-city-in-a-year.rq')
    data = {'nodes': [], 'edges': []}

    # add node data as needed by visjs to help us show some useful graphics
    for node_id in g.node:
        data['nodes'].append({
            'id': node_id,
            'label': g.node[node_id]['label'],
            'title': 'Name: {} <br> Amount (€): {}'
                .format(g.node[node_id]['label'], g.node[node_id]['amount']),
            'group': g.node[node_id]['group']
        })

    # add special format for edges used by visjs
    # exm: [{from: 1, to: 10}, {from: 2, to: 12]
    for edge in g.edges():
        data['edges'].append({'from': edge[0], 'to': edge[1]})

    return render_template('layouts/city_year_graph.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
