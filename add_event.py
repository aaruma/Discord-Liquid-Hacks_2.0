import json

events = {}

def write(dict):
    json_object = json.dumps(dict, indent = 4)
    with open("events.json", "w") as outfile:
        outfile.write(json_object)  

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
                
                for i in range(len(new_date)):
                    curr_date[i] = int(curr_date[i])
                    new_date[i] = int(new_date[i])
                    
                # print(curr)
                # print(new_event)
                
                if new_date[2] > curr_date[2]: # Year
                    continue
                elif new_date[2] == curr_date[2]:
                    print("year equal")
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