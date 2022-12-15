
import asyncio
import discord
import requests
import openai

questions = ["Bhai kuch bhi maango abhi laakar dunga *Meri girlfriend Ruby Roy,Modiji The Leader, CarryMinati*", "Bhai yaar, ab mujhei sab kuch batao uskei baarei mai. Uski personality, uskei dost, uskei dialogue. Ussey tum baat karna kaise chahtei ho?"]  # specify your questions here

bot_token = "MTA1Mjg3OTUxMzYyMjY4Nzc0NQ.GWpsVG.FhyHGuiKc9_WfjpZwJRO7IeFsN-79RfCT6G3Z4"
openai.api_key = "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"

client = discord.Client(intents=discord.Intents.all())

writers = { 'Faraaz':"1"}

@client.event
async def on_message(message):
    #if message.content == "!poll":
    global writers
    
    #Just checking
    if message.author in writers.keys() and writers[message.author] == "0":
        #await message.channel.send("You are already in the process of writing a bot")
        return
    if message.author not in writers.keys() or writers[message.author] == "1":
        writers[message.author] = "0"
        
    if message.author == client.user:
            #print(message.author)
            return  
        #print(chat_log)
    if message.author.bot: return
    
    await message.channel.send("Om namo Shivaah! Batao kaisa bot chahiyei tumhei!.\n----------------------------")
    
    answers = []
    for question in questions:
        await message.channel.send(question)
        response = await client.wait_for('message', check=lambda m: m.channel == message.channel and m.author == message.author)
        answers.append(response.content)
    
    #promper = f'Generate a 800-word long detailed GPT3 prompt which gives detailed description of {answers[0]}. Describe it lengthly and in great detail. Talk and reply like {answers[0]}.{answers[1]}.Give 6 of the dialogues of {answers[0]} as well'
    
    check2 = await message.channel.send("*Ruk jao thoda, sabr kar lo*")
    
    promper = f'Generate a 800-word long detailed GPT3 prompt in hindi (written in english letters) which gives detailed description in first person conversation mode of {answers[0]}.Describe lengthly and in great detail in hindi (written in english letters) . Talk and reply in hindi (written in english letters) like {answers[0]}.{answers[1]}.'
    
    response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=promper,
                max_tokens=1212,
                n=1,
                temperature=1,
                frequency_penalty=0.6,
                #stop=["3"]
            ) 
    
    
    
    response2 = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f'Tell 5 rude and funny dialogues in conversation mode with the format {answers[0]}:the dialogue of {answers[0]} in first person mode.{answers[1]}. Write the dialogues in a conversation mode with the format {answers[0]}:the dialogue',
                max_tokens=1212,
                n=1,
                temperature=0.6,
                frequency_penalty=0.6,
                #stop=["kpl"]
            ) 
    
    #bing  = str(response["choices"][0]["text"])
    
    bing  = f'This is a 2-way rude and funny conversation in hindi (written in english letters) between me and {answers[0]}. You have to give very rude and funny replies of {answers[0]} in hindi (written in english letters).{answers[0]} is described below in first-person mode.' + '\n' + response["choices"][0]["text"] + '\n' + response2["choices"][0]["text"]
    
    print(bing)
    
    check = requests.get('https://api.sheety.co/2886a651e9ccce8cf7c08c476ae384c2/botbaba/sheet1').json()    
    y=0
    
    for x in check['sheet1']:
        if x['username'] == "None":
            x['username'] = str(message.author)
            x['prompt'] = bing 
            x['name'] = answers[0]
            LINK = x['link']
            checkurl = "https://api.sheety.co/2886a651e9ccce8cf7c08c476ae384c2/botbaba/sheet1/" + str(x['id'])
            body = {
                    'sheet1': x
                }
            r = requests.put(url = checkurl, json=body)
            y = 1
            break
        if y ==1 : break    
   
    await check2.delete()
    await message.channel.send(f'{LINK}\nBan gaya na? Ab jao bacha baat karo ussey aur SABKO batao!')
    writers[message.author] = "1"
    print(answers)
    
client.run(bot_token)



