from os import access
import discord
import json
import time
import requests

with open('config.json') as f:
    config = json.load(f)
Token = config.get("Token")
password = config.get("pass")


option = int(input("[1] Save account \n\n[2] Restore an account(no)\n\n>"))

dataE = '{"max_age":0,"max_uses":0,"temporary":false}'

headers = {
    'Content-Type':'application/json',
    'Authorization': Token,
}

def save():
    bot = discord.Client()
    print('logging in to discord...成功')
    @bot.event
    async def on_ready():
        print("saving using settings from config\n ")
        print(f"logged into {bot.user.name}")

        with open(f'Saves/{bot.user.id}.dcsave', 'w') as f:
            f.write('{"friends": [],"blocked": [],"guilds":[]}')

        def write_json(data, filename = F"Saves/{bot.user.id}.dcsave"):
            with open (filename, "w") as f:
                json.dump(data, f, indent=2)
            
        savefriends = config.get('saveFriends')
        saveBlocked = config.get('saveBlocked')
        saveguilds = config.get('saveguilds')

        if savefriends == "true":
            print('Saving friends...')
            for friend in bot.user.friends:
                friendlist = (friend.name)+'#'+(friend.discriminator)
                with open (F"Saves/{bot.user.id}.dcsave") as json_file:
                    data = json.load(json_file)
                    users = data ["friends"]
                    banUse = (friendlist)
                    users.append(banUse)
                    write_json(data)
            print('done')
                
        if saveBlocked == "true":
            print('Saving blocked...')
            for block in bot.user.blocked:
                blocklist = (block.name)+'#'+(block.discriminator)
                with open (F"Saves/{bot.user.id}.dcsave") as json_file:
                    data = json.load(json_file)
                    blocked = data ["blocked"]
                    blocked.append(blocklist)
                    write_json(data)
            print('done')

        
        if saveguilds == "true":
            print("Saving guilds...")
            guilds = await bot.fetch_guilds(limit=200).flatten()
            print(f'found {len(guilds)} guilds ')
            for guild in guilds:
                guild = bot.get_guild(guild.id)
                for channel in guild.text_channels:
                    r=requests.get(f"https://discord.com/api/v9/channels/{channel.id}",headers=headers)
                    if r.status_code ==200:
                        r = requests.post(f'https://discord.com/api/v9/channels/{channel.id}/invites',data=dataE,headers=headers)
                        inv = r.json()
                        inv = inv.get('code')
                        invite = f'https://discord.gg/{inv}'
                        if str(inv) == '50013' or str(inv) == '10003':
                            r = requests.get(f'https://discord.com/api/v9/guilds/{guild.id}',headers=headers)
                            try:
                                invite = 'https://discord.gg/'+r.json().get('vanity_url_code')
                            except:
                                pass
                            if str(invite) == 'https://discord.gg/50013' or str(invite) == 'https://discord.gg/10003':
                                print(f'failed to create invite for guild {guild.name}')
                                break
                            else:
                                with open (F"Saves/{bot.user.id}.dcsave") as json_file:
                                    data = json.load(json_file)
                                    guild = data ["guilds"]
                                    guild.append(invite)
                                    write_json(data)
                                    time.sleep(5)
                                break
                        else:
                            with open (F"Saves/{bot.user.id}.dcsave") as json_file:
                                data = json.load(json_file)
                                guild = data ["guilds"]
                                guild.append(invite)
                                write_json(data)
                                time.sleep(5)
                            break
            print('done')
        

        print(f"{bot.user.name} was Saved")
        input()
        exit(1)

        
    bot.run(Token, bot=False)

if option == 1:
    save()

 
