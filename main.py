import os
import discord
import asyncio
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


def getchannel(ctx):
    global channel
    channel = discord.utils.get(ctx.guild.channels, name="general")


def autosend(msg):
    global stopindicator
    if stopindicator == 0:
        global channel
        coro = channel.send(msg)
        future = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            future.result()
        except:
            pass


def find_source(link):
    global source
    if "spotify" in link:
        source = "spotify"
    elif "youtu.be" in link or "youtube" in link:
        source = "youtube"


def download_song(link):
    if source == "spotify":
        try:
            command = str(link)+" --path-template "+"'{title}.{ext}'"
            os.system(f"spotdl {command}")
            os.system("move *.mp3 ./umusic/")
        except Exception as e:
            print(e)
            pass
    elif source == "youtube":
        try:
            command = f"{link} --extract-audio --audio-format mp3 -o ./umusic/%(title)s.%(ext)s"
            os.system(f"yt-dlp {command}")
        except Exception as e:
            print(e)
            pass


def cleanUmusic():

    ls = os.listdir("./umusic")
    if(len(ls) != 0):
        name = ls[0]
        if(os.path.isfile("./umusic/"+name)):
            os.remove("./umusic/"+name)


@client.event
async def on_ready():
    print('Logged on as', client.user)


@client.event
async def on_member_remove(member):
    guild = client.get_guild(961654075668201502)
    channel = guild.get_channel(961654075668201505)
    await channel.send(f" {member.name} is removed from {guild.name}")


@client.event
async def on_member_join(member):
    guild = client.get_guild(961654075668201502)
    channel = guild.get_channel(961654075668201505)
    await channel.send(f" Hello {member.name}!! welcome to {guild.name}")


@client.event
async def on_message(message):
    global stopindicator
    global source
    global songQueue
    stopindicator = 1
    songQueue = []
    msg = message.content
    m = msg.lower()
    m = m.strip()
    if(message.author != client.user):
        if(m.startswith("hello") or m.startswith("hi") or m.startswith("hii")):
            hellopart = m.split(" ")[0]
            if(hellopart == "hii" or hellopart == "hello" or hellopart == "hi"):
                await message.channel.send(f"hello {message.author.mention}")
        elif(m.startswith(";")):
            if "join" in m:
                for channel in message.guild.voice_channels:
                    if(channel.members != []):
                        voiceChannel = channel
                        await message.add_reaction("👍")
                        try:
                            await voiceChannel.connect()
                            await message.channel.send("Joined to " + voiceChannel.name+" :thumbsup:")
                        except:
                            await message.channel.send("Cannot connect to this voice channel :upside_down:")
                        break
                else:
                    myEmbed = discord.Embed(
                        description="You should be connected to a the channel first", colour=discord.Color.blue())
                    myEmbed.set_author(name=str(message.author))
                    await message.channel.send(embed=myEmbed)
            elif "leave" in m:
                voice = discord.utils.get(
                    client.voice_clients, guild=message.guild)
                if voice.is_connected():
                    await voice.disconnect()
                    await message.channel.send(f"left the voice channel {voice.channel.name}")
                else:
                    myEmbed = discord.Embed(
                        description="I am not connected to a voice channel right now", colour=discord.Color.blue())
                    myEmbed.set_author(name=str(message.author))
                    await message.channel.send(embed=myEmbed)
            elif "play" in m:
                getchannel(message)
                stopindicator = 0
                msglst = msg.split(" ")
                link = msglst[1]
                link = link.strip()

                voice_client = discord.utils.get(
                    client.voice_clients, guild=message.guild)
                if voice_client.is_playing():
                    songQueue.append(link)
                else:

                    try:
                        cleanUmusic()
                        find_source(link)
                        download_song(link)
                        song_here = os.listdir("./umusic/")
                        name = song_here[0]
                        voice_client = discord.utils.get(
                            client.voice_clients, guild=message.guild)
                        voice_client.play(discord.FFmpegPCMAudio(
                            "./umusic/"+name, executable='ffmpeg'), after=lambda e: autosend(";next"))
                        myEmbed = discord.Embed(
                            description=f"NOW PLAYING... **{name}**", colour=discord.Color.blue())
                        myEmbed.set_author(name=str(message.author))

                        await message.channel.send(embed=myEmbed)
                    except Exception as e:
                        await message.channel.send("Some error occured")
                        print(e)
            elif "next" in m:
                if songQueue != []:

                    voice_client = discord.utils.get(
                        client.voice_clients, guild=message.guild)
                    link = songQueue.pop(0)
                    link = link.strip()
                    try:
                        cleanUmusic()
                        find_source(link)
                        download_song(link)
                        song_here = os.listdir("./umusic/")
                        name = song_here[0]
                        voice_client = discord.utils.get(
                            client.voice_clients, guild=message.guild)
                        voice_client.play(discord.FFmpegPCMAudio(
                            "./umusic/"+name, executable='ffmpeg'), after=lambda e: autosend(";next"))
                        myEmbed = discord.Embed(
                            description=f"NOW PLAYING... **{name}**", colour=discord.Color.blue())
                        myEmbed.set_author(name=str(message.author))

                        await message.channel.send(embed=myEmbed)
                    except Exception as e:
                        await message.channel.send("Some error occured")
                        print(e)
                else:
                    await message.channel.send("There is no song in the queue")

            elif "stop" in m:
                stopindicator = 1
                await message.channel.purge(limit=1)
                voice_client = discord.utils.get(
                    client.voice_clients, guild=message.guild)
                voice_client.stop()
    else:
        if msg == ";next" and stopindicator == 0:
            print(songQueue)
            if songQueue != []:
                print("here")
                voice_client = discord.utils.get(
                    client.voice_clients, guild=message.guild)
                link = songQueue.pop(0)
                link = link.strip()
                try:
                    cleanUmusic()
                    find_source(link)
                    download_song(link)
                    song_here = os.listdir("./umusic/")
                    name = song_here[0]
                    voice_client = discord.utils.get(
                        client.voice_clients, guild=message.guild)
                    voice_client.play(discord.FFmpegPCMAudio(
                        "./umusic/"+name, executable='ffmpeg'), after=lambda e: autosend(";next"))
                    myEmbed = discord.Embed(
                        description=f"NOW PLAYING... **{name}**", colour=discord.Color.blue())
                    myEmbed.set_author(name=str(message.author))

                    await message.channel.send(embed=myEmbed)
                except Exception as e:
                    await message.channel.send("Some error occured")
                    print(e)
            else:
                await message.channel.send("There is no song in the queue")


client.run("OTYxNjQ0MDcxMjMzOTM3NDQ4.Yk7-1Q.w3CoI1O2HXqideDys78JlNF9tBE")
