# assistant_thread.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a helpful math tutor who helps students understand math concepts.",
    model="gpt-4o-mini"
)

print(f"Created assistant ID: {assistant.id}")

# Thread
thread = client.beta.threads.create()
print(f"Created thread ID: {thread.id}")

# Thread message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is the Pythagorean theorem?"
)

# Run
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

print(f"Created run ID: {run.id}")