# News Droid

This is a project to experiment with different methods of getting news sentiment for a given coin and to trade on that sentiment.

It is assoaciated with a [Blog post on ProfitView](https://profitviews.net/blog/what-i-learned-when-building-an-ai-news-trading-bot).  You can [sign-up there](https://profitview.net/register) to run a bot that trades using news sentiment.

## Experiment

I've created a [Jupyter notebook](src/experiment.ipynb) to experiment with different methods of getting news sentiment for a given coin.

To run the notebook, use your prefered Python environment.  I recommend using [JupyterLab](https://jupyter.org/install) or [VSCode](https://code.visualstudio.com/download).

You will probably set up a virtual environment; I recommend using [PyEnv](https://github.com/pyenv/pyenv) to manage your Python versions.  In your virtual environment, install the required packages - use `src/requirements.txt` via `pip install -r requirements.txt`.

## Trading Bot

I've created a [Trading Bot](src/NewsDroid.py) that uses the news sentiment to trade on.  This runs on the [ProfitView platform](https://profitview.net/).

