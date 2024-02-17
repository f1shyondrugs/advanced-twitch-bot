from twitchio.ext import commands
import pickle
from pydub import AudioSegment
from pydub.playback import play
from discord_webhook import DiscordWebhook
import time
import random
import pygame
import datetime

spamsuggestionwebhookurl = "YOUR WEBHOOK URL"
webhookurl = "YOUR WEBHOOK URL"
twitchlink = "YOUR TWITCH LINK"
admins = ["f1shy312", "ADMIN2"]



    

all_emotes = []
with open("allemotes.txt","r") as w:
    a = w.readlines()
    for line in a:
        all_emotes.append(line.strip())

def randomemoji():
    return all_emotes[random.randint(0,len(all_emotes) - 1)]

today = datetime.datetime.today().strftime('%Y-%m-%d___%H-%M-%S')
logfile = "logs/log-" + today + ".log"
with open(logfile, "w") as w:
    w.write(f"-- LOGS -- {str(datetime.datetime.now())} -- \n")


# -------------
# GAMBLE POINTS
# -------------

async def gamblef(msg, number):
    


    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
        userpts = data[str(msg.author.name)][0]
        if number < 100:
            await msg.channel.send(f'/me {msg.author.mention}, please enter a valid amount to gamble. minimum 100 points.')
            return
        try:
            float(number)
        except:
            await msg.channel.send(f'/me {msg.author.mention}, please enter a valid amount to gamble. minimum 100 points.')
            return
        if userpts < number:
            await msg.channel.send(f'/me {msg.author.mention}, you do not have enough points ({userpts}/{number}) {randomemoji()}')
            return
        else:
            
            pick = random.randint(1,10)
            if pick > 6:
                data[str(msg.author.name)] = [data[str(msg.author.name)][0] + number, data[str(msg.author.name)][1]]
                await msg.channel.send(f'/me {msg.author.mention} gambled {number} points and won {randomemoji()} current points: {data[str(msg.author.name)][0]}')
                with open(logfile, "a") as w:
                    w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} gambled {number} points and WON | Updated: {data[str(msg.author.name)][0]}\n")
            else:
                data[str(msg.author.name)] = [data[str(msg.author.name)][0] - number, data[str(msg.author.name)][1]]
                await msg.channel.send(f'/me {msg.author.mention} gambled {number} points and lost {randomemoji()} current points: {data[str(msg.author.name)][0]}')
                with open(logfile, "a") as w:
                    w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} gambled {number} points and LOST | Updated: {data[str(msg.author.name)][0]}\n")

        

        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)




# ----------
# SET POINTS
# ----------
            
async def adminset(msg, user, number):
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
        userpts = data[str(msg.author.name)][0]
        if msg.author.name not in admins:
            await msg.channel.send(f'/me {msg.author.mention} You are not allowed to do this {randomemoji()}')
            return
        else:
            data[str(user)] = [number, data[str(user)][1]]
            await msg.channel.send(f'/me {msg.author.mention} set @{user} points to {number}!')

            with open('data.pickle', 'wb') as f:
                pickle.dump(data, f)






# ----------
# GET POINTS
# ----------

async def points(message, opfer):
        pointorpoints = "points"
        if opfer[0] == "@":
            opfer = opfer[1:]

        with open('data.pickle', 'rb') as f:
            data = pickle.load(f)

        try:
            if data[str(opfer)][0] == 1:
                pointorpoints = "point"
        except KeyError:
            await message.channel.send(f"/me {opfer} doesn't have any data on my bot {randomemoji()}")
            return


        if opfer == message.author.name:
            await message.channel.send(f"/me {message.author.mention} has {data[str(message.author.name)][0]} {pointorpoints} {randomemoji()}")
        else:
            await message.channel.send(f"/me @{opfer} has {data[str(opfer)][0]} {pointorpoints} {randomemoji()}")




# ----------
# PAY POINTS
# ----------

async def pay(msg, opfer, number):
    


    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
        userpts = data[str(msg.author.name)][0]
        if number < 100:
            await msg.channel.send(f'/me {msg.author.mention}, please enter a valid amount to pay. minimum 100 points.')
            return
        try:
            float(number)
        except:
            await msg.channel.send(f'/me {msg.author.mention}, please enter a valid amount to pay. minimum 100 points.')
            return
        if userpts < number:
            await msg.channel.send(f'/me {msg.author.mention}, you do not have enough points ({userpts}/{number}) {randomemoji()}')
            return
        else:
            data[str(msg.author.name)] = [data[str(msg.author.name)][0] - number, data[str(msg.author.name)][1]]
            data[str(opfer)] = [data[str(opfer)][0] + number, data[str(opfer)][1]]
            await msg.channel.send(f'/me {msg.author.mention} paid {number} points to @{opfer} {randomemoji()}')

            with open(logfile, "a") as w:
                w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} paid {number} points to {opfer} | Updated: {data[str(msg.author.name)][0]}\n")

        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)




# --------
# PLAY SFX
# --------
            
async def sfx(msg, song):
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
        userpts = data[str(msg.author.name)][0]


        all_sfx = {"finishhimdaddy": 300, "lospenguinos": 700, "ummguysisthisfreddyfazbear": 600, "waterphone": 300, "chinaguyexplaining": 700, "ewwdudewtf": 500,
                   "goddamn": 200, "ohmygod": 500, "ohmygoodness": 400, "stopitgetsomehelp": 300}

        print(song)
        if song == "help":
            await msg.channel.send("All SFX on web or smth")
            return
        for key in all_sfx.keys():
            if song.lower() == key.lower():
                if userpts < all_sfx[key]:
                    await msg.channel.send(f"You do not have enough points to redeem this sfx ({userpts}/{all_sfx[key]}) {randomemoji()}")
                    return
                else:
                    await msg.channel.send(f"{msg.author.mention} played {song} for {all_sfx[key]} points {randomemoji()}")
                    data[str(msg.author.name)] = [data[str(msg.author.name)][0] - all_sfx[key], data[str(msg.author.name)][1]]
                    with open('data.pickle', 'wb') as f:
                        pickle.dump(data, f)

                    with open(logfile, "a") as w:
                        w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} played {song} for {all_sfx[key]} points | Updated: {data[str(msg.author.name)][0]}\n")
                    

                    pygame.mixer.init() 
                    
                    sound_file =f"sfx/{song}.mp3" 
                    sound = pygame.mixer.Sound(sound_file)  

                    sound.play() 
                    
                    return
        
        await msg.channel.send(f"This one doesn't exist! you find all of them on ____ {randomemoji()}")



# --------------
# ROB FOR POINTS
# --------------
            
lll = []

async def rob(msg, opfer):
    user = msg.author.name
    global lll

    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)

    if len(lll) >= 3:
        for i in range(0,len(lll)):
            lll.pop(0)
            print(lll)


    if user == opfer:
        await msg.channel.send(f"/me bro you cant rob yourself")
        return

    if user not in lll or len(lll) == 0:
        try:
            if data[str(opfer)][0] >= 200:
                lll.append(user)
                r = round(data[str(opfer)][0] / random.randint(5, 10))
                data[opfer] = data[str(opfer)][0] - r, data[str(opfer)][1]
                data[user] = data[str(user)][0] + r, data[str(user)][1]

                await msg.channel.send(f"/me {user} robbed {opfer} for {r} points {randomemoji()}")

                with open('data.pickle', 'wb') as f:
                    pickle.dump(data, f)

                with open(logfile, "a") as w:
                    w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} robbed {opfer} for {r} points | Updated: {data[str(msg.author.name)][0]}\n")
                    

                

            else:
                await msg.channel.send(f"/me {opfer} is too poor to rob. {randomemoji()}")
                return
    
            
        except KeyError:
            await msg.channel.send(f"/me {opfer} doesn't have any data on my bot {randomemoji()}")
            return
    else:
        await msg.channel.send(f"@{msg.author.name} you've already robbed someone, wait a bit and try again.")



# --------
# GIVEAWAY
# --------

prize = "None"
listofusers = []
async def giveaway(msg, mode, prize):    
    global listofusers
    

    prizestr = " ".join(prize)
    if mode == "start":
        if msg.author.name in admins:
            listofusers = []
            await msg.channel.send(f"Giveaway ({str(prizestr)}) started NOW | Enter with '!giveaway enter' {randomemoji()}")
        else:
            await msg.channel.send(f"@{msg.author.name} you do not have the permissions to do that, sorry!")
    
    elif mode == "end":
        if msg.author.name in admins:
            winner = listofusers[random.randint(0, len(listofusers) - 1)]
            await msg.channel.send(f"Giveaway ({str(prizestr)}) ended NOW | Congrats to @{winner} {randomemoji()}")
            with open(logfile, "a") as w:
                w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} won the giveaway! | Prize: {prizestr}")                                         

        else:
            await msg.channel.send(f"@{msg.author.name} you do not have the permissions to do that, sorry!")

    elif mode == "enter":
        if prize != "None":
            if msg.author.name not in listofusers:
                listofusers.append(msg.author.name)
                await msg.channel.send(f"@{msg.author.name} successfully entered the current giveaway {randomemoji()}")
            else:
                await msg.channel.send(f"@{msg.author.name} you've already entered this giveaway!")

        else:
            await msg.channel.send(f"@{msg.author.name} No giveaway running rn, sorry!")


activebingo = False
rightemote = None



# ------------
# SLOT MACHINE
# ------------

async def slots(msg, pts):
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
    user = msg.author.name
    emotelist = ["PogChamp", "4Head", "NotLikeThis", "KappaPride", "DoritosChip"]
    e1 = emotelist[random.randint(0,len(emotelist) - 1)]
    e2 = emotelist[random.randint(0,len(emotelist) - 1)]
    e3 = emotelist[random.randint(0,len(emotelist) - 1)]

    if pts < 250:
        await msg.channel.send(f"@{msg.author.name} Bro you have to play with minimum 250 points")
        return

    if data[user][0] < pts:
        await msg.channel.send(f"@{msg.author.name} You do not have enough points for that ({data[user][0]}/{pts})")
        return
    
    if e1 == e2 and e2 == e3:
        await msg.channel.send(f"{e1} | {e2} | {e3} | @{msg.author.name} JACKPOT!! {randomemoji()} YOU'VE WON {pts * 15} POINTS")
        data[user] = data[str(user)][0] + pts * 10, data[str(user)][1]

        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)

        with open(logfile, "a") as w:
            w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} played slots for {pts} points and WON | Updated: {data[user][0]}\n")     
    
    else:
        await msg.channel.send(f"{e1} | {e2} | {e3} | @{msg.author.name} unfortunately, you've lost your {pts} points {randomemoji()}")
        data[user] = data[str(user)][0] - pts, data[str(user)][1]

        with open(logfile, "a") as w:
            w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} played slots for {pts} points and LOST | Updated: {data[user][0]}\n")    

        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)



# -----------
# ROLL POINTS
# -----------
            
async def roll(msg, number):
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
        userpts = data[str(msg.author.name)][0]
        if number < 100:
            await msg.channel.send(f'/me {msg.author.mention}, please enter a valid amount to roll. minimum 100 points.')
            return
        try:
            float(number)
        except:
            await msg.channel.send(f'/me {msg.author.mention}, please enter a valid amount to roll. minimum 100 points.')
            return
        if userpts < number:
            await msg.channel.send(f'/me {msg.author.mention}, you do not have enough points ({userpts}/{number}) {randomemoji()}')
            return
        else:
            n1 = random.randint(1,6)
            n2 = random.randint(1,6)

            if n1 == n2:
                c = random.randint(1,10)
                if c < 8:

                    data[str(msg.author.name)] = [data[str(msg.author.name)][0] + number * 5, data[str(msg.author.name)][1]]
                    await msg.channel.send(f'/me {msg.author.mention} rolled {n1} | {n2} with {number} points and won {randomemoji()} current points: {data[str(msg.author.name)][0]}')
                    with open(logfile, "a") as w:
                        w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} rolled {n1} | {n2} with {number} points and WON | Updated: {data[str(msg.author.name)][0]}\n")
                else:
                    data[str(msg.author.name)] = [data[str(msg.author.name)][0] - number, data[str(msg.author.name)][1]]
                    await msg.channel.send(f'/me {msg.author.mention} rolled {n1} | {n2} with {number} points and lost {randomemoji()} current points: {data[str(msg.author.name)][0]}')
                    with open(logfile, "a") as w:
                        w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} rolled {n1} | {n2} with {number} points and LOST | Updated: {data[str(msg.author.name)][0]}\n")

            else:
                data[str(msg.author.name)] = [data[str(msg.author.name)][0] - number, data[str(msg.author.name)][1]]
                await msg.channel.send(f'/me {msg.author.mention} rolled {n1} | {n2} with {number} points and lost {randomemoji()} current points: {data[str(msg.author.name)][0]}')
                with open(logfile, "a") as w:
                    w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{msg.author.name} rolled {n1} | {n2} with {number} points and LOST | Updated: {data[str(msg.author.name)][0]}\n")

        

        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)

# -----------
# SUGGESTIONS
# -----------
listofsuggestionusers = []
async def suggestion(message, suggestion):
    suggestion = " ".join(suggestion)
    time = datetime.datetime.now()
    if message.author.name not in listofsuggestionusers:
        listofsuggestionusers.append(message.author.name)
        webhook = DiscordWebhook(url=webhookurl, content=f"Suggestion from **{message.author.name}** ({time})\n**{suggestion}**")
        response = webhook.execute()
        await message.channel.send(f"@{message.author.name} Your Suggestion got sent!")
    elif message.author.name in listofsuggestionusers:
        webhook = DiscordWebhook(url=webhookurl, content=f"Suggestion from **{message.author.name}** ({time})\n**{suggestion}**")
        response = webhook.execute()
        await message.channel.send(f"@{message.author.name} Because you've already suggested something, it got marked as spam, but maybe i'll still read it.")





lurkingpeople = []
class Bot(commands.Bot):

    def __init__(self):
        with open("CREDENTIALS.txt", "r") as file:
            a = file.readlines()
            super().__init__(token=a[0].strip(), prefix='!', initial_channels=['f1shy312'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    
    activebingo = False
    rightemote = None
    async def event_message(self, message):
        if message.echo:
            return 
        words = message.content.split(" ")

        if len(words) >= 2 and words[0].lower() == '!settext':
            with open('data.pickle', 'rb') as f:
                data = pickle.load(f)
            user = words[1:]
            msg = " ".join(words[1:])
            userpts = data[str(message.author.name)][0]
            if userpts < 1000:
                await message.channel.send(f"@{message.author.name}, You do not have enough points to do that!")
            else:
                data[str(message.author.name)][0] = userpts - 1000
                with open("templates/latesttext", "w") as w:
                    w.write(f"{message.author.name}\n{msg}")

            with open('data.pickle', 'wb') as f:
                data = pickle.dump(data, f)


        if len(words) >= 1 and words[0].lower() == '!leaderboard':
            with open('data.pickle', 'rb') as f:
                data = pickle.load(f)
            top_5 = sorted((key, value) for key, value in data.items() if key not in admins)
            top_5 = top_5[:5]
            i = 1
            await message.channel.send(f"@{message.author.name} Leaderboard:")
            for key, value in top_5:
                if i == 1:
                    place = "🥇"
                elif i == 2:
                    place = "🥈"
                elif i == 3:
                    place = "🥉"
                else:
                    place = f"{i}."
                await message.channel.send(f"{place} @{key} : {value[0]}pts")
                i = i + 1


        if len(words) >= 2 and words[0].lower() == '!suggest':
            
            suggestionwords = words[1:]
            await suggestion(message, suggestionwords)

        if len(words) >= 1 and words[0].lower() == '!lurk':
            if message.author.name not in lurkingpeople:
                lurkingpeople.append(message.author.name)
                await message.channel.send(f"Thanks for the Lurk @{message.author.name}, have a good time!")
            else:
                lurkingpeople.remove(message.author.name)
                await message.channel.send(f"@{message.author.name} is back from lurking!")
            

        if len(words) >= 2 and words[0].lower() == '!roll':
            try:
                number = int(words[1])
                await roll(message, number)
            except ValueError:
                pass

        if len(words) >= 2 and words[0].lower() == '!emotebingo':
            global rightemote
            global activebingo
            if words[1].lower() == "start":
                if activebingo == False:
                    if message.author.name in admins:
                        rightemote = all_emotes[random.randint(0,len(all_emotes) - 1)]
                        activebingo = True
                        print(rightemote)
                        await message.channel.send(f"For 5000 points! The Chat need to guess one of all global twitch emotes {randomemoji()}")
                    else:
                        await message.channel.send(f"@{message.author.name} you do not have the permissions to do that, sorry!")
                else:
                    await message.channel.send(f"There is already one running rn. first stop it.")


            if words[1].lower() == "stop":
                if activebingo == True:
                    if message.author.name in admins:
                        rightemote = None
                        activebingo = False
                        await message.channel.send(f"Ended the Emote-Bingo | No winners! {randomemoji()}")
                    else:
                        await message.channel.send(f"@{message.author.name} you do not have the permissions to do that, sorry!")
                else:
                    await message.channel.send(f"No bingo active rn.")


        if len(words) >= 2 and words[0].lower() == '!giveaway':
            global prize
            global listofusers
            if words[1].lower() == "reset":
                if message.author.name in admins:
                    listofusers = []
                    prize = "None"
                    await message.channel.send(f"Giveaway list resetted.")
                else:
                    await message.channel.send(f"@{message.author.name} you do not have the permissions to do that, sorry!")
        
            
            if len(words) >= 3:
                try:
                    mode = words[1]
                    prize = words[2:]
                    await giveaway(message, mode, prize)
                except ValueError:
                    pass
            if len(words) == 2:
                try:
                    mode = words[1]
                    prize = prize
                    await giveaway(message, mode, prize)
                except ValueError:
                    pass

            


        if len(words) >= 1 and words[0].lower() == '!rob':
            if len(words) == 2:
                user = words[1]
                if user[0] == "@":
                    user = user[1:]
                await rob(message, user)
            else:
                await message.channel.send(f"{message.author.mention} usage: !rob @user")

        if len(words) >= 0 and words[0].lower() == '!sfx':
            
            try:
                song = words[1]
            except IndexError:
                song = "help"
                
            
            await sfx(message, song)
            


        if len(words) >= 1 and words[0].lower() == '!points':
            if len(words) == 1:
                await points(message, message.author.name)
            if len(words) >= 2:
                await points(message, words[1])
        if len(words) >= 1 and words[0].lower() == '!pts':
            if len(words) == 1:
                await points(message, message.author.name)
            if len(words) >= 2:
                await points(message, words[1])
            

        if len(words) >= 2 and words[0].lower() == '!gamble':
            try:
                number = int(words[1])
                await gamblef(message, number)
            except ValueError:
                pass

        if len(words) >= 2 and words[0].lower() == '!slots':
            try:
                number = int(words[1])
                await slots(message, number)
            except ValueError:
                pass

        if len(words) >= 3 and words[0].lower() == '!setpts':
            try:
                user = words[1]
                if user[0] == "@":
                    user = user[1:]



                number = int(words[2])
                await adminset(message, user, number)
            except ValueError:
                pass

        

        
        if len(words) >= 3 and words[0].lower() == '!pay':
            try:
                user = words[1]
                if user[0] == "@":
                    user = user[1:]


                    
                number = int(words[2])
                await pay(message, user, number)
            except ValueError:
                pass

        if len(words) >= 0 and words[0].lower() == '!help':
            await message.channel.send("more infos abt commands here: <website>")


        with open('data.pickle', 'rb') as f:
            data = pickle.load(f)


        if not message.author.name in data:
            data[str(message.author.name)] = [0,0]
            with open(logfile, "a") as w:
                w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}Created data for User {message.author.name}\n")
            print("created data for new chatter " + message.author.name)
        else:
            if message.content[0] != "":
                print(f"+ 10 pts for {message.author.name} ({data[str(message.author.name)][0] + 10})")
                data[str(message.author.name)] = [data[str(message.author.name)][0] + 10, data[str(message.author.name)][1]]
                with open(logfile, "a") as w:
                    w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{message.author.name} got +10 pts for chatting | Updated: {data[str(message.author.name)][0]} | MESSAGE: {message.content}\n")                                         

        if activebingo == True:
            if rightemote != None:
                if rightemote in words:
                    await message.channel.send(f"Congrats to @{message.author.name} for guessing the right Emote ({rightemote}) and winning 5000 points")
                    data[str(message.author.name)] = [data[str(message.author.name)][0] + 5000, data[str(message.author.name)][1]]
                    with open(logfile, "a") as w:
                        w.write(f"{str(datetime.datetime.today().strftime('%H:%M:%S - '))}{message.author.name} WON 5000 POINTS IN THE EMOTE BINGO | Updated: {data[str(message.author.name)][0]}\n")                                         

                    rightemote = None
                    activebingo = False


        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)

        await self.handle_commands(message)

        





        
        


bot = Bot()
bot.run()
