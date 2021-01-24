import discord
from datetime import datetime
from discord.ext import commands
import os
import youtube_dl
from datetime import datetime
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler

client = commands.Bot(command_prefix="//")
datetime = datetime.now()

@client.command()
async def change(ctx, arg1:str):
    songexists = os.path.isfile("song.mp3")
    try:
        if songexists:
            os.remove("song.mp3")
    except PermissionError:
        ctx.send("Zastav momentalne hrajucu hudbu")
        return

    ydlOpts= {
        'format':'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydlOpts) as ydl:
        ydl.download([arg1])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")




@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Bot nieje nikde pripojený")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Nič momentálne nehrá")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Nič nieje pauznuté")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
@client.command()
async def play(ctx):
    voicechannel=discord.utils.get(ctx.guild.voice_channels, name="Škola (Hlasová miestnosť)")
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()            
        await voicechannel.connect()
    except UnboundLocalError or AttributeError:
        await voicechannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


async def TestTimeOn():
    print(datetime.now().time())
    if datetime.now().hour==8:
        voicechannel=discord.utils.get(ctx.guild.voice_channels, name="Škola (Hlasová miestnosť)")
        try:
            voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
            if voice.is_connected():
                await voice.disconnect()            
            await voicechannel.connect()
        except UnboundLocalError or AttributeError:
            await voicechannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
    if datetime.now().hour==9:
        voicechannel=discord.utils.get(ctx.guild.voice_channels, name="Škola (Hlasová miestnosť)")
        try:
            voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
            if voice.is_connected():
                await voice.disconnect()            
            await voicechannel.connect()
        except UnboundLocalError or AttributeError:
            await voicechannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
    if datetime.today().weekday==1 or datetime.today().weekday==2 or datetime.today().weekday==3 or datetime.today().weekday==4:
        if datetime.now().hour==10:
            voicechannel=discord.utils.get(client.guilds[0].voice_channels, name="Škola (Hlasová miestnosť)")
            try:
                voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
                if voice.is_connected():
                    await voice.disconnect()            
                await voicechannel.connect()
            except UnboundLocalError or AttributeError:
                await voicechannel.connect()
            voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
            voice.play(discord.FFmpegPCMAudio("song.mp3"))
async def TestTimeOff():
    print(datetime.now().time())
    if datetime.now().hour==9:
        voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
        if voice.is_connected():
            voice.stop()
            await voice.disconnect()
    if datetime.now().hour==10:
        voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
        if voice.is_connected():
            voice.stop()
            await voice.disconnect()
    if datetime.today().weekday==1 or datetime.today().weekday==2 or datetime.today().weekday==3 or datetime.today().weekday==4:
        if datetime.now().hour==11:
            voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
            if voice.is_connected():
                voice.stop()
                await voice.disconnect()

async def ForceOn():
    voicechannel=discord.utils.get(client.guilds[0].voice_channels, name="Škola (Hlasová miestnosť)")
    try:
        voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
        if voice.is_connected():
            await voice.disconnect()            
        await voicechannel.connect()
    except UnboundLocalError or AttributeError:
        await voicechannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
async def ForceOff():
    voice = discord.utils.get(client.voice_clients, guild=client.guilds[0])
    if voice.is_connected():
        voice.stop()
        await voice.disconnect()

scheduler = AsyncIOScheduler(timezone=utc)
scheduler.add_job(TestTimeOn, 'cron', minute=50)
scheduler.add_job(TestTimeOff, 'cron', minute=0)
scheduler.start()
client.run("token")
