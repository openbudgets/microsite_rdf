from flask import Flask, render_template
from rdf_utils.stm import STM
from rdf_utils.obeu_graph import OBEUGraph
from utils import double_quote, next_link

app = Flask(__name__)
app.debug = True


@app.route('/<city>/<year>')
def index(city, year):
    g = OBEUGraph()
    g.add_obeu_observation_edges(
        city=city,
        year=year,
        query_file='/home/piero/Documents/fraunhofer/obeu-explorer/rdf_utils/queries/'
                   'all-about-observations-from-city-in-a-year.rq')
    data = {'nodes': [], 'edges': []}

    for node_id in g.node:
        data['nodes'].append({
            'id': node_id,
            'label': '',  # is it sane to use the URI (node_id) as label?
            'title': 'Amount (€): {}'.format(g.node[node_id]['amount']),
            'group': g.node[node_id]['group']
        })

    for edge in g.edges():
        data['edges'].append({'from': edge[0], 'to': edge[1]})

    return render_template('layouts/city_year_graph.html', data=data)


@app.route('/old-index')
def old_index():
    city = double_quote('aragon')
    resp = STM.get_data('rdf_utils/queries/top-dimensions-of-city.rq', [city])
    dimensions = STM.predicates_list(resp)
    links = [next_link(city, d) for d in dimensions]
    return render_template('layouts/index.html',
                           data=[
                               {'uri': uri, 'next_link': next_link}
                               for uri, next_link in zip(dimensions, links)
                               ]
                           )


@app.route('/<city>/<path:dimension>')
def specific_dimension(city, dimension):
    city = double_quote(city)
    resp = STM.get_data('rdf_utils/queries/specific-dimensions.rq',
                        [dimension, city, dimension, city])
    dimensions = STM.predicates_list(resp)

    # we got to the deepest level in this classification tree, let's show
    # transactions (observations) right away!
    if not dimensions:
        print(dimensions)
        return render_template('layouts/error.html',
                               data={'error': 'Transactions data coming soon!'})

    # we still have some more nodes to explore
    links = [next_link(city, double_quote(d)) for d in dimensions]
    return render_template('layouts/index.html',
                           data=[
                               {'uri': uri, 'next_link': next_link}
                               for uri, next_link in zip(dimensions, links)
                               ]
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
