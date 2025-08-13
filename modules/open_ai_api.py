from openai import OpenAI

#Chat GPT and Deep Seek are use the same API
class ChatGPT():
    api_key = None
    model = None
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai = OpenAI(api_key=api_key)

    def chat(self, prompt, model="gpt-3.5-turbo"):
        response = self.openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content']
    
    def chat_with_context(self, prompt, context):
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": context}, {"role": "user", "content": prompt}],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content']