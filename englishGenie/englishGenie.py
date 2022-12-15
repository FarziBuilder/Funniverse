import asyncio
import discord
import requests
import openai

questions = ["FIRST question what character do you want in the bot huh! Just tell me *Shahrukh Khan as Devdas*, *Your dog Rio?*, *A Cheese which talks*", "Ohhh interesting, NOW tell me everything about this character. His personality, his jokes, who are his friends EVERYTHING"]  # specify your questions here

bot_token = ""
openai.api_key = ""

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
    
    await message.channel.send("Ok comrade, answer my questions amazingly and I pinki promise I'll give you a bot.\n----------------------------")
    
    answers = []
    for question in questions:
        await message.channel.send(question)
        response = await client.wait_for('message', check=lambda m: m.channel == message.channel and m.author == message.author)
        answers.append(response.content)
    
    check2 = await message.channel.send("*Wait up comrade, I am brewing ur bot!*")
    
    #promper = f'Generate a 800-word long detailed GPT3 prompt which gives detailed description of {answers[0]}. Describe it lengthly and in great detail. Talk and reply like {answers[0]}.{answers[1]}.Give 6 of the dialogues of {answers[0]} as well'
    
    promper = f'Generate a 800-word long detailed GPT3 prompt which gives detailed description in first person conversation mode of {answers[0]}.Describe lengthly and in great detail. Talk and reply like {answers[0]}.{answers[1]}.'
    
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
    
    bing  = f'This is a 2-way rude and funny conversation between me and {answers[0]}. You have to give very rude and funny replies of {answers[0]}.{answers[0]} is described below in first-person mode.' + '\n' + response["choices"][0]["text"] + '\n' + response2["choices"][0]["text"]
    
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
    
    await message.channel.send(f'{LINK}\nYoohoo! your bot is ready. Go add it to any server and talk to it.')
    writers[message.author] = "1"
    print(answers)
    
client.run(bot_token)
