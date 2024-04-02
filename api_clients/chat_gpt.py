import json
import re
from typing import Iterable
from openai import OpenAI

from paths import CHAT_GPT_CONFIG


class ChatGptApiClient:
    def __init__(self, chat_gpt_config=CHAT_GPT_CONFIG):
        with open(chat_gpt_config) as file:
            self.credentials = json.load(file)

        self.client = OpenAI(api_key=self.credentials["api_key"])
