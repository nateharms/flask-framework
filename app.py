from flask import Flask, render_template, request, redirect
from alpha_vantage.timeseries import TimeSeries
import matplotlib
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if (request.method == 'POST') and (request.form.get('ticker', '') != ''):
    return ticker()
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

def plot_ticker(ticker_index, opening, closing, adj_closing):
  """
  A function to create a plot of the 
  """
  ts = TimeSeries(key='2HJW48VQJPVUPP5L')
  opening_data = []
  closing_data = []
  adj_closing_data = []
  dates = []
  if not any([opening, closing, adj_closing]):
    closing = True 
    # Setting closing to be true in the case that a 
    # user doesn't specify any.
  adj_daily_ticker_data, *_ = ts.get_daily_adjusted(ticker_index.upper())

  df = pd.DataFrame(adj_daily_ticker_data).T
  df.index = pd.to_datetime(df.index, format = "%Y-%m-%d")

  #output_file("lines.html")
  p = figure(title=f"Stock Prices for {ticker_index.upper()}", x_axis_label='Date', y_axis_label='Stock Price (USD)', x_axis_type="datetime")
  
  # add a line renderer with legend and line thickness
  if opening:
    p.line(df.index, df['1. open'], legend_label="Opening Price", line_width=2, color='red')
  if closing:
    p.line(df.index, df['4. close'], legend_label="Closing Price", line_width=2, color='blue')
  if adj_closing:
    p.line(df.index, df['5. asjusted close'], legend_label="Adjusted Closing Price", line_width=2, color='green')
  #show(p)
  return components(p)

if __name__ == '__main__':app.run(port=33507)
