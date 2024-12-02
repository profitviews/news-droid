# News Bot

Use news interpretation as trading signal

The first version is a simple bot that uses news headlines as trading signal.

The process is as follows:

1. Get the news headlines
2. Use a pre-trained model to interpret the news headlines
3. Generate trading signals based on the news interpretation
4. Provide a signal.  It can be consumed by a trading algorithm or sent to other consumers

Possible improvements:
1. Get news from more sources
2. Get news story text
3. Use more sophisticated models to interpret the news
4. Use more sophisticated models to generate trading signals
5. Backtest the signal
6. Tune the signal

## First implementation

### Getting Headlines

Headlines are retrieved from the NewsAPI using the `newsapi` Python package.

### Interpreting Headlines

An OpenAI API call is used to interpret the headlines.

### Generating Signals

A simple prompt will be used to provide a Buy, Sell, or Hold signal.

