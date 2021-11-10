import discord 
import json

from discord import message

events = {}

def write(dict=events):
    json_object = json.dumps(dict, indent = 4)
    with open("events.json", "w") as outfile:
        outfile.write(json_object)

def enter_event(command):
    new_event = {
        "name": command[1],
        "date": command[2],
        "time": command[3]
    }

    # Reading from calendar.json
    with open("events.json") as c:
        read_json = json.load(c)
        events = read_json
        
    events[new_event["name"]] = new_event
    write(events)

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()
    
token = read_token()
client = discord.Client()

@client.event
async def on_message(message):
     # print(message.content)
     if message.content.startswith('!event') != -1:
        print(message.content)
     else:
        print("'%s' not a command. Enter --commands to see a list of valid commands" % message[0])
        
client.run(token)