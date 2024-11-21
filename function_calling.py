# function_calling.py

from openai import OpenAI
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_weather(location):
   return {
       "temperature": 20,
       "condition": "sunny",
       "location": location
   }

# Assistant
assistant = client.beta.assistants.create(
   name="Weather Assistant",
   instructions="You help users check weather information.",
   model="gpt-4o-mini",
   tools=[{
       "type": "function",
       "function": {
           "name": "get_weather",
           "description": "Get current weather for a location",
           "parameters": {
               "type": "object",
               "properties": {
                   "location": {
                       "type": "string",
                       "description": "City name"
                   }
               },
               "required": ["location"]
           }
       }
   }]
)

# Thread
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
   thread_id=thread.id,
   role="user",
   content="What's the weather like in Seoul?"
)

# Run
run = client.beta.threads.runs.create(
   thread_id=thread.id,
   assistant_id=assistant.id
)

# function
while True:
   run_status = client.beta.threads.runs.retrieve(
       thread_id=thread.id,
       run_id=run.id
   )
   
   if run_status.status == 'requires_action':
       tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
       tool_outputs = []
       
       for tool_call in tool_calls:
           if tool_call.function.name == "get_weather":
               arguments = json.loads(tool_call.function.arguments)
               weather_data = get_weather(arguments['location'])
               tool_outputs.append({
                   "tool_call_id": tool_call.id,
                   "output": json.dumps(weather_data)
               })
       
       client.beta.threads.runs.submit_tool_outputs(
           thread_id=thread.id,
           run_id=run.id,
           tool_outputs=tool_outputs
       )
   
   elif run_status.status == 'completed':
       break
   
   time.sleep(1)

# result
messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order="asc"
)

for message in messages:
   print(f"Role: {message.role}")
   print(f"Content: {message.content[0].text.value}\n")