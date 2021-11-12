from os import name
import discord 
import json
from discord.ext import commands
import datetime
from add_event import add_change

from discord import message

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()
    
token = read_token()
client = discord.Client()
client = commands.Bot(command_prefix = '$')

daysinmonth = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    6: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

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
            - Example Valid Inputs:
                -> $events
                -> $events Lecture
                -> $events 'Team Liquid Vs. Vitality CS:GO Game'
                            
        $change             <name> <date> <time>
        
            - Same format as adding except you use an existing event name.
            - Example Valid Inputs:
                -> $add 'Team Liquid Vs. Vitality CS:GO Game' 24/11/21 6:00pm
                -> $add Lecture 15/11/21 8:00am

        $delete             <event name>

            - Delete an event within planned schedule, with an existing event name.
            - Example Valid Inputs:
                -> $delete Lecture
                -> $delete 'Team Liquid Vs. Vitality CS:GO Game'

        $clear              <none>
            
            - Clears all planned events within a schedule.
            - Example Valid Input:
                -> $clear
        
        $display            <none>
        
            - Displays all planned events.
            - Example Valid Input:
                -> $display
        
        $help               <none>

            - Displays all bot commands and descriptions.
            - Example Valid Input:
                -> $help
        
        ```'''

def write(dict):
    json_object = json.dumps(dict, indent = 4)
    with open("events.json", "w") as outfile:
        outfile.write(json_object)    
        
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.command()
async def display(ctx):
    embed = discord.Embed(
            title = ':calendar_spiral: CALENDAR',
            url = 'https://calendar.google.com/calendar/u/0/r/month/',
            description = 'These are your upcoming scheduled events!',
            colour = 0x199400
            )
    
    embed.set_thumbnail(url = 'https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/2/25/Team_Liquidlogo_profile.png/revision/latest?cb=20210319225201')
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text='To interact with your schedule, type $help')
    
    with open('events.json') as f:
        obj = json.load(f)

    # Conveting time to 24hr
    for i in obj:
        l = obj[i]['time'].split(":")
        pringle = l[0]
        pringle = int(pringle)
        
        # Displays the actual calendar
        if ((pringle != 0) and (pringle < 10)):
            embed.add_field(name="{}".format(obj[i]['date']), value = '``` {} am   |   {}```'.format(obj[i]['time'], obj[i]['name']), inline = False)
        elif (pringle == 0):
            pringle = 12
            embed.add_field(name="{}".format(obj[i]['date']), value = '```{}{}{}{} am   |   {}```'.format(pringle, obj[i]['time'][2], obj[i]['time'][3], obj[i]['time'][4], obj[i]['name']), inline = False)
        else:
            if (pringle > 12):
                pringle -= 12
                if pringle < 10:
                    embed.add_field(name="{}".format(obj[i]['date']), value = '``` {}{}{}{} pm   |   {}```'.format(pringle, obj[i]['time'][2], obj[i]['time'][3], obj[i]['time'][4], obj[i]['name']), inline = False)
                else:
                    embed.add_field(name="{}".format(obj[i]['date']), value = '```{}{}{}{} pm   |   {}```'.format(pringle, obj[i]['time'][2], obj[i]['time'][3], obj[i]['time'][4], obj[i]['name']), inline = False)
            elif (pringle == 12):
                    embed.add_field(name="{}".format(obj[i]['date']), value = '```{}{}{}{} pm   |   {}```'.format(pringle, obj[i]['time'][2], obj[i]['time'][3], obj[i]['time'][4], obj[i]['name']), inline = False)
            else:
                embed.add_field(name="{}".format(obj[i]['date']), value = '```{} am   |   {}```'.format(obj[i]['time'], obj[i]['name']), inline = False)
    
    await ctx.send(embed=embed)


@client.event
async def on_message(message):
    msg = message.content
    if msg.startswith('$display'):
        pass
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
                
                ### Check if date is valid

                x = str(datetime[0])
                
                slash = 0
                for i in range(len(x)):
                    if x[i] == "/":
                        slash += 1

                if slash != 2:
                    await message.channel.send("You have not declared the event date correctly!")
                    print("Incorrect date format!")
                else:
                    z = x.split("/")
                    try:
                        z[0] = int(z[0])
                        z[1] = int(z[1])
                        z[2] = int(z[2])
                    except Exception:
                        await message.channel.send("You have not declared the event month correctly!")
                        print("Incorrect Date format!")
                    else:
                        if ((z[0] >= 1) and (z[0] <= 12)):
                            if ((z[1] >= 1) and z[1] <= daysinmonth[z[0]]):
                                if(z[2] >= 21):
                                    string.append(datetime[0])  #append date onto string
                                    
                                    ### NAME AND DATE CORRECT -> CHECK TIME
                                    
                                    y = datetime[1]
                                    
                                    colin = 0
                                    for i in range(len(y)):
                                        if y[i] == ":":
                                            colin += 1

                                    if colin != 1:
                                        await message.channel.send("You have not declared the event time correctly!")
                                    else:
                                        b = y.split(":")
                                        if len(b) != 2:
                                            await message.channel.send("You have not declared the event time correctly!")
                                        else:
                                            if len(b[1]) != 4:
                                                await message.channel.send("You have not declared the event time correctly!")
                                            else:
                                                t = []
                                                t.append(str(b[0]))
                                                t.append(str(b[1][0] + b[1][1]))
                                                t.append(str(b[1][2] + b[1][3]))
                                                try:
                                                    t[0] = int(t[0])
                                                    t[1] = int(t[1])
                                                except Exception:
                                                    await message.channel.send("You have not declared the event time correctly!")
                                                else:
                                                    if ((t[0] >= 1) and (t[0] <= 12)):
                                                        if ((t[1] >= 0) and (t[1] <= 59)):
                                                            if ((t[2] == "am") or (t[2] == "pm")):
                                                                
                                                                ### WORKED

                                                                v = datetime[1]
                                                                if v[-2] == "a":
                                                                    if t[0] < 10:
                                                                        v = v[0] + v[1] + v[2] + v[3]
                                                                    else:
                                                                        #v = "12:00am"
                                                                        pumper = v[0] + v[1]
                                                                        pumper = int(pumper)
                                                                        if pumper == 12:
                                                                            s = list(v)
                                                                            s[0] = "0"
                                                                            s[1] = "0"
                                                                            v = "".join(s)
                                                                            
                                                                        v = v[0] + v[1] + v[2] + v[3] + v[4]
                                                                            
                                                                        #v = "00:00"
                                                                        
                                                                elif v[-2] == "p":
                                                                    pumper = v[0] + v[1]
                                                                    pumper = int(pumper)
                                                                    if pumper == 12:
                                                                        t[0] = 12
                                                                    else:
                                                                        t[0] += 12      
                                                                    
                                                                    if len(v) == 6: 
                                                                        v = str(t[0]) + v[1] + v[2] + v[3]
                                                                    else:
                                                                        v = str(t[0]) + v[2] + v[3] + v[4]
                                                                
                                                                string.append(v)
                                                                print("Valid Input : Multiple Word Name ->")
                                                                print(string)
                                                                add_change(string)
                                                                
                                                            else:
                                                                await message.channel.send("You have not declared the event time correctly!")
                                                        else:
                                                            await message.channel.send("You have not declared the event minute correctly!")
                                                    else:
                                                        await message.channel.send("You have not declared the event Hour correctly!")       
                                else:
                                    await message.channel.send("You have not declared the event year correctly!")
                            else:
                                await message.channel.send("You have not declared the event Day correctly!")
                        else:
                            await message.channel.send("You have not declared the event year correctly!")
             
            elif ((len(m) > 4) and ((m[1][0] != "'") or (m[-3][-1] != "'"))):
                await message.channel.send("You have not declared the event name correctly!")
            elif len(m) == 4:
                
                ### TEST DATE
                
                x = m[2]
                y = m[3]
                
                slash = 0
                for i in range(len(x)):
                    if x[i] == "/":
                        slash += 1

                if slash != 2:
                    await message.channel.send("You have not declared the event date correctly!")
                else:
                    z = x.split("/")
                    try:
                        z[0] = int(z[0])
                        z[1] = int(z[1])
                        z[2] = int(z[2])
                    except Exception:
                        await message.channel.send("You have not declared the event month correctly!")
                    else:
                        if ((z[0] >= 1) and (z[0] <= 12)):
                            if ((z[1] >= 1) and z[1] <= daysinmonth[z[0]]):
                                if(z[2] >= 21):
                                    
                                    #NAME AND DATE GOOD -> CHECK TIME
                                    
                                    colin = 0
                                    for i in range(len(y)):
                                        if y[i] == ":":
                                            colin += 1

                                    if colin != 1:
                                        await message.channel.send("You have not declared the event time correctly!")
                                    else:
                                        b = y.split(":")
                                        if len(b) != 2:
                                            await message.channel.send("You have not declared the event time correctly!")
                                        else:
                                            if len(b[1]) != 4:
                                                await message.channel.send("You have not declared the event time correctly!")
                                            else:
                                                t = []
                                                t.append(str(b[0]))
                                                t.append(str(b[1][0] + b[1][1]))
                                                t.append(str(b[1][2] + b[1][3]))
                                                try:
                                                    t[0] = int(t[0])
                                                    t[1] = int(t[1])
                                                except Exception:
                                                    await message.channel.send("You have not declared the event time correctly!")
                                                else:
                                                    if ((t[0] >= 1) and (t[0] <= 12)):
                                                        if ((t[1] >= 0) and (t[1] <= 59)):
                                                            if ((t[2] == "am") or (t[2] == "pm")):
                                                                
                                                                ### CODE WORKED
                                                                v = msg.split(' ')
                                                                if v[3][-2] == "a":
                                                                    if t[0] < 10:
                                                                        v[3] = v[3][0] + v[3][1] + v[3][2] + v[3][3]
                                                                    else:                                                                      
                                                                        pumper = v[3][0] + v[3][1]
                                                                        pumper = int(pumper)
                                                                        if pumper == 12:
                                                                            s = list(v[3])
                                                                            s[0] = "0"
                                                                            s[1] = "0"
                                                                            v[3] = "".join(s)
                                                                        v[3] = v[3][0] + v[3][1] + v[3][2] + v[3][3] + v[3][4]
                                                                        
                                                                elif v[3][-2] == "p":
                                                                    pumper = v[3][0] + v[3][1]
                                                                    pumper = int(pumper)
                                                                    if pumper == 12:
                                                                        t[0] = 12
                                                                    else:
                                                                        t[0] += 12      
                                                                    if len(v[3]) == 6: 
                                                                        v[3] = str(t[0]) + v[3][1] + v[3][2] + v[3][3]
                                                                    else:
                                                                        v[3] = str(t[0]) + v[3][2] + v[3][3] + v[3][4]
                                                                
                                                                print("Valid Input : 1 Word Name ->")
                                                                print(v)
                                                                add_change(v)
                                                                
                                                            else:
                                                                await message.channel.send("You have not declared the event time correctly!")
                                                        else:
                                                            await message.channel.send("You have not declared the event minute correctly!")
                                                    else:
                                                        await message.channel.send("You have not declared the event Hour correctly!")
                                else:
                                    await message.channel.send("You have not declared the event year correctly!")
                            else:
                                await message.channel.send("You have not declared the event Day correctly!")
                        else:
                            await message.channel.send("You have not declared the event year correctly!")
                

    elif msg.startswith('$help'):
        await message.channel.send(commands)
    elif msg.startswith('$delete'):
        thekey = ""
        with open('events.json') as f:
            obj = json.load(f)
            h = msg.split(" ")
            
        for i in range(1, len(h)):
            if (i == len(h) - 1):
                thekey = thekey + h[i]
            else:
                thekey = thekey + h[i] + " " 

        r = dict(obj)
        del r[thekey]
        
        json_object = json.dumps(r, indent = 4)
        with open("events.json", "w") as outfile:
            outfile.write(json_object)    
            
    elif msg.startswith('$clear'):
        events = {}
        write(events)
        
    await client.process_commands(message)
        
        
client.run(token)