import discord
from discord.ext import commands
from riotwatcher import LolWatcher
import requests
import json
from test import all_champions


lol_key = 'SECRET CODE'
discord_key = 'SECRET CODE'

bot = commands.Bot(command_prefix=';')





@bot.event
async def on_ready():
    print('I am ready')

@bot.command()
async def test(ctx, *,  username):



    lol = LolWatcher(lol_key)
    summoner = lol.summoner.by_name('ru', username)
    stats = lol.league.by_summoner('ru', summoner['id'])
    data = lol.data_dragon.items(version='11.4.1')


    itemslol = []

    for j in data['data']:
        itemslol.append(j)

    with open('items.json', 'w') as f:
        json.dump(itemslol,f)


    champion_mastery = lol.champion_mastery.by_summoner('ru' , (summoner['id']))

    matchlist = lol.match.matchlist_by_account('ru', str(summoner['accountId']))




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

    for i in lol.data_dragon.champions(version='11.3.1')['data']:
        print(i)


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
***Main champions 🥇 ***
**1** :  {champemoji1} *{all_champions[champion_mastery[0]['championId']]}* [*Points:* **{championpoints1}**]{champicon1}
**2** :  {champemoji2} *{all_champions[champion_mastery[1]['championId']]}* [*Points:* **{championpoints2}**]{champicon2}
**3** :  {champemoji3} *{all_champions[champion_mastery[2]['championId']]}* [*Points:* **{championpoints3}**]{champicon3}

**Rank**
*SoloQ* : **{RankSoloQ}**
*Flex* : **{RankFlex}**

**History**
  """)
    for i in range(4):

        champplayedid = matchlist['matches'][i]['champion']


        match = lol.match.by_id('ru', matchlist['matches'][i]['gameId'])

        print(matchlist['matches'][i])
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

                em.add_field(name = f'**Victory** - {queue}'if match['participants'][j]['stats']['win'] == True else f'**Defeat** - {queue}',
                value = f'{emojiforhistory} {kills}/{deaths}/{assists} -  {item0}{item1}{item2}{item3}{item4}{item5}{item6}', inline=False)
    em.set_thumbnail(url = f'http://lolg-cdn.porofessor.gg/img/summonerIcons/11.4/64/{IconId}.png')
    await ctx.send(embed = em)

bot.run(discord_key)
