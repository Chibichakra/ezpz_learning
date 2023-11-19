from openai import OpenAI
import os

class ExpandModel:
    def __init__(self, context, extra_context = None) -> None:
        self.client = OpenAI(
            api_key=os.environ['OPENAI_APIKEY'],
        )
        self.model = 'gpt-3.5-turbo'
        self.default_messages = [{"role": "system", "content": "You need to provide more details related to a specific paragraph or phrase depending on the following context: " + context}]

        if extra_context:
            self.default_messages += [{"role": "system", "content": "Here is some extra context for the required details: " + extra_context}]

        

    def expand(self, phrase) -> None:
        response = self.client.chat.completions.create(
            model = self.model,
            messages = self.default_messages + [{"role": "user", "content": phrase}]
        )

        return response.choices[0].message.content

