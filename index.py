import discord 
import json

# from discord import message

# def read_token():
#     with open("token.txt", "r") as f:
#         lines = f.readlines()
#         return lines[0].strip()
    
# token = read_token()
# client = discord.Client()

# commands = '''```list of Calendar Bot commands:
        
#         $add                <name> <date> <time> 
        
#             - Add events to your scehdule with a name, date and time.
#             - If the event name has multiple words, surround the name with apostrophes.
#             - Do not use more than 2 apostrphes
#             - Example Valid Inputs:
#                 -> $add 'Team Liquid Vs. Vitality CS:GO Game' 24/11/21 6:00pm
#                 -> $add Lecture 15/11/21 8:00am
        
#         $events             <none>
#                             <event name>

#             - Displays all planned events in a timely order.
#             - To display all events do not specify an event name.
#             - To display the details of a specific event, use the events command followed by the event name.
#             - If the event name has multiple words, surround the name with apostrophes.
#             - Example Valid Inputs:
#                 -> $events
#                 -> $events Lecture
#                 -> $events 'Team Liquid Vs. Vitality CS:GO Game'
                            
#         $change             <name> <date> <time>
        
#             - Change event dates and times in your scehdule with an existing name, new date and new time.
#             - If the event name has multiple words, surround the name with apostrophes.
#             - Do not use more than 2 apostrphes
#             - Example Valid Inputs:
#                 -> $add 'Team Liquid Vs. Vitality CS:GO Game' 24/11/21 6:00pm
#                 -> $add Lecture 15/11/21 8:00am

#         $delete             <event name>

#             - Delete an event within planned schedule, with an existing event name.
#             - If the event name has multiple words, surround the name with apostrophes.
#             - Example Valid Inputs:
#                 -> $delete Lecture
#                 -> $delete 'Team Liquid Vs. Vitality CS:GO Game'

#         $clear              <none>
            
#             - Clears all planned events within a schedule.
#             - Example Valid Input:
#                 -> $clear
        
#         $help               <none>

#             - Displays all bot commands and descriptions.
#             - Example Valid Input:
#                 -> $help

#         ```'''

# daysinmonth = {
#     1: 31,
#     2: 28,
#     3: 31,
#     4: 30,
#     5: 31,
#     6: 30,
#     6: 31,
#     8: 31,
#     9: 30,
#     10: 31,
#     11: 30,
#     12: 31,
# }

events = {}

def write(dict):
    json_object = json.dumps(dict, indent = 4)
    with open("events.json", "w") as outfile:
        outfile.write(json_object)  

channel = ""

# async def testDate(msg, channel):
#     pass

async def send(message):
    await message.channel.send(message)

def add_change(msg):
    # Reading from events.json
    with open("events.json") as r:
        file = json.load(r) # type = dictionary

        # Event to be added
        new_event = {
            "name": msg[1],
            "date": msg[2],
            "time": msg[3],
            "priority": len(file) + 1
        }
        
        if msg[0] == "$change" and file.get(msg[1], False) == False:
            # send("Event does not exist.")
            print("Event not found.")
            return False
        elif msg[0] == "$add" and not file.get(msg[1], False) == False:
            # send("Event already exists. Use the change command to change an exisiting event.")
            print("Event already exists. Use the 'change' command to change an exisiting event.")
            return False
        else:
            # If change then remove event that is to be changed and just proceed with adding (it again)
            if msg[0] == "$change":
                p = file.get(msg[1])["priority"] - 1    # 2
                file.pop(msg[1])    # {'name': 'Dude', 'date': '5/23/2022', 'time': '7:00', 'priority': 3}
                for i in range(p, len(file)):   # 2, 3
                    file[list(file)[i]]["priority"] -= 1
                new_event["priority"] -= 1
                
            events = file
            # print(list(events))
            
            # Checking for time conflict
            for event in events:
                curr = events[event]
                if new_event["date"] == curr["date"]:
                    if new_event["time"] == curr["time"]:
                        print("Time slot is occupied by an existing event. -> ", curr["name"])
                        return False
            
            # Appending new event
            events[new_event["name"]] = new_event
            new_list  = {}
            
            # Sorting priorities in each event
            for event in events:
                curr = events[event]
                curr_date = curr["date"].split('/')
                new_date = new_event["date"].split('/')
                # print(curr)
                # print(new_event)
                if new_date[2] > curr_date[2]: # Year
                    continue
                elif new_date[2] == curr_date[2]:
                    # print("year equal")
                    if  new_date[0] > curr_date[0]: # Month
                        continue
                    elif new_date[0] == curr_date[0]:
                        # print("month equal")
                        if new_date[1] > curr_date[1]: # Day
                            continue
                        elif new_date[1] == curr_date[1]:
                            # print("day equal")
                            curr_time = int(curr["time"].replace(":", ""))
                            new_time = int(new_event["time"].replace(":", ""))
                            # print(new_time, curr_time)
                            if new_time > curr_time:
                                continue
                
                # Swap priorities
                temp = new_event["priority"] # 5
                new_event["priority"] = curr["priority"] # 3
                curr["priority"] = temp # 5
                
                # New event for comparison = perviously swapped (curr)
                new_event = curr
                # print("switch")
            
            # Appending to new dictionary based on sorted priorities
            for num in range(len(events)):
                for event in events:
                    if events[event]["priority"] == num + 1:
                        new_list[event] = events[event]
            
            # fixing the priorities
            index = list(new_list)
            for i in range(0, len(index)):
                new_list[index[i]]["priority"] = i + 1   
                         
            write(new_list)
                                                        
            return True
              
print(add_change(["$change", "hb", "4/21/2022", "5:30"]))

    # "Babu": {
    #     "name": "Babu",
    #     "date": "5/22/2022",
    #     "time": "8:00",
    #     "priority": 1
    # },
    # "Hola": {
    #     "name": "Hola",
    #     "date": "5/22/2022",
    #     "time": "9:00",
    #     "priority": 2
    # },
    # "Dude": {
    #     "name": "Dude",
    #     "date": "5/23/2022",
    #     "time": "7:00",
    #     "priority": 3
    # },
    # "Yadu": {
    #     "name": "Yadu",
    #     "date": "5/23/2022",
    #     "time": "9:00",
    #     "priority": 4
    # },
    # "Hey": {
    #     "name": "Hey",
    #     "date": "5/23/2022",
    #     "time": "10:00",
    #     "priority": 5
    # },
    # "Buddy": {
    #     "name": "Buddy",
    #     "date": "5/24/2022",
    #     "time": "3:00",
    #     "priority": 6
    # },
    # "Gay": {
    #     "name": "Gay",
    #     "date": "5/24/2022",
    #     "time": "7:00",
    #     "priority": 7
    # }

#yoyo umm well does ur code account for if the event name is larger than 1?

# @client.event
# async def on_ready():
#     print("We have logged in as {0.user}".format(client))
    
# @client.event
# async def on_message(message):
#     msg = message.content
#     channel = client.get_channel(channel_id)
#     if msg.startswith('$display'):
#         await message.channel.send("Not done yet.")
#     elif msg.startswith('$add') or msg.startswith('$change'):
        
#         #check if theres multiple '
#         c = 0
#         for i in range(len(msg)):
#             if msg[i] == "'":
#                 c += 1

#         if c > 2:
#             await message.channel.send("You cannot use apostrophes within the event name!")
#         elif c == 1:
#             await message.channel.send("You must add an apostrophe at the end of the event name!")
#         else:
#             #check if name is multiple words
#             m = msg.split(" ")
#             if ((len(m) > 4) and (m[1][0] == "'") and (m[-3][-1] == "'") and c == 2):
#                 s = msg.split("'")
#                 add
# = s[0].strip()
#                 datetime = s[2].strip().split(' ')
#                 string = []
#                 string.append(add)  
#                 string.append(s[1])
#                 string.append(datetime[0]) 
#                 string.append(datetime[1])
#                 add_change(string)
#             elif ((len(m) > 4) and ((m[1][0] != "'") or (m[-3][-1] != "'"))):
#                 await message.channel.send("You have not declared the event name correctly!")
#             elif len(m) == 4:
#                 add_change(msg)
#
#                
#                
#     elif msg.startswith('$help'):
#         await message.channel.send(commands)
#     elif msg.startswith('$delete'):
#         try:
#             name = msg.split("'")
#             with open("events.json") as r:
#                 events = json.load(r)
#                 d = events.pop(name[1], None)
#                 if d == None:
#                     await message.channel.send("Event not found.")
            
#             write(events) 
#         except:
#             await message.channel.send("Improper syntax") 
            
#     elif msg.startswith('$clear'):
#         events = {}
#         write(events)
#     elif msg.startswith('$ping'):
             
# client.run(token)