x = input()
x = str(x)
print(x)

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

slash = 0
for i in range(len(x)):
    if x[i] == "/":
        slash += 1

if slash != 2:
    #await message.channel.send("You have not declared the event date correctly!")
    print("Incorrect date format!")
else:
    z = x.split("/")
    try:
        z[0] = int(z[0])
        z[1] = int(z[1])
        z[2] = int(z[2])
    except Exception:
        #await message.channel.send("You have not declared the event month correctly!")
        print("Incorrect Date format!")
    else:
        #ADDING THIS
        if ((z[0] <= 0) and (z[1] <= 0) and (z[2] <= 0)):
            #await message.channel.send("You have not declared the event year correctly!")
            print("Invalid year Entered!")
        elif ((z[0] >= 1) and (z[0] <= 12)):
            if ((z[1] >= 1) and z[1] <= daysinmonth[z[0]]):
                if(z[2] >= 21):
                    #Execute Code, No problems exist
                    print("valid Date Entered!")
                else:
                    #await message.channel.send("You have not declared the event year correctly!")
                    print("Incorrect Year added!")
            else:
                #await message.channel.send("You have not declared the event Day correctly!")
                print("Incorrect Day added!")
        else:
            #await message.channel.send("You have not declared the event year correctly!")
            print("Incorrect Month added!")
                
        print(z)
    

