#!/usr/bin/env python3

import os
import feedparser
from gtts import gTTS
from bs4 import BeautifulSoup
import random
from datetime import datetime

# List of RSS feeds
feeds = [
    {"name": "Jornal Fumaça", "url": "https://fumaca.pt/feed/"},
    {"name": "Jornal Mapa", "url": "https://jornalmapa.pt/feed/"},
    {"name": "Jornal Público", "url": "https://feeds.feedburner.com/PublicoRSS"},
    {"name": "Jornal de Negócios", "url": "https://www.jornaldenegocios.pt/rss"},
    {"name": "Noticias ao Minuto", "url": "https://www.noticiasaominuto.com/rss/cultura"},
    {"name": "Observador", "url": "https://observador.pt/rss"},
    {"name": "Outras Palavras", "url": "https://outraspalavras.net/feed/"},
    {"name": "Jornal Record", "url": "https://www.record.pt/rss"},
    {"name": "RTP", "url": "https://www.rtp.pt/noticias/rss"}
]

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def fetch_and_save_feed(feed, filename):
    print(f"Fetching feed from {feed['name']}...")
    text = f"Fetching feed from {feed['name']}."
    
    d = feedparser.parse(feed['url'])
    for entry in d.entries[:10]:  # Read out the first 10 entries
        title = entry.title
        summary = clean_html(entry.summary) if 'summary' in entry else "No summary available."
        print(f"Título: {title}")
        print(f"Sumário: {summary}")
        
        text += f" Title: {title}. Summary: {summary}."
    
    tts = gTTS(text=text, lang='pt')
    tts.save(filename)

def fisher_yates_shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]

# Save the audio to a .mp3 file
def save_audio_to_file(filename):
    fisher_yates_shuffle(feeds)  # Shuffle the feeds using Fisher-Yates algorithm
    text = ' '.join([f"Título: {entry.title}. Sumário: {clean_html(entry.summary) if 'summary' in entry else 'No summary available.'}" 
                     for feed in feeds for entry in feedparser.parse(feed['url']).entries[:10]])
    tts = gTTS(text=text, lang='pt')
    tts.save(filename)

# Get current date and time
current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

# Fetch and save feeds with current date and time in filename
output_mp3_file = f"/home/machaddr/Labs/RadioAberta/news/news_audio_{current_time}.mp3"
save_audio_to_file(output_mp3_file)

# Clean up temporary files if any
if os.path.exists("temp.mp3"):
    os.remove("temp.mp3")
    