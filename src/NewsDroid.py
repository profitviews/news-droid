from profitview import Link, http, logger, cron
import openai
from openai import OpenAI
import feedparser
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class Signals(Link):
	OPENAI_CLIENT = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
	
	@cron.run(on='1m')
	def check_news(self):
		signal = {'Buy': 1, 'Neutral': 0, 'Sell': -1}[self.predict('Bitcoin')]
		self.signal('bitmex', 'XBTUSD', size=signal)
	
	def predict(self, coin, minutes=2):
		feed = feedparser.parse(f"https://news.google.com/rss/search?q={coin}")
		headlines = []

		# Extract articles
		time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
		for entry in feed.entries:
			published_time = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
			if published_time > time_threshold:
				headlines.append(entry.title)
		if not headlines: return 'Neutral'
	
		google_feed_query = f"""
			Assess this news headline or set of them as it pertains to cryptocurrency {coin}. 
			Provide a single-word recommendation: 'Buy', 'Neutral', or 'Sell'.  
			Provide only the word.

			"""
		google_feed_query += "".join([f"Headline: {headline}\n" for headline in headlines])
		
		logger.info(google_feed_query)
		
		response = self.OPENAI_CLIENT.chat.completions.create(
			model = "gpt-4o-mini",
			response_format={ "type": "text"},
			messages=[
				{"role": "system", 
			 	"content": "You are a cryptocurrency trading expert."}, 
				{"role": "user", "content": google_feed_query}],
				frequency_penalty=0.0)

		prediction = response.choices[0].message.content

		logger.info(f"{prediction=}")
		
		return prediction
