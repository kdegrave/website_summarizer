from dotenv import load_dotenv 
from bs4 import BeautifulSoup
from openai import OpenAI
import requests
import os


class Website:
    """
    Class to parse website content while removing unhelpful tags.
    """

    def __init__(self, url):
        self.url = url

        try:
            content = requests.get(self.url).content
        except requests.RequestException as e:
            raise ValueError(f"Error fetching URL {self.url}: {e}")

        soup = BeautifulSoup(content, 'html.parser')

        for tag in soup(['script', 'style', 'img', 'input']):
            tag.decompose()

        self.title = soup.title.string if soup.title else 'No title available.'

        self.text = soup.body.get_text(separator='\n', strip=True) if soup.body else 'No content available.'


class Prompt:

    def __init__(self, website):
        self.website = website

    def create_prompts(self):

        system_prompt = 'You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown.'


        user_prompt = f"You are looking at a website titled {self.website.title}. \
The contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"

        user_prompt += self.website.text

        return [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ]


class Model:

    def __init__(self):
        load_dotenv()
        self.api_key = self.get_api_key()
        self.openai = OpenAI()

    @staticmethod
    def get_api_key():

        api_key = os.getenv('OPENAI_API_KEY')

        if not api_key:
            raise EnvironmentError("OpenAI API key not found. Ensure 'OPENAI_API_KEY' is set in the environment or .env file.")
        return api_key

    def summarize(self, model, prompt):

        response = self.openai.chat.completions.create(
            model=model,
            messages=prompt
        )

        return response.choices[0].message.content