import json
import re
from typing import Iterable
from openai import OpenAI

from paths import CHAT_GPT_CONFIG
from commons.design_patterns import Singleton


class ChatGptApiClient(metaclass=Singleton):
    def __init__(self):
        with open(CHAT_GPT_CONFIG) as file:
            self.credentials = json.load(file)

        self.client = OpenAI(api_key=self.credentials["api_key"])

    def request_keyword_suggestions(
        self, example_keywords: Iterable[str], response_keywords_number=5
    ):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            temperature=0,
            frequency_penalty=0,
            top_p=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful SEO assistant in B2C Commerce, designed to output JSON.",
                },
                {
                    "role": "user",
                    "content": self.build_keywords_suggestions_request(
                        ["production", "video", "audio"], 5
                    ),
                },
                {
                    "role": "assistant",
                    "content": "1. entertainment\n2. content creation\n3. digital media\n4. podcast\n5. streaming",
                },
                {
                    "role": "user",
                    "content": self.build_keywords_suggestions_request(
                        example_keywords,
                        response_keywords_number,
                    ),
                },
            ],
        )
        content = response.choices[0].message.content
        return self.parse_keywords_suggestions_response(content)

    def parse_keywords_suggestions_response(self, response_message: str):
        pattern = r"(\d+\.\s*)?(.+)"
        match_groups = re.findall(pattern, response_message)
        return [group[1] for group in match_groups]

    def build_keywords_suggestions_request(
        self, example_keywords, response_keywords_number=5
    ):
        listing = ", ".join(
            [f"`{self.preprocess_keyword(keyword)}`" for keyword in example_keywords]
        )
        return f"Suggest {response_keywords_number} keywords like {listing}"

    def preprocess_keyword(self, keyword):
        return keyword.lower().replace(".", "").replace(",", "")
