import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "Refactor the following Python code:\n\n'''\nwhile True:\n  mass = int(input(\"Enter the mass value: \"))\n  if mass > 0:\n    break\nwhile True:\n  acceleration = int(input(\"Enter the acceleration: \"))\n  if acceleration > 0:\n    break\nprint(\"The Force is\", mass * acceleration)\n'''"
    }
  ],
  temperature=0,
  max_tokens=1000,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response["choices"][0]["message"]["content"])
