from profitview import Link, logger, cron
from openai import OpenAI
from dotenv import load_dotenv
import feedparser
import os

load_dotenv()

class Signals(Link):
  OPENAI_CLIENT = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
  
  @cron.run(on='1m')
  def check_news(self):
    self.signal('bitmex', 'XBTUSD', size=self.predict('Bitcoin'))
  
  def predict(self, coin):
    feed = feedparser.parse(
      f"https://news.google.com/rss/search?q={coin}&tbs=qdr:h")

    google_feed_query = f"""
      Assess these news headlines as they pertain to 
      cryptocurrency {coin}, taking into account their publication 
      date and time for relevance. Provide a single floating point 
      number between -1.0 and 1.0, with -1.0 signifying extreme 
      negativity, 0.0 neutrality and 1.0 extreme positivity.
      Provide only the number and no other text.

      """

    google_feed_query += "".join([
      f"""Published: {entry.published}. Headline: {entry.title}
      """ for entry in feed.entries])
    
    response = self.OPENAI_CLIENT.chat.completions.create(
      model = "gpt-4o-mini",
      response_format={ "type": "text"},
      messages=[{"role": "system", 
                 "content": "You are a cryptocurrency trading expert."}, 
                {"role": "user",   "content": google_feed_query}])

    prediction = float(response.choices[0].message.content)

    logger.info(f"{prediction=}")
    
    return prediction