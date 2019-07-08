# GPL-3.0-or-later
# RP Crop Bot takes a text file from a user through the Application Discord and processes passes it to cropper.py for processing
#  Copyright (C) 2018 Selarics
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

import io
import math
import pathlib

# default text process
async def TextToFile(textString, charMaxCount=0, charCount=0, numPosts=0, newPostCounter=0, letter=0, post=True):
    while True:
        # make sure that the user enters the correct file name in the directory
        try:
            userFileIn = textString
            if (pathlib.Path(textString).suffix) != ".txt":
                textFromFile = io.open((str(userFileIn) + ".txt"), "r+", encoding="utf-8")
            else:
                textFromFile = io.open((str(userFileIn)), "r+", encoding="utf-8")
            break
        except FileNotFoundError:
            print("File not found error, please enter the name of the file again.")
            return False
            break

    testText = textFromFile.read()
    # open (currently default) file to write 2000 character posts
    programFileOut = io.open(("chopped_" + userFileIn), "a", encoding="utf-8")
    # init array for carachter
    arrayVar = []
    # max character split
    varSplit = 2000
    #process text into an array
    for i in testText:
        # discord counts white spaces
        charMaxCount += 1
        arrayVar.append(i)
    #set notComplete var to true for flow control -
    notComplete = True
    #while loop controls overall posting
    while(notComplete):
        #if the number of letters processed is not equal to the total number of characters, continue posting
        if( letter != charMaxCount):
            #post control
            while(post):
                #if the character count and total character count is not equal continue processing
                if ((charCount != varSplit)) and ((charCount + newPostCounter) != charMaxCount):
                    #Write each char to the write file
                    programFileOut.write((str(arrayVar[letter])))
                    #increment control counters
                    charCount += 1
                    letter+=1
                else:
                    #Enter else if 2000 characters have been processed

                    #If we are done processing characters, eneter if to finish processing
                    if (newPostCounter == charMaxCount):
                        charCount = newPostCounter
                        post = False
                        break
                    #write new post
                    programFileOut.write("\n ------------NEW POST------------ \n")
                    #continue to collect total characters processed
                    newPostCounter += charCount
                    #reset currect post character count
                    charCount = 0
        else:
            #set number of posts and set loop to complete
            numPosts = (math.ceil((len(testText) / 2000)))
            notComplete = False
    #print new line, numbers of characters and total posts - text from file to file
    print("\n")
    print("Number of characters being processed: " + str(charMaxCount))
    print("Number of posts to send entire message: " + str(numPosts))
    s = str(userFileIn)
    print("Done! File: " + s + " has been processed")

async def TextToClient(myFileOrig, mgsChan, msg2, client):
    testText = io.open(myFileOrig, "r+", encoding="utf-8").read()
    arrayVar = []
    # max character split
    varSplit = 2000
    # vars for control
    charCount = 0
    charMaxCount = 0
    numPosts = 0
    letter = 0
    postText = ""
    newPostCounter = 0
    notComplete = True
    post = True
    for i in testText:
        # discord counts white spaces
        charMaxCount += 1
        arrayVar.append(i)
    while (notComplete):
        # if the number of letters processed is not equal to the total number of characters, continue posting
        if (letter != charMaxCount):
            # post control
            while (post):
                # if the character count and total character count is not equal continue processing
                if ((charCount != varSplit)) and ((charCount + newPostCounter) != charMaxCount):
                    # Write each char to the write file
                    postText += str(arrayVar[letter])
                    # increment control counters
                    charCount += 1
                    letter += 1
                else:
                    # Enter else if 2000 characters have been processed

                    # If we are done processing charact!ers, eneter if to finish processing
                    if (newPostCounter == charMaxCount):
                        charCount = newPostCounter
                        post = False
                        # await client.send_message(mgsChan, postText)
                        break
                    # write new post
                    await client.send_message(mgsChan, postText)
                    # continue to collect total characters processed
                    newPostCounter += charCount
                    # reset currect post character count
                    charCount = 0
                    postText = ""
        else:
            # break
            notComplete = False
            await client.send_message(mgsChan, msg2)