# GIT COMMANDS
# git fetch --all
# git switch altaaf

from PIL import Image, ImageDraw, ImageFont
from calendar import Calendar
from event import Event

# Decalring Basic dimensions and RGB values
LENGTH = 1280
WIDTH = 720
WHITE = (255,255,255)
BLACK = (0,0,0)
BACKGROUND = (47,49,54)
BLUE = (49,160,223)

# FONT's
TITLE_FNT = ImageFont.truetype("fonts/SourceCodePro-Light.ttf", 50)
SUBTITLE_FNT = ImageFont.truetype("fonts/SourceCodePro-Light.ttf", 35)
EVENT_FNT = ImageFont.truetype("fonts/SourceCodePro-Light.ttf", 30)


# Creates an image
out = Image.new("RGB", (LENGTH, WIDTH), BACKGROUND)

# Getting a drawing context
template = ImageDraw.Draw(out)

# Setting Title
template.multiline_text((30,30), "Calendar", font=TITLE_FNT, fill=WHITE, stroke_width=1)

X_PIXEL = 30
Y_PIXEL = 100

# Setting Sub-Title
template.text((X_PIXEL,Y_PIXEL), "Today's TO-DO List/Events", font=SUBTITLE_FNT, stroke_width=1)

# Sample events
event1 = Event("EVENT DESCRIPTION TEST 1 LONG VERSION TEST 1 TEST TEST TEST TES TES TEST ", "2021-11-10", "8:30pm")
event2 = Event("EVENT DESCRITION 2 !(*&^*(&", "2021-11-11", "5:30pm")
event3 = Event("EVENT DESCRIPTION 3 TEST TEST", "2021-11-11", "9:30pm")

# Sample Calendar
calendar = Calendar("Calendar 1")

# Adding events 
calendar.addEvent(event1)
calendar.addEvent(event2)
calendar.addEvent(event3)

Y_PIXEL += 70
# template.text((X_PIXEL, Y_PIXEL), "Description:", font=SUBTITLE_FNT, stroke_width=1, fill=BLUE)

# template.text((X_PIXEL, 650), "Description:", font=SUBTITLE_FNT, stroke_width=1, fill=BLUE)

for event in calendar.getEvents():

    Y_PIXEL += 100

    if (Y_PIXEL >= 650):
        Y_PIXEL = 200
        X_PIXEL = 640
    # description_len = len(event.getDescription())
    # description_words = event.getDescription().split(' ')
    # string = ""
    # x = 0

    # while (description_len > 30):
        
        # for word in description_words:
        #     x += len(word) + 1
        #     string += word + " "
        #     if (x > 30):
        #         string -= word + " "
        #         template.text((X_PIXEL, Y_PIXEL), text=string, )

    # template.text((X_PIXEL, Y_PIXEL), "Description:", font=EVENT_FNT, fill=BLUE, stroke_width=1)
    if (len(event.getDescription()) > 30):
        string = event.getDescription().split(' ')
        x = 0
        words = ""
        for word in string:
            x += len(word) + 1
            words += word + " "
            if (x > 30):
                template.text((X_PIXEL, Y_PIXEL), f'{words}', font=EVENT_FNT)
                x = 0
                words = "\n"

        template.text((X_PIXEL, Y_PIXEL), f'\n{words}', font=EVENT_FNT)
        Y_PIXEL += 70
        template.text((X_PIXEL, Y_PIXEL), f'\n{event.getDate()}', font=EVENT_FNT)
        continue
        
    
    template.text((X_PIXEL, Y_PIXEL), f'\n{event.getDescription()}\n{event.getDate()}\n', font=EVENT_FNT) 
    

# for event in calendar.getEvent():
#     calendar.text(f'{even.getDescription()}', )

# Drawing the calendar rectangular block
# d.rectangle([100,100,1180,620], fill = None, width = 2, outline = BLACK)

# # Drawing the columns
# for x in range(100 + int((1180-100)/7), 1281 - int((1180-100)/7), int((1180-100)/7)):
#     d.line([x, 100, x, 620], width = 2, fill = BLACK)

# # Drawing the rows
# for y in range(100, 621, 104):
#     d.line([100, y, 1180, y], width = 2, fill = BLACK)


# event_fnt = ImageFont.truetype("fonts/SourceCodePro-Light.ttf", 15)
# d.text((110,110), "TESTING LOL", fill = BLACK, font = event_fnt, stroke_width = 1)



# X_EVENTPIXEL = 0
# Y_EVENTPIXEL = 0
# row = 0
# col = 0



# for event in calendar.getEvents():
#     if (int(event.getDay()) > 7):
#         col = int(event.getDay())
#         while(col > 7):
#             row += 1
#             col -= 7
#         X_EVENTPIXEL = 110 + int((1180-100)/7) * (col - 1) 
#         Y_EVENTPIXEL = 110 + 104 * (row)
#         d.text((X_EVENTPIXEL, Y_EVENTPIXEL), f'{event.getDescription()}\n{event.getDate()}', fill = BLACK, font = event_fnt, stroke_width = 1)
#         row = 0
#         col = 0

#     else:
#         X_EVENTPIXEL = int(event.getDay()) * int((1180-100)/7)
#         Y_EVENTPIXEL = 110
#         d.text((X_EVENTPIXEL, Y_EVENTPIXEL), f'{event.getDescription()}\n{event.getDate()}', fill = BLACK, font = event_fnt, stroke_width = 1)
#         row = 0
#         col = 0

# X_EVENTPIXEL = 0
# Y_EVENTPIXEL = 0
# for day in days:
#     X_EVENTPIXEL += int((1180-100)/7)
#     Y_EVENTPIXEL += 104
#     d.text((X_EVENTPIXEL,Y_EVENTPIXEL), , fill = BLACK, font = event_fnt, stroke_width = 1)

# print(days)


# print(calendar.getEvents())
# print(calendar)
out.save("render.png")