# GPL-3.0-or-later
# RP Crop Bot takes a text file from a user through the Application Discord and processes passes it to cropper.py for processing
# Copyright (C) 2019 Selarics
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import aiohttp, secrets, random, time, os, discord, asyncio
from cropper import *
from logger import *


# init our client
client = discord.Client()
filenamelist = []
global cleanned
cleanned = True

# @client.event
# async def on_join(guild):
#     return # unused ATM - TODO: add join message

@client.event
# the main event
async def on_message(message):

    # don't talk to ourselves
    if message.author == client.user:
        return

    # information about the bot
    if message.content.startswith("!crop info"):
        async with message.channel.typing():
            await message.channel.send(str(message.author.mention))

            await message.channel.send("""This bot takes a Text(.txt) file and processes it into 2000 character chunks to post to discord. If the file is larger than 5kb, than you must manually post the text from the chopped text file to the channel.
            """)

            await message.channel.send("""IMPORTANT: The program will not accept anything other than a utf-8 encoded text file. To ensure that your file has the correct encoding, please open it in a text editor(notepad on windows PCs) and go to the file menu. Click 'save as' and select the propper encoding type.
            """)

            await message.channel.send("Current commands: !chop, !crop info, !crop legal")

    if message.content.startswith("!crop legal"):
        async with message.channel.typing():
            await legallog(message)
            await message.channel.send(str(message.author.mention))
            await message.channel.send(
        """RP Crop Bot Copyright (C) 2019 Selarcis
    
        This program comes with ABSOLUTELY NO WARRANTY;'.
        This is free software, and you are welcome to redistribute it
        under certain conditions; <http://www.gnu.org/licenses/gpl-3.0-standalone.html>""")

    # admin remote stop - super secret
    if message.content.startswith(str(stopToken)):
        async with message.channel.typing():
            await adminlog(message)
            await message.delete()
            await message.channel.send("Goodbye! - shutdown by admin in 3..2..1")
            time.sleep(3)
            cleanup().close()
            await client.logout()

    #so now we get to the good stuff
    if message.content.startswith('!chop'):
        global cleanned
        async with message.channel.typing():
            # here we take down some things: message author, message id, message url,
            # message size in bytes, message proxy url, and the file name
            await croplog(message)

            # assign reused calls for my own sanity
            try:
                mgsChan = message.channel
                mgsAttch = message.attachments[0].filename
                url = str(message.attachments[0].url)
                msg = 'Begin post for {0.author.mention}'.format(message)
                msg2 = 'End post for {0.author.mention}'.format(message)
                global myFileChopped
                global myFileOrig
            except IndexError:
                await message.channel.send("No file was attached to the message, please submit a text file and try again")
                return False
            except:
                return False

            # print message that we are starting a chop for a user
            print("Begin chop for " + str(message.author) + " file; " + str(mgsAttch))

            # send acknowledgment to user on Discord
            await message.channel.send(msg)

            # now we get the file from discord - how does this work? It works.
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    with open(str(mgsAttch), 'wb') as fn:
                        while True:
                            chunk = await resp.content.read()
                            if not chunk:
                                break
                            fn.write(chunk)

            # pass the file name to a new variable
            myFileOrig = str(mgsAttch)
            filenamelist.append(str(myFileOrig))

            # check if the file size is rather big
            # if not, send the text to the channel
            if message.attachments[0].size <= 5000:
                await TextToClient(message, myFileOrig, message.channel, msg2, discord.client)
                await message.delete()
            else:
                # process the text file into chunks
                # rename the file with the prefix chopped_
                myFileChopped = str("chopped_" + mgsAttch)
                print(myFileOrig, myFileChopped)
                filenamelist.append(str(myFileChopped))

                if(mgsAttch):
                    await TextToFile(str(mgsAttch), message)
                    try:
                        await message.channel.send(
                            content="File to big, please manually send the posts from the chopped file.",
                            file=discord.File(str(myFileChopped))
                        )
                    except:
                        await errorLog(message)
                        cleanned = False
                        return False
                    await message.channel.send(msg2)
                else:
                    await message.channel.send(msg2)
                    return

            # Done, time to let the user know
            print("End chop for " + str(message.author) + " file; " + str(mgsAttch) + "\n")
            cleanned = False


async def cleanup():
    print("Cleaning...")
    # the file was processed locally, time to clean it up
    for name in filenamelist:
        if os.path.isfile(str(name)):
            os.remove(str(name))
        else:
            print("No file named: " + name)
    filenamelist.clear()

# super secret
tokenGet = io.open("token", "r", encoding="utf-8")
token = tokenGet.readline()
tokenGet.close()
lowr = random.randint(32,64)
upr = random.randint(107, 255)
tokSiz = random.randint(lowr,upr)
stopToken = secrets.token_hex(tokSiz)
print(stopToken)
rand = random.randint(1,10)
rand = (rand/1000)


@client.event
# client is ready
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!crop info"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # check if we need to clean every 30 seconds
    while True:
        await asyncio.sleep(30)
        global cleanned
        if cleanned != True:
            print(filenamelist)
            await cleanup()
            cleanned = True
    # await on_join(discord._from_data['id'])-- for the future

# fire us off
client.run(token)