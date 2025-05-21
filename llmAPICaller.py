import os
from groq import Groq

client = Groq(
    # api_key=os.environ.get("GROQ_API_KEY"),  # This is the default and can be omitted
    api_key= ""
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs. Respond in just 1 line. Keep it simple",
        }
    ],
    model="llama3-8b-8192",
)
print(chat_completion.choices[0].message.content)