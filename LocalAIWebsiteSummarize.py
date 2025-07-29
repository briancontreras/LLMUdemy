import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import ollama
from rich.markdown import Markdown
from rich.console import Console

#basic header titles
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
MODEL = "llama3.2"
class Website:
    def __init__(self,url):
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
    
#Defining the system prompt

system_prompt = "You are an assistant that analyzes the contents of a website\
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

#function for user Prompt

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\n The contents of this website is as follows; \ please provide a short summary of this website in markdown. \
    If it includes news or announcements, then summarise these too. \n\n"
    user_prompt += website.text
    return user_prompt

#now we are going to make a function that will get the setup for the website we passed it originiall
def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content" : user_prompt_for(website)}
    ]

def summarize(url):
    website = Website(url)
    response = ollama.chat(model=MODEL, messages = messages_for(website), stream=True)
    val = ""
    for chunk in response:
        print(chunk['message']['content'] or ' ', end=' ',flush=True)
        val += chunk['message']['content'] or ' '
    return val




print(Markdown(summarize("https://edwarddonner.com")))