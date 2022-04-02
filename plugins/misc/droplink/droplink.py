from pyrogram import Client, filters
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

bot = Client('droplink',
             api_id=API_ID,
             api_hash="API_HASH",
             bot_token='BOT_TOKEN',
             workers=50,
             sleep_threshold=10)

@bot.on_message(filters.command('start') & filters.private)
def start(bot, message):
    message.reply_text("Hello")

@bot.on_message(filters.command('link') & filters.private)
def start(bot, message):
# droplink url
    url = message.command[1]

# ==============================================
    
    def droplink_bypass(url):
        client = requests.Session()
        res = client.get(url)
        # print(res)
        ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

        h = {'referer': ref}
        res = client.get(url, headers=h)
        # print(res)

        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.find_all('input')
        data = { input.get('name'): input.get('value') for input in inputs }

        h = {
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest'
        }
        p = urlparse(url)
        final_url = f'{p.scheme}://{p.netloc}/links/go'
        print(final_url)

        time.sleep(3.1)
        res = client.post(final_url, data=data, headers=h).json()
        # print(res['url'])

        return res['url']

    # ==============================================
    msg = f"**Here Is Your Link:**\n{droplink_bypass(url)}"
    message.reply_text(msg, quote=True)
bot.run()