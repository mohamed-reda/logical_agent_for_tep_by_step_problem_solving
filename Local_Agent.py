from openai import OpenAI

# add your own API key or your Local LLM
client = OpenAI(base_url="URL")
llm_name = "LLM name"


# Create our own simple agent
class LocalAgent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        response = client.chat.completions.create(
            model=llm_name,
            messages=self.messages,
            max_tokens=400,  # Adjust as needed
            temperature=0.6,
            # Lower temperature reduces randomness and creativity, helping to reduce hallucinations <button class="citation-flag" data-index="6">
            top_p=0.6,  # Use nucleus sampling to focus on high-probability tokens
            frequency_penalty=0.5,  # Penalize repetitive tokens to avoid nonsensical outputs
            presence_penalty=0.6,  # Encourage diversity in responses
            stream=False
        )
        return response.choices[0].message.content
