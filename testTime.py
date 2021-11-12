y = input()
y = str(y)
print(y)

colin = 0
for i in range(len(y)):
    if y[i] == ":":
        colin += 1

if colin != 1:
    #await message.channel.send("You have not declared the event time correctly!")
    print("Incorrect time format!")
    print("lol1")
else:
    b = y.split(":")
    if len(b) != 2:
        #await message.channel.send("You have not declared the event time correctly!")
        print("Incorrect time format!")
        print("lol2")
    else:
        if len(b[1]) != 4:
            #await message.channel.send("You have not declared the event time correctly!")
            print("Incorrect time format!")
            print("lol3")
        else:
            t = []
            t.append(str(b[0]))
            t.append(str(b[1][0] + b[1][1]))
            t.append(str(b[1][2] + b[1][3]))
            try:
                t[0] = int(t[0])
                t[1] = int(t[1])
            except Exception:
                #await message.channel.send("You have not declared the event time correctly!")
                print("Incorrect Time Entered!")
            else:
                if ((t[0] >= 1) and (t[0] <= 12)):
                    if ((t[1] >= 0) and (t[1] <= 59)):
                        if ((t[2] == "am") or (t[2] == "pm")):
                            print("valid Time Entered!")
                            if (t[1] < 10):
                                t[1] = str(t[1]).zfill(2)
                            t[0] = str(t[0]) 
                            t[1] = str(t[1])                     
                            print(t)
                        else:
                            #await message.channel.send("You have not declared the event time correctly!")
                            print("Invalid Time Entered!")
                    else:
                        #await message.channel.send("You have not declared the event minute correctly!")
                        print("valid Minute Entered!")
                else:
                    #await message.channel.send("You have not declared the event Hour correctly!")
                    print("valid Hour Entered!")