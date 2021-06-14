DOCTYPE = '''<!DOCTYPE html>'''
HEAD = '''
  <head>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald&family=Ubuntu&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://use.typekit.net/oxi4xqh.css">
    <title>QuantBot</title>
    <link rel="shortcut icon" href="resources/favicon.ico">
  </head>
  <body>
'''

NAVBAR = '''
    <div class="nav-bar">
      <a href="QuantBot.io">
      <video disableRemotePlayback autoplay muted loop id="myVideo">
        <source src="resources/logo.mp4" type="video/mp4">
      </video>
    </a>
      <ul class="nav-buttons">
        <li class="button color"><a style = "text-decoration: none; color: inherit" href="#top">Portfolio</a></li>
        <li class="button color "><a style = "text-decoration: none; color: inherit" href="#news">News</a></li>
        <li class="button color"><a style = "text-decoration: none; color: inherit" href="#contact">Contact Us</a></li>
      </ul>
    </div>
'''

SIDEBAR = '''
    <div class="side-bar">
      <p class="holdings">Current Holdings</p>
      <ul class="shares">
'''

def add_sidebar_holding(symbol, qty, price, color, percent):
  return f'''
        <li class="share">
          <ul class="share-details">
            <li ><p style="margin-bottom: -10px; top: -40%;">{symbol}</p><p class="quantity">{qty} Shares</p></li>
            <li class="value"><p class="num">${price}</p><p class="per num" style="color: {color}; font-weight: bold">{percent}%</p></li>
          </ul>
        </li>
  '''

END_SIDEBAR = '''
      </ul>
    </div>
'''
def add_primary_content_body(equity, dailychange, percentchange, graph, buyingpower):
  return f'''
    <div class="body">
      <h1 id="top" class="num">${equity}</h1>
      <h2 class="color num">{dailychange} ({percentchange}%)</h2>
      {graph}
      <div class="buyingpower">
          <p class="buy">Buying Power</p>
          <p class="buy2 num">${buyingpower}</p>
      </div>
  '''

NEWS = '''
    <div class="summary">
      <p class="color" style="font-weight: bold">What is Quantbot?</p>
      <p class="des">QuantBot is a completely automated bot that makes use of artificial intelligence to trade 
        the stock market for its founders, <a class="us" href="https://bergsneider.dev" target="_blank">Alan</a> and 
        <a class="us" href="https://joshcunningham.net" target="_blank">Josh</a>. We've programmed the bot using Python 
        to scrape the web to find data it desires regarding different assets, perform machine learning (both time series 
        and sentiment analyses with price and news data respectively), and finally decide to buy/sell using the Alpaca 
        API and brokerage based on the conclusions of the analyses when compared against each other. This project is 
        being completed over Summer 2021 outside of our professional endeavours, and we are learning all of these concepts
        (web scraping, time series analysis, sentiment analysis / Natural Language Processing, financial reporting, etc) on
        our own from scratch. 
      </p>
    </div>
    <div class="news-head" id="news"><p>News the Bot Used to Buy/Sell</p></div>
      <div class="news">
        <ul class="news-list">
          <li class="article">
            <ul class="inner-article">
              <li>
                <img src="resources/a.png" alt="graph" class="article-img">
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
                <img src="resources/a.png" alt="graph" class="article-img">
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
                <img src="resources/a.png" alt="graph" class="article-img">
              </li>
              <li class="article-words">
                <p class="article-summary color">This article led to the bot buying 15 shares of TSLA.</p>
                <p class="article-p">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Saepe magnam animi voluptatibus qui? Ipsam provident laboriosam cupiditate sapiente expedita. Aspernatur aut accusamus pariatur rerum minima dolorum molestiae ipsa nam nihil!</p>
              </li>
            </ul>
          </li>
        </ul>
      </div>
'''

CONTACT = '''
      <div class="contact color" id="contact">
        <h3 style="margin-bottom: -10px; font-size: 18px;">Contact Us</h3>
        <p style="margin-bottom: -10px; font-size: 15px;">Josh Cunningham || jcun@umich.edu || LinkedIn</p>
        <p style="font-size: 15px">Alan Bergsneider || bera@umich.edu || LinkedIn</p>
      </div>
    </div>
  </body>
'''
