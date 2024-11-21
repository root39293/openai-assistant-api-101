from openai import OpenAI
import time
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Vector Store
vector_store = client.beta.vector_stores.create(name="Document Store")

# file upload, vector store setting
file = open("example.pdf", "rb")
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=[file]
)

# Assistant 
assistant = client.beta.assistants.create(
    name="Document Assistant",
    instructions="You help users understand documents.",
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {
            "vector_store_ids": [vector_store.id]
        }
    }
)

# Thread
thread = client.beta.threads.create(
    messages=[{
        "role": "user",
        "content": "PDF의 주요 내용을 요약해주세요."
    }]
)

# Run
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

while True:
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run_status.status == "completed":
        break
    time.sleep(1)

messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order="asc"
)

for message in messages:
    print(f"Role: {message.role}")
    print(f"Content: {message.content[0].text.value}\n")