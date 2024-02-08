import json
import requests
import os
from openai import OpenAI
from prompts import formatter_prompt, assistant_instructions

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
x_rapid_api_key = "c233a1a325mshae8707ed83ff4fap197c5fjsn558c106f46f2"
#Alejo (paid): c233a1a325mshae8707ed83ff4fap197c5fjsn558c106f46f2
#Henry: 292b37741emsh8c5ef5e63f9442ep19a024jsnff83c46ee798
x_rapid_api_host = "ski-resorts-and-conditions.p.rapidapi.com"
# Init OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)


#Functions
def get_available_resorts(page_number=1, get_all_pages=True):
  url = "https://ski-resorts-and-conditions.p.rapidapi.com/v1/resort"

  headers = {
      "X-RapidAPI-Key": x_rapid_api_key,
      "X-RapidAPI-Host": x_rapid_api_host
  }

  all_resorts = []  #make an empty list
  while True:
    response = requests.get(url, params={"page": page_number}, headers=headers)
    all_resorts.extend(response)  #add things to the end of the list
    print("NEXT PAGE:", response.json()["next_page"])
    print("ALL RESORTS SO FAR:", all_resorts)

    if not get_all_pages or not response.json()["next_page"]:
      break
    page_number += 1

  return all_resorts


def get_url_for_mountain_conditions(mountain, available_resorts):
  client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )

  chat_completion = client.chat.completions.create(
      messages=[{
          "role":
          "user",
          "content":
          f"Given the mountain that the user wants to know the skiing conditions for: {mountain}, retrieve the correct URL from this JSON-inside-of-a-list: {available_resorts}. ONLY RETURN THE URL AND NOTHING ELSE.",
      }],
      model="gpt-4-1106-preview",
  )
  return chat_completion.choices[0].message.content.strip()


def get_mountain_conditions(url_for_mountain):
  headers = {
      "X-RapidAPI-Key": x_rapid_api_key,
      "X-RapidAPI-Host": x_rapid_api_host
  }

  response = requests.get(url_for_mountain, headers=headers)
  return response.json()


def lifts_status(mountain):  #:str = "alpine meadows"
  available_resorts = get_available_resorts()
  print(available_resorts)
  url_for_mountain = get_url_for_mountain_conditions(mountain,
                                                     available_resorts)
  print(url_for_mountain)
  mountain_conditions = get_mountain_conditions(url_for_mountain)
  print(mountain_conditions)
  return mountain_conditions


#use lift_status() to get the lift status for a mountain


# Create or load assistant
def create_assistant(client):
  assistant_file_path = 'assistant.json'

  # If there is an assistant.json file already, then load that assistant
  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    # If no assistant.json is present, create a new assistant using the below specifications

    # To change the knowledge document, modifiy the file name below to match your document
    # If you want to add multiple files, paste this function into ChatGPT and ask for it to add support for multiple files
    file = client.files.create(file=open("knowledge.pdf", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(
        # Getting assistant prompt from "prompts.py" file, edit on left panel if you want to change the prompt
        instructions=assistant_instructions,
        model="gpt-4-1106-preview",
        tools=[
            {
                "type": "retrieval"  # This adds the knowledge base as a tool
            },
            {
                "type": "function",  # This adds the solar calculator as a tool
                "function": {
                    "name": "get_weather",
                    "description":
                    "",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type":
                                "string",
                                "description":
                                "Location (address, mountain, hotel) to get weather conditions for"
                            }
                        },
                        "required": ["address", "monthly_bill"]
                    }
                }
            },
            {
                "type": "function",  # This adds the lift status as a tool
                "function": {
                    "name": "get_lift_status",
                    "description": "returns the lift status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "mountain": {
                                "type": "string",
                                "description": "Name of the mountain."
                            }
                        },
                        "required": ["mountain"]
                    }
                }
            }
        ],
        file_ids=[file.id])

    # Create a new assistant.json file to load on future runs
    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
