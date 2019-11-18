import requests
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import datetime

#Images
NewsAdpsace = Image.open("assets/empty.png","r")
Background = Image.open('assets/Background.jpg',"r")
Draw = ImageDraw.Draw(Background)

#Fonts
DateFont = ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', 35)
AdspaceFont = ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', 40)

Date = datetime.datetime.now().strftime('%A %dth %B %Y')
DateX = (Background.width - DateFont.getsize(Date)[0]) / 2

def GetNews(Language="en"):
    data = requests.get('https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game',headers={'Accept-Language' : Language}).json()
    if (len(data["battleroyalenews"]["news"]["messages"]) == 1 and data["battleroyalenews"]["news"]["messages"][0]["image"] != "https://cdn2.unrealengine.com/Fortnite/fortnite-game/battleroyalenews/v42/BR04_MOTD_Shield-1024x512-75eacc957ecc88e76693143b6256ba06159efb76.jpg") or (len(data["battleroyalenews"]["news"]["messages"]) == 2 and data["battleroyalenews"]["news"]["messages"][1]["image"] == "https://cdn2.unrealengine.com/Fortnite/fortnite-game/battleroyalenews/v42/BR04_MOTD_Shield-1024x512-75eacc957ecc88e76693143b6256ba06159efb76.jpg"):
        return News1(data["battleroyalenews"]["news"]["messages"][0])
    else:
        return News3(data)

def DrawAdspace(X,Y,Message):
    AdspaceLeft = NewsAdpsace.crop((0, 0, 23, 47))
    Background.paste(AdspaceLeft,(X,Y),AdspaceLeft)
        
    AdspaceMiddle = NewsAdpsace.crop((23, 0, 66, 47)).resize((DateFont.getsize(Message)[0] - 40,47), Image.ANTIALIAS)
    Background.paste(AdspaceMiddle,(X + AdspaceLeft.width,Y),AdspaceMiddle)
        
    AdspaceRight = NewsAdpsace.crop((66, 0, 122, 47))
    Background.paste(AdspaceRight,(X + AdspaceLeft.width + AdspaceMiddle.width,Y),AdspaceRight)

    Draw.text((X + AdspaceLeft.width, Y + 1), Message, font=AdspaceFont)

def News1(Message):
    #Fonts
    NewsFont = ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', 200)
    DescriptionFont = ImageFont.truetype('assets/BurbankSmall-Bold.otf', 30)

    #Draw "NEWS"
    Draw.text((((Background.width - NewsFont.getsize("NEWS")[0]) / 2),40), "NEWS", font=NewsFont)
    
    #Draw Date
    Draw.text((DateX, 25), Date,font=DateFont)

    #Draw Rectangle
    Draw.rectangle((554, 280, 1365, 735), fill="white")

    #Paste News Image
    NewsImage = Image.open(BytesIO((requests.get(Message["image"])).content)).resize((800, 383), Image.ANTIALIAS)
    Background.paste(NewsImage,(560,286))

    #Draw Title
    TitleFontSize = 40
    Title = Message["title"].upper()
    while (ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', TitleFontSize)).getsize(Title)[0] > 790:
        TitleFontSize -= 1
    TitleFont = (ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', TitleFontSize))
    TitleX = (Background.width - TitleFont.getsize(Title)[0]) / 2
    Draw.text((TitleX, 675), Title,(35,41,65), font=TitleFont)

    #Draw Description,Rectangle
    Descriptions = textwrap.wrap(Message["body"], width=50)
    y = 675 + TitleFont.getsize(Title)[1] + 19
    for Description in Descriptions:
        Draw.rectangle((554, y, 1365, y + 30), fill="white")
        Draw.text((570, y), Description,(76,147,203), font=DescriptionFont)
        y += 30
    Draw.rectangle((554, y, 1365, y + 6), fill="white")

    if "adspace" in Message:
        DrawAdspace(535,266,Message["adspace"])

    return Background

def News3(data):
    #Fonts
    NewsFont = ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', 250)
    
    x = 115
    y = 376
    i = 696

    #Get largest message to know how big the rectangle needs to be
    message = max(data["battleroyalenews"]["news"]["messages"], key = lambda x : len(x["body"]))
    for Description in textwrap.wrap(message["body"], width=45):
        i += 25

    for idx,Message in enumerate(data["battleroyalenews"]["news"]["messages"]):
        if idx == 3:
            break
        
        #Fonts
        NewsFont = ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', 200)
        DescriptionFont = ImageFont.truetype('assets/BurbankSmall-Bold.otf', 22)
        
        #Draw "NEWS"
        Draw.text((((Background.width - NewsFont.getsize("News")[0]) / 2),90), "NEWS", font=NewsFont)
        
        #Draw Date
        Draw.text((DateX, 75), Date,font=DateFont)
        
        #Draw Rectangle
        Draw.rectangle((x - 6, 370, x + 23 + 512, i), fill="white")
        
        #Paste News Image
        NewsImage = Image.open(BytesIO((requests.get(Message["image"])).content)).resize((530, 254), Image.ANTIALIAS)
        Background.paste(NewsImage,(x,y))
        
        #Draw Title
        TitleFontSize = 40
        Title = Message["title"].upper()
        while (ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', TitleFontSize)).getsize(Title)[0] > 525:
            TitleFontSize -= 1
        TitleFont = (ImageFont.truetype('assets/BurbankBigCondensed-Black.ttf', TitleFontSize))
        TitleX = (512 - TitleFont.getsize(Title)[0]) / 2
        Draw.text((TitleX + x, 638), Title,(35,41,65), font=TitleFont)
        
        #Draw Description,Rectangle
        y2 = 690
        for Description in textwrap.wrap(Message["body"], width=45):
            Draw.text((x + 15, y2), Description,(76,147,203), font=DescriptionFont)
            y2 += 25
            
        if "adspace" in Message:
            DrawAdspace(x - 24,353,Message["adspace"])
            
        x += 580
    return Background