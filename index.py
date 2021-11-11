from os import name
import discord 
import json

from discord import message

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()
    
token = read_token()
client = discord.Client()

events = {}
commands = '''```list of Calendar Bot commands:
        
        $add                <name> <date> <time> 
        
            - Add events to your scehdule with a name, date and time.
            - If the event name has multiple words, surround the name with apostrophes.
            - Do not use more than 2 apostrphes
            - Example Valid Inputs:
                -> $add 'Team Liquid Vs. Vitality CS:GO Game' 24/11/21 6:00pm
                -> $add Lecture 15/11/21 8:00am
        
        $events             <none>
                            <event name>

            - Displays all planned events in a timely order.
            - To display all events do not specify an event name.
            - To display the details of a specific event, use the events command followed by the event name.
            - If the event name has multiple words, surround the name with apostrophes.
            - Example Valid Inputs:
                -> $events
                -> $events Lecture
                -> $events 'Team Liquid Vs. Vitality CS:GO Game'
                            
        $change             <name> <date> <time>
        
            - Change event dates and times in your scehdule with an existing name, new date and new time.
            - If the event name has multiple words, surround the name with apostrophes.
            - Do not use more than 2 apostrphes
            - Example Valid Inputs:
                -> $add 'Team Liquid Vs. Vitality CS:GO Game' 24/11/21 6:00pm
                -> $add Lecture 15/11/21 8:00am

        $delete             <event name>

            - Delete an event within planned schedule, with an existing event name.
            - If the event name has multiple words, surround the name with apostrophes.
            - Example Valid Inputs:
                -> $delete Lecture
                -> $delete 'Team Liquid Vs. Vitality CS:GO Game'

        $clear              <none>
            
            - Clears all planned events within a schedule.
            - Example Valid Input:
                -> $clear
        
        $help               <none>

            - Displays all bot commands and descriptions.
            - Example Valid Input:
                -> $help

        ```'''

def write(dict):
    json_object = json.dumps(dict, indent = 4)
    with open("events.json", "w") as outfile:
        outfile.write(json_object)    

def enter_event(msg):
    new_event = {
        "name": msg[1],
        "date": msg[2],
        "time": msg[3]
    }

    # Reading from events.json
    with open("events.json") as r:
        events = json.load(r)
        events[new_event["name"]] = new_event
        write(events)
    
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    
@client.event
async def on_message(message):
    msg = message.content
    if msg.startswith('$display'):
        await message.channel.send("Not done yet.")
    elif msg.startswith('$add') or msg.startswith('$change'):
        
        #check if theres multiple '
        c = 0
        for i in range(len(msg)):
            if msg[i] == "'":
                c += 1

        if c > 2:
            await message.channel.send("You cannot use apostrophes within the event name!")
        elif c == 1:
            await message.channel.send("You must add an apostrophe at the end of the event name!")
        else:
            #check if name is multiple words
            m = msg.split(" ")
            if ((len(m) > 4) and (m[1][0] == "'") and (m[-3][-1] == "'") and c == 2):
                s = msg.split("'")
                add = s[0].strip()
                datetime = s[2].strip().split(' ')
                string = []
                string.append(add)  
                string.append(s[1])
                string.append(datetime[0]) 
                string.append(datetime[1])
                enter_event(string)
            elif ((len(m) > 4) and ((m[1][0] != "'") or (m[-3][-1] != "'"))):
                await message.channel.send("You have not declared the event name correctly!")
            elif len(m) == 4:
                enter_event(msg.split(' '))
                
    elif msg.startswith('$help'):
        await message.channel.send(commands)
    elif msg.startswith('$delete'):
        try:
            name = msg.split("'")
            with open("events.json") as r:
                events = json.load(r)
                d = events.pop(name[1], None)
                if d == None:
                    await message.channel.send("Event not found.")
            
            write(events) 
        except:
            await message.channel.send("Improper syntax") 
            
    elif msg.startswith('$clear'):
        events = {}
        write(events)
            
client.run(token)
