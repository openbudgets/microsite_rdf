from flask import Flask, render_template
from rdf_utils.stm import STM

app = Flask(__name__)
app.debug = True


def double_quote(string):
    return '"{}"'.format(string)


@app.route('/')
def index():
    city = double_quote('aragon')
    resp = STM.get_data('rdf_utils/queries/top-dimensions-of-city.rq', [city])
    dimensions = STM.predicates_list(resp)
    links = [STM.next_link(city, d) for d in dimensions]
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
    links = [STM.next_link(city, double_quote(d)) for d in dimensions]
    return render_template('layouts/index.html',
                           data=[
                               {'uri': uri, 'next_link': next_link}
                               for uri, next_link in zip(dimensions, links)
                               ]
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
