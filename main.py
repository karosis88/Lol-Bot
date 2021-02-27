import discord
from discord.ext import commands
from riotwatcher import LolWatcher
import json
from champions import *
from datetime import datetime
from imgurrlol import imgurr








lol_key = secret
discord_key = secret

bot = commands.Bot(command_prefix='r>')
lol = LolWatcher(lol_key)





serverliststr = ['ru', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1']

bot.remove_command('help')







@bot.event
async def on_ready():
    print('I am ready')


    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="r>help"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(embed = discord.Embed(colour=discord.Colour.red(), description=f"""{ctx.author.mention} , **Command {ctx.message.content} not found**
```Use r>help```"""))



@bot.command()
async def stat(ctx, server, *, username):
    try:
        guild = ctx.guild
    except AttributeError:
        return

    with open('guildlanguage.json', 'r') as f:
        guildlanguage = json.load(f)

    if str(ctx.guild.id) not in guildlanguage:
        guildlanguage[str(ctx.guild.id)] = 'languageeng'

    with open('guildlanguage.json', 'w') as f:
        json.dump(guildlanguage, f)

    with open('guildlanguage.json', 'r') as f:
        guildlanguage = json.load(f)

    if guildlanguage[str(ctx.guild.id)] == 'languageeng':
        language = languageeng
    else:
        language = languageru


    if server.lower() not in serverliststr:
        return await ctx.send(embed = discord.Embed(colour=discord.Colour.red(), description=f"""{ctx.author.mention} , {language['stats'][1]} **{server}** {language['stats'][2]}
*{language['stats'][3]}*```
ru
eun1
euw1
jp1
kr
la1
la2
na1
oc1
tr1
```"""))


    try:
        summoner = lol.summoner.by_name(server, username)
    except:
        return await ctx.send(embed = discord.Embed(colour=discord.Colour.red(), description=language['stats'][4]))
    stats = lol.league.by_summoner(server, summoner['id'])



    champion_mastery = lol.champion_mastery.by_summoner(server , (summoner['id']))

    matchlist = lol.match.matchlist_by_account(server, str(summoner['accountId']))




    champid1 = str(champion_mastery[0]['championId'])
    if len(champid1) == 1:
        champid1 = f'{champid1}_'

    champid2 = str(champion_mastery[1]['championId'])
    if len(champid2) == 1:
        champid2 = f'{champid2}_'

    champid3 = str(champion_mastery[2]['championId'])
    if len(champid3) == 1:
        champid3 = f'{champid3}_'


    champemoji1 = None
    champemoji2 = None
    champemoji3 = None

    championpoints1 = champion_mastery[0]['championPoints']
    championpoints2 = champion_mastery[1]['championPoints']
    championpoints3 = champion_mastery[2]['championPoints']

    championplvl1 = champion_mastery[0]['championLevel']
    championplvl2 = champion_mastery[1]['championLevel']
    championplvl3 = champion_mastery[2]['championLevel']

    champicon1 = f'*Rank:* ({str(championplvl3)})'
    champicon2 = f'*Rank:* ({str(championplvl3)})'
    champicon3 = f'*Rank:* ({str(championplvl3)})'

    IconId = summoner['profileIconId']
    RankSoloQ = None
    RankFlex = None

    item0 = None
    item1 = None
    item2 = None
    item3 = None
    item4 = None
    item5 = None
    item6 = None

    noniconguild = bot.get_guild(687742674689589281)
    for nonicon in noniconguild.emojis:
        if nonicon.name == 'nonicon':
            item0 = item1 = item2 = item3 = item4 = item5 = item6 = nonicon



    for guildid in [804442853107171398, 803679741281566720, 803643924068565033, 813748721354932256]:
        guild = bot.get_guild(guildid)
        for emoji in guild.emojis:
            if emoji.name == champid1:
                champemoji1= emoji
            if emoji.name == champid2:
                champemoji2 = emoji
            if emoji.name == champid3:
                champemoji3 = emoji


    guildforranks = bot.get_guild(687742674689589281)
    for emoji in guildforranks.emojis:
        if emoji.name == f'lvl{championplvl1}':
            champicon1 = emoji
        if emoji.name == f'lvl{championplvl2}':
            champicon2 = emoji
        if emoji.name == f'lvl{championplvl3}':
            champicon3 = emoji

    for i in stats:
        try:
            if i['queueType'] == 'RANKED_SOLO_5x5':
                RankSoloQ = i['tier'] + ' ' + i['rank']
        except:
            if i['queueType'] == 'RANKED_FLEX_SR':
                RankFlex = i['tier'] + ' ' + i['rank']



    em = discord.Embed(colour=0xFFFF00, title= 'Information about '+ username, description=f"""
***{language['stats'][5]} 🥇 ***
**1** :  {champemoji1} *{all_champions[champion_mastery[0]['championId']]}* [*{language['stats'][6]}:* **{championpoints1}**]{champicon1}
**2** :  {champemoji2} *{all_champions[champion_mastery[1]['championId']]}* [*{language['stats'][6]}:* **{championpoints2}**]{champicon2}
**3** :  {champemoji3} *{all_champions[champion_mastery[2]['championId']]}* [*{language['stats'][6]}:* **{championpoints3}**]{champicon3}

**{language['stats'][7]}**
*SoloQ* : **{RankSoloQ}**
*Flex* : **{RankFlex}**

**{language['stats'][8]}**
  """)
    for i in range(7):

        champplayedid = matchlist['matches'][i]['champion']


        match = lol.match.by_id(server, matchlist['matches'][i]['gameId'])


        queue = matchlist['matches'][i]['queue']

        if queue == 420:
            queue = 'Ranked - SoloQ'
        elif queue == 440:
            queue = 'Ranked - Flex'
        elif queue == 400:
            queue = 'Normal (Draft Pick)'
        elif queue == 430:
            queue = 'Normal (Blind Pick)'
        elif queue == 450:
            queue = 'ARAM'
        elif queue == 700:
            queue = 'Clash'


        for j in range(10):

            emojiforhistory = None

            if champplayedid == match['participants'][j]['championId']:

                if len(str(champplayedid)) == 1:
                    champplayedid = f'{champplayedid}_'

                for guildid in [804442853107171398, 803679741281566720, 803643924068565033, 813748721354932256]:
                    guild = bot.get_guild(guildid)
                    for emoji in guild.emojis:
                        if emoji.name == str(champplayedid):

                            emojiforhistory = emoji


                for guildid in [813734113995522079, 813733770837491723, 452016802315370506, 510883071026003991]:
                    guild = bot.get_guild(guildid)
                    for emoji in guild.emojis:
                        if emoji.name == str(match['participants'][j]['stats']['item0']):
                            item0 = emoji
                        elif emoji.name == str(match['participants'][j]['stats']['item1']):
                            item1 = emoji
                        elif emoji.name == str(match['participants'][j]['stats']['item2']):
                            item2 = emoji
                        elif emoji.name == str(match['participants'][j]['stats']['item3']):
                            item3 = emoji
                        elif emoji.name == str(match['participants'][j]['stats']['item4']):
                            item4 = emoji
                        elif emoji.name == str(match['participants'][j]['stats']['item5']):
                            item5 = emoji
                        elif emoji.name == str(match['participants'][j]['stats']['item6']):
                            item6 = emoji

                kills = match['participants'][j]['stats']['kills']
                deaths = match['participants'][j]['stats']['deaths']
                assists = match['participants'][j]['stats']['assists']
                gameduration = int(match['gameDuration'])
                min = gameduration//60
                sec = gameduration%60
                if len(str(sec)) == 1:
                    sec = f'0{sec}'


                em.add_field(name = f'**{language["stats"][9]}** - {queue}'if match['participants'][j]['stats']['win'] == True else f'**{language["stats"][10]}** - {queue}',
                value = f'{emojiforhistory} {kills}/{deaths}/{assists} -  {item0}{item1}{item2}{item3}{item4}{item5}{item6} {min}:{sec} ', inline=False)
                em.set_image(url=f'{imgurr[int(champid1)]}')
    em.set_thumbnail(url = f'http://ddragon.leagueoflegends.com/cdn/11.4.1/img/profileicon/{IconId}.png')
    await ctx.send(embed = em)

@stat.error
async def lolstaterror(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed = discord.Embed(colour=discord.Colour.red(), description=f"""{ctx.author.mention} ***Invalid syntax***, *try*
```
r>stat [server] [nickname]
For example r>stat ru kar88
Check available server with command : r>serverlist
```"""))

@bot.command()
async def serverlist(ctx):
    try:
        guild = ctx.guild
    except AttributeError:
        return

    with open('guildlanguage.json', 'r') as f:
        guildlanguage = json.load(f)

    if guildlanguage[str(ctx.guild.id)] == 'languageeng':
        language = languageeng
    else:
        language = languageru

    await ctx.send(
        embed=discord.Embed(colour=discord.Colour.red(), description=f"""
    *{language['stats'][3]}*```
ru
eun1
euw1
jp1
kr
la1
la2
na1
oc1
tr1
```"""))

@bot.command()
async def help(ctx):

    with open('guildlanguage.json', 'r') as f:
        guildlanguage = json.load(f)

    if guildlanguage[str(ctx.guild.id)] == 'languageeng':
        language = languageeng
    else:
        language = languageru

    await ctx.send(
        embed=discord.Embed(colour=discord.Colour.red(), description=f"""
        ***{language['help'][5]}***
`r>stat [{language['error'][1]}] [{language['error'][4]}]` - {language['help'][1]} [{language['error'][4]}], {language['help'][2]}
`r>serverlist` - {language['help'][3]}
`r>clashinfo [{language['error'][1]}]` - {language['help'][4]}
`r>changelng ` - {language['error'][7]}
"""))

@bot.command()
async def clashinfo(ctx, server):

    with open('guildlanguage.json', 'r') as f:
        guildlanguage = json.load(f)

    if guildlanguage[str(ctx.guild.id)] == 'languageeng':
        language = languageeng
    else:
        language = languageru

    if server.lower() not in serverliststr:
        return await ctx.send(embed=discord.Embed(colour=discord.Colour.red(),
                                                  description=f"""{ctx.author.mention} , {language['stats'][1]} **{server}** {language['stats'][2]}
        *{language['stats'][3]}*```
ru
eun1
euw1
jp1
kr
la1
la2
na1
oc1
tr1
```"""))

    clash = lol.clash.tournaments(server)
    em = discord.Embed()
    for i in range(len(clash)):
        name = clash[i]['nameKey']
        startTime = int(clash[i]['schedule'][0]['startTime'])
        datastart = datetime.fromtimestamp(float(startTime)/1000.)
        month = language['monthnames'][datastart.month]
        em.add_field(name = name.title(), value= f'{month} {datastart.day} {datastart.year} {datastart.strftime("%H:%M:%S")}')

    em.set_image(url = 'https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt7cfcbef1c7754ca4/5e3b50211ff22e62a7ce690e/CLASH2020_T2_CLIENT_1920x1080_ARTICLE_IMAGE_FINAL.jpg')
    await ctx.send(embed = em)

@clashinfo.error
async def clashinfoerror(ctx, error):

    with open('guildlanguage.json', 'r') as f:
        guildlanguage = json.load(f)

    if guildlanguage[str(ctx.guild.id)] == 'languageeng':
        language = languageeng
    else:
        language = languageru

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(colour=discord.Colour.red(), description=f"""{ctx.author.mention} {language['error'][5]}
```
r>clashinfo [{language['error'][1]}]
{language['error'][2]} r>clashinfo euw1
{language['error'][3]} r>serverlist
```"""))

# @bot.command()
# async def clash(ctx, server, username):
#     if server.lower() not in serverliststr:
#         await ctx.send(
#             embed=discord.Embed(colour=discord.Colour.red(), description=f"""{ctx.author.mention} , Server **{server}** not found
#     *There is all available servers:*```
#     ru
#     eun1
#     euw1
#     jp1
#     kr
#     la1
#     la2
#     na1
#     oc1
#     tr1
#     ```"""))
#
#     summoner = lol.summoner.by_name(server, username)
#     clashbyusername = lol.clash.by_summoner(server, summoner['id'])
#     print(clashbyusername)

@bot.command()
@commands.has_permissions(administrator=True)
async def changelng(ctx):
    try:
        guild = ctx.guild
    except AttributeError:
        return



    with open('guildlanguage.json', 'r') as f:
        guildlanguage = json.load(f)



    if str(ctx.guild.id) not in guildlanguage:
        guildlanguage[str(ctx.guild.id)] = 'languageeng'

    with open('guildlanguage.json', 'w') as f:
        json.dump(guildlanguage, f)

    with open('guildlanguage.json', 'r') as h:
        guildlanguage = json.load(h)

    if guildlanguage[str(ctx.guild.id)] == "languageeng":
        guildlanguage[str(ctx.guild.id)] = "languageru"
    else:
        guildlanguage[str(ctx.guild.id)] = "languageeng"

    with open('guildlanguage.json', 'w') as h:
        json.dump(guildlanguage, h)

    if guildlanguage[str(ctx.guild.id)] == 'languageeng':
        language = languageru
    else:
        language = languageeng

    await ctx.send(embed = discord.Embed(colour=discord.Colour.red(), description= language['error'][6]))

@bot.command()
async def topplayers(ctx, server):
    def get_points(employee):
        return employee.get('leaguePoints')
    topplayers = lol.league.challenger_by_queue(server , 'RANKED_SOLO_5x5')
    topplayers = topplayers['entries']
    sortedTopplayers = sorted(topplayers, key=get_points , reverse=True)

    # entries
    toplist = {
        'topinfo1' : [],
        'topinfo2' : [],
        'topinfo3' : [],
        'topinfo4' : [],
        'topinfo5' : [],
        'topinfo6' : [],
        'topinfo7' : [],
        'topinfo8' : [],
        'topinfo9' : [],
        'topinfo10' : [],}

    for i in range(10):
        toplist[f'topinfo{i + 1}'].append(sortedTopplayers[i]['summonerName'])
        toplist[f'topinfo{i + 1}'].append(sortedTopplayers[i]['leaguePoints'])



    em = discord.Embed(colour=discord.Colour.dark_blue(), title=f'**Top Players {server}**', description= f"""
**1** : ` {toplist['topinfo1'][0]} `  ***{toplist['topinfo1'][1]}*** LP
**2** : ` {toplist['topinfo2'][0]} `   ***{toplist['topinfo2'][1]}*** LP
**3** : ` {toplist['topinfo3'][0]} `   *** {toplist['topinfo3'][1]}*** LP
**4** : ` {toplist['topinfo4'][0]} `   *** {toplist['topinfo4'][1]}*** LP
**5** : ` {toplist['topinfo5'][0]} `   *** {toplist['topinfo5'][1]}*** LP
**6** : ` {toplist['topinfo6'][0]} `   *** {toplist['topinfo6'][1]}*** LP
**7** : ` {toplist['topinfo7'][0]} `  *** {toplist['topinfo7'][1]}*** LP
**8** : ` {toplist['topinfo8'][0]} `  *** {toplist['topinfo8'][1]}*** LP
**9** : ` {toplist['topinfo9'][0]} `  *** {toplist['topinfo9'][1]}*** LP
**10** : ` {toplist['topinfo10'][0]} `  *** {toplist['topinfo10'][1]}*** LP""")

    msg = await ctx.send(embed = em)

    guild = bot.get_guild(804442853107171398)
    mekemoji = discord.utils.get(guild.emojis, name = '_1')
    rightemoji = discord.utils.get(guild.emojis, name = 'right')

    await msg.add_reaction(mekemoji)
    await msg.add_reaction(rightemoji)




bot.run(discord_key)
