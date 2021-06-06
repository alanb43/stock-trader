from alpaca_trade_api.rest import Positions
from trader import *
import time
import matplotlib.pyplot as plt # side-stepping mpl backend
import numpy as np
import plotly.graph_objects as go
from webpage import constants
from datetime import date, datetime


class Stock:
  '''
  
  Stock object to store key information regarding a stock for the purpose of
  supplying QuantBot.io with correct info. Used with WebpageDataRefresher. 

  '''
  def __init__(self, symbol, qty, current_price, lastday_price, market_value, 
            unrealized_intraday_pl, unrealized_intraday_plpc) -> None:
    self.symbol = symbol
    self.qty = qty
    self.current_price = current_price
    self.lastday_price = lastday_price
    self.market_value = market_value
    self.intraday_pl = unrealized_intraday_pl
    self.intraday_plpc = unrealized_intraday_plpc


  def __str__(self):
    ''' Returns a paragraph blurb listing all of the data the object holds. '''
    string = f'''{self.symbol}\nQty: {self.qty}\nCurrent Price: {self.current_price}\n'''
    string += f'''Yesterday's Close: {self.lastday_price}\nMarket Value: {self.market_value}\n'''
    string += f'''Today's P/L: {self.intraday_pl}\nToday's P/L % Change: {self.intraday_plpc}\n'''
    return string


  def __lt__(self, other_stock):
    ''' Overloaded less than operator, for alphabetical sorting of stocks based on symbol '''
    return self.symbol < other_stock.symbol


class WebpageDataRefresher:
  '''

  Webpage Data Refresher tool to supply QuantBot.io with latest information regarding
  equities, positions, profits & losses, and more. Generally returns tuples containing
  the float for a particular case and it's formatted string.

  NOTE: initializing an instance connects us to the api and sets class up with account
        and positions info
  NOTE: functionality for sidebar refreshing needs to be added
  NOTE: this class can / maybe will be used in conjunction with a server that runs it
        to update the site periodically

  '''
  def __init__(self) -> None:
    self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')
    self.account = self.api.get_account()
    self.positions = self.api.list_positions()


  def __number_float_to_string(self, float) -> str:
    ''' Turns a float into a formatted string '''
    return f'{float :,.2f}'


  def __format_dollars_to_string(self, float) -> str:
    ''' Formats a dollar string with dollar signs and direction '''
    string = self.__number_float_to_string(float)
    if str(float)[0] == '-':
      return "-$" + string[1:]
    return "+$" + string


  def __format_percentage_to_string(self, percentage) -> str:
    ''' Formats a percentage string with direction '''
    if percentage >= 0:
      return '+' + self.__number_float_to_string(percentage)
    return '-' + self.__number_float_to_string(percentage)


  def get_equity(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for account equity and
    a formatted string of this value.
    '''
    return tuple((float(self.account.equity), self.__number_float_to_string(float(self.account.equity))))


  def get_buying_power(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for buying power and a
    formatted string of this value.
    '''
    buying_power = float(self.account.buying_power)
    return tuple((buying_power, self.__number_float_to_string(buying_power)))  


  def __get_account_positions(self) -> list:
    '''
    Goes through positions received from Alpaca, initializes Stock objects with
    relevant info, adds them to an array which is eventually returned.
    '''
    positions = self.positions
    stock_array = []
    for position in positions:
      stock_array.append(
        Stock(
          position.symbol, position.qty, position.current_price, 
          position.lastday_price, position.market_value, 
          position.unrealized_intraday_pl, position.unrealized_intraday_plpc
        )
      )
    return stock_array


  def get_account_daily_change(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for the account's daily change 
    and a formatted string of this value.
    '''
    daily_change = 0
    positions = self.__get_account_positions()
    for position in positions:
      daily_change += float(position.intraday_pl)

    return tuple((daily_change, self.__format_dollars_to_string(daily_change)))


  def get_account_percent_change(self) -> tuple((float, str)):
    '''
    Returns a tuple containing the float value for the account's daily percent 
    change and a formatted string of this value.
    '''
    percent_change = 0
    positions = self.__get_account_positions()
    equity = (self.get_equity())[0]
    for position in positions:
      percent_change += float( position.intraday_plpc ) * ( ( float(position.market_value) * float(position.qty) ) / equity )

    return tuple((percent_change, self.__format_percentage_to_string(percent_change)))

  
  def print_stock_price_alphabetical(self):
    ''' for debugging, so you can see what your handling '''
    positions = self.__get_account_positions()
    for position in sorted(positions):
      print(position)


  def get_position_colors(self) -> dict:
    positions = self.__get_account_positions()
    colors = {}
    for x in range(len(positions)):
      if float(positions[x].intraday_plpc) >= 0:
        colors[positions[x].symbol] = "green"
      else:
        colors[positions[x].symbol] = "red"
    return colors


  def __convert_timestamps(self) -> list:
    timestamps = self.api.get_portfolio_history(date_start=None, date_end=None, period="1D", timeframe="5Min", extended_hours=None).timestamp
    dt_array = []
    for stamp in timestamps:
      dt = datetime.fromtimestamp(stamp)
      dt = str(dt)[11:-3]
      dt_array.append(dt)
    return dt_array

  
  def create_plot_html(self) -> str:
    equity_data = self.api.get_portfolio_history(date_start=None, date_end=None, period="1D", timeframe="5Min", extended_hours=None).equity
    dt_data = self.__convert_timestamps()
    fig = go.Figure([go.Scatter(x=dt_data, y=equity_data, line=dict(color="yellow"))])
    fig.layout.xaxis.color = 'yellow'
    fig.layout.yaxis.visible = False
    fig.layout.paper_bgcolor = 'rgba(0, 0, 0, 0)'
    fig.layout.plot_bgcolor='black'
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_layout(
      xaxis = dict(
          dtick = 12
      )
    )
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    with open('./webpage/graph.html', 'w') as f:
      f.write(fig.to_html(include_plotlyjs='cdn', default_width="90%", config={"displayModeBar": False}))
    with open('./webpage/graph.html', 'r') as graph:
      graph.readline()
      graph.readline()
      graph.readline()
      graph_div = graph.readline()
      graph_div += graph.readline()
    return graph_div
  

  def create_site_html(self) -> str:
    graph_div = self.create_plot_html()
    with open("webpage/index.html", "w") as html_file:
      html_top = constants.TOP_OF_PAGE
      html_file.write(html_top)
      positions = self.__get_account_positions()
      for x in range(len(positions)):
        price = "{:,.2f}".format(float(positions[x].current_price))
        percent = "{:.2f}".format(float(positions[x].intraday_plpc) * 100)
        html_content = f"""        
            <li class="share">
              <ul class="share-details">
                <li>{positions[x].symbol}</li>
                <li class="value"><p>${price}</p><p class="per" style="color: {self.get_position_colors()[positions[x].symbol]}; font-weight: bold">{percent}%</p></li>
              </ul>
            </li> """
        html_file.write(html_content)

      html_content = f"""
          </ul>
        </div>
        <div class="body">
          <h1 id="top">${self.get_equity()[1]}</h1>
          <h2 class="color">{self.get_account_daily_change()[1]} ({self.get_account_percent_change()[1]}%) Today</h2>
          {graph_div}
          <div class="buyingpower">
              <p class="buy">Buying Power</p>
              <p class="buy2">${self.get_buying_power()[1]}</p>
          </div>
          <div class="summary">
            <p class="color">What is Quantbot?</p>
            <p class="des">Quantbot is a Python Bot that utilizes a combination of machine learning, time analysis, and sentiment analysis to automatically buy and sell stocks. The bot uses a web scraper that periodically checks for new articles regarding a company and analyzes the content in the article. If the bot deems the article particularly positive or negative for that company, the bot will either buy or sell the shares we have.</p>
          </div>
          <div class="news-head" id="news"><p>News the Bot Used to Buy/Sell</p></div>
          <div class="news">
            <ul class="news-list">
              <li class="article">
                <ul class="inner-article">
                  <li>
                    <img src="a.png" alt="graph" class="article-img">
                  </li>
                  <li class="article-words">
                    <p class="article-summary color">This article led to the bot buying 10 shares of AAPL.</p>
                    <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
                  </li>
                </ul>
              </li>
              <li class="article">
                <ul class="inner-article">
                  <li>
                    <img src="a.png" alt="graph" class="article-img">
                  </li>
                  <li class="article-words">
                    <p class="article-summary color">This article led to the bot selling 20 shares of GOOGL.</p>
                    <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
                  </li>
                </ul>
              </li>
              <li class="article">
                <ul class="inner-article">
                  <li>
                    <img src="a.png" alt="graph" class="article-img">
                  </li>
                  <li class="article-words">
                    <p class="article-summary color">This article led to the bot buying 15 shares of TSLA.</p>
                    <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        """
      html_file.write(html_content)
      html_file.write(constants.BOTTOM_OF_PAGE)

WDR = WebpageDataRefresher()
WDR.create_site_html()
# WDR.print_stock_price_alphabetical()



