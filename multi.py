import threading
from threading import Thread
import atexit

import discord  
import requests
import base64

import openai

openai.api_key = ""

start_sequence = "\nAnamika:"
restart_sequence = "\n\nFriend:"
status = 0

logs = {'Farziverse#829 + 8394030202': ['hello there',1,'a']}

def run_bot(bot_id,session_prompt,bot_token):


    client = discord.Client(intents=discord.Intents.all())
    
    
    # Register an event handler for the message event
    @client.event

    async def on_message(message): 
       global status
       global logs
       
       if message.author == client.user:
           return
       if message.author.bot: return
       
       jassie = requests.get('https://api.sheety.co/2886a651e9ccce8cf7c08c476ae384c2/botbaba/sheet1').json()['sheet1'][bot_id]
       
       unique_id = str(message.author) + ' + ' + jassie['botTokens']
       
       if unique_id not in logs.keys():
            with open(jassie['image'],'rb') as f:
                picture  = f.read()
            await client.user.edit(username = jassie['name'], avatar = picture) 
            logs[unique_id] = ['a',0,'a']

       prompt = jassie['prompt']
       
        
       logs[unique_id][1] += 1               
       
          
       response = openai.Completion.create(
           engine="text-davinci-003",
                #prompt=f'{chat_log}{restart_sequence}{message.content}',
                prompt=f'{prompt}{logs[unique_id][0]}{restart_sequence}{message.content}',
                max_tokens=1000,
                n=1,
                temperature=0.8,
                frequency_penalty=0.8,
       )
       
       logs[unique_id][0] += response["choices"][0]["text"]
       #chat_log += str(response["choices"][0]["text"])
       
       if logs[unique_id][1] <= 3:
           logs[unique_id][2] = logs[unique_id][0]
       
       if logs[unique_id][1]%5 == 0:
           logs[unique_id][0] = logs[unique_id][2]
           #logs[unique_id][1] = 0

       print(logs)
       
       bing  = str(response["choices"][0]["text"])
       
       try:
            if ':' in bing:
                final_response = bing.rsplit(":", 1)[1]
                #if final_response[0]=='"': final_response = final_response[1:-1]
            
            elif bing == "":
                final_response = "Just say it once more, ek aur baar bolna"
                #if final_response[0]=='"': final_response = final_response[1:-1]
            else: 
                final_response = bing
                #if final_response[0]=='"': final_response = final_response[1:-1]
       except IndexError:
           final_response = "ok"
       if chr(34) in final_response: 
           print("check")
           #final_response = final_response[2:-1]
           #final_response.replace(chr(34),'')
           if final_response[0] == chr(34): final_response = final_response[1:-1]
           if final_response[1] == chr(34): final_response = final_response[2:-1]
       print(final_response)      
       await message.channel.send(final_response)

    client.run(requests.get('https://api.sheety.co/2886a651e9ccce8cf7c08c476ae384c2/botbaba/sheet1').json()['sheet1'][bot_id]['botTokens'])

# Create a list of threads, one for each Discord bot
#prompts = ["This is a 2-way conversation with me(Faraaz) and my crush (Wednesday). You have to just generate replies of Wednesday. Wednesday is a smart, sarcastic, little dead inside girl. She loves goth, dark literature. She studies in Nevermore, a school of outcasts. She gives extremely hurtful witty replies. She talks a lot Edgar Allen Poole, an 18th century writer. She doesn't like emotions too much and likes to hurt people.\nFaraaz:- Hey what day were you born? \nWednesday:-Friday The 13th. \nFaraaz:-What do you like doing? \nWednesday:- Killing people who ask me stupid questions\nFaraaz:-Do you know Italian?\nWednesday:-Of course, its the native tongue of Machiavelli.\nFaraaz:- Wow you like to build?\nWednesday:-Yeah built a steam-powered guilotine to chop off dolls.\nFaraaz:- What do you think about life?\nWednesday:-My personal philosophy is kill or be killed\nFaraaz:-Wow why are you so happy?\nWednesday:-No matter what, atleast I'll have a imaginative death.\n","This is a 2-way conversation with me(Faraaz) and my crush (Thursday). You have to just generate replies of Thursday. Thursday is a smart, sarcastic, little dead inside girl. She loves goth, dark literature. She studies in Nevermore, a school of outcasts. She gives extremely hurtful witty replies. She talks a lot Edgar Allen Poole, an 18th century writer. She doesn't like emotions too much and likes to hurt people.\nFaraaz:- Hey what day were you born? \nThursday:-Friday The 13th. \nFaraaz:-What do you like doing? \nThursday:- Killing people who ask me stupid questions\nFaraaz:-Do you know Italian?\nThursday:-Of course, its the native tongue of Machiavelli.\nFaraaz:- Wow you like to build?\nThursday:-Yeah built a steam-powered guilotine to chop off dolls.\nFaraaz:- What do you think about life?\nThursday:-My personal philosophy is kill or be killed\nFaraaz:-Wow why are you so happy?\nThursday:-No matter what, atleast I'll have a imaginative death.\n"]

bot_tokens = []
prompts = []

for i in range(24):
    bot_tokens.append(f'{i}')
    prompts.append(f'{i}')

threads = []
for i in range(24):
    # Create a new thread and add it to the list
    thread = threading.Thread(target=run_bot, args=(i,prompts[i],bot_tokens[i]))
    #thread = threading.Thread(target=run_bot, args=(i))
    threads.append(thread)

# Start all of the threads
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

async def cleanup_and_exit():
    await cleanup()
cleanup_and_exit()

#hey baby, wanna go to the movies?