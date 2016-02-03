from flask import Flask, render_template
import plotly
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF


import json

import pandas as pd
import numpy as np

app = Flask(__name__)
app.debug = True

df = pd.read_csv("data/bank.csv", sep=";")

res = pd.DataFrame({"Relative score":[100,85,73,70,60], "Predictor":["marital","education","job","balance","loan"] })

table = FF.create_table(res)

@app.route('/')
def index():

    churn = [Scatter(x=range(4), y=[10,11,12,13], mode="markers", marker=dict(size=[40,60,80,100]), name = "High CLV")
      ,Scatter(x=range(4), y=[13.4,9,7,5], mode="markers", marker=dict(size=[50,70,90,110]), name = "Medium CLV")
      ,Scatter(x=range(4), y=[8,11,10,7], mode="markers", marker=dict(size=[30,40,50,60]), name = "Low CLV")
      ]


    ## Histograms of 'important' variables

    marital = [Histogram(x=np.array(df.query('y=="yes"').ix[:,'marital']), name='Took loan'),
            Histogram(x=np.array(df.query('y=="no"').ix[:,'marital']), name='Rejected loan')]

    education = [Histogram(x=np.array(df.query('y=="yes"').ix[:,'education']), name='Took loan'),
            Histogram(x=np.array(df.query('y=="no"').ix[:,'education']), name='Rejected loan')]

    job = [Histogram(x=np.array(df.query('y=="yes"').ix[:,'job']), name='Took loan'),
            Histogram(x=np.array(df.query('y=="no"').ix[:,'job']), name='Rejected loan')]


    ids = ["churn","table","marital","education","job"]
    graphs = [churn,table,marital,education,job]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layouts/index.html',ids=ids,graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
