from flask import Flask, render_template
import json
import plotly
import pandas as pd
import numpy as np
from rdf_utils.stm import STM

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    # query SPARQL endpoint and build a list of data
    data = STM.get_data('rdf_utils/predicates-of-subjects-related-to-amounts.rq')
    x = [e[0] for e in data]
    y = [float(e[1]) for e in data]

    graphs = [
        dict(
            data=[
                dict(
                    labels=x,
                    values=y,
                    type='pie'
                ),
            ],
            layout=dict(
                title='second graph'
            )
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layouts/old-index.html',
                           ids=ids,
                           graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
