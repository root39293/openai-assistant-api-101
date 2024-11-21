from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Code Interpreter Assistant
assistant = client.beta.assistants.create(
   name="Data Analyst",
   instructions="You are a data analyst who helps with Python code and data analysis.",
   model="gpt-4o-mini",
   tools=[{"type": "code_interpreter"}]
)

# Thread
thread = client.beta.threads.create()

# 데이터 분석
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="""
    1. Create a random dataset of 100 numbers
    2. Create a histogram of the data
    3. Calculate basic statistics
    4. Show me the plot and results
    """
)

# Run
run = client.beta.threads.runs.create(
   thread_id=thread.id,
   assistant_id=assistant.id
)

# Run 상태 확인
while True:
   run_status = client.beta.threads.runs.retrieve(
       thread_id=thread.id,
       run_id=run.id
   )
   if run_status.status == "completed":
       break
   time.sleep(1)

# Result
messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order="asc"
)

for message in messages:
    for content in message.content:
        if content.type == 'image_file':
            image_data = client.files.with_raw_response.retrieve_content(content.image_file.file_id)
            # save image
            with open(f"histogram.png", "wb") as f:
                f.write(image_data.content)
        else:
            print(content.text.value)