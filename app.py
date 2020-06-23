from flask import Flask, render_template, request, redirect
from alpha_vantage.timeseries import TimeSeries
import matplotlib
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/ticker', methods=['GET', 'POST'])
def ticker():
  bool_dict = {
    'on':True,
    'off':False
  }
  ticker_index = request.form.get('ticker').upper()
  opening = bool_dict[request.form.get('opening', 'off')]
  closing = bool_dict[request.form.get('closing', 'off')]
  adj_closing = bool_dict[request.form.get('adj-closing', 'off')]
  try:
    script, div = plot_ticker(
      ticker_index=ticker_index,
      opening=opening,
      closing=closing,
      adj_closing=adj_closing,
    )
  except:
    return redirect('/')
  return render_template('ticker.html', 
    ticker=request.form.get('ticker'),
    script = script,
    div = div
    )

if __name__ == '__main__':
  app.run(port=33507)
