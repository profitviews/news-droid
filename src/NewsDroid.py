from profitview import Link, http, logger, cron
from openai import OpenAI
from datetime import datetime, timedelta
from dotenv import load_dotenv
import feedparser
import os

load_dotenv()


class Signals(Link):
	OPENAI_CLIENT = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
	
	@cron.run(on='1m')
	def check_news(self):
		signal = {'Buy': 1, 'Neutral': 0, 'Sell': -1}[self.predict('Bitcoin')]
		self.signal('bitmex', 'XBTUSD', size=signal)
	
	def predict(self, coin, minutes=2):
		feed = feedparser.parse(f"https://news.google.com/rss/search?q={coin}&tbs=qdr:h")

		google_feed_query = f"""
			Assess these news headlines as they pertain to cryptocurrency {coin},
			taking into account their publication date and time for relevance. 
			Provide a single-word recommendation: 'Buy', 'Neutral', or 'Sell'.  
			Provide only the word.

			"""
		google_feed_query += "".join([f"Published: {entry.published}. Headline: {entry.title}\n" for entry in feed.entries])
		
		response = self.OPENAI_CLIENT.chat.completions.create(
			model = "gpt-4o-mini",
			response_format={ "type": "text"},
			messages=[{"role": "system", "content": "You are a cryptocurrency trading expert."}, 
					  {"role": "user",   "content": google_feed_query}])

		prediction = response.choices[0].message.content

		logger.info(f"{prediction=}")
		
		return prediction
