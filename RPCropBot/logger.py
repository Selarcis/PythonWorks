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
import io, time

# admin command logging
async def adminlog(message):
    logFile = io.open("localLog.txt", "a", encoding="utf-8")
    logFile.write(str(time.strftime("%X %x")) + "\n")
    logFile.write(str(message.author) + "\n")
    logFile.write("content: " + str(message.content) + "\n")
    logFile.write("message id: " + str(message.id) + "\n")
    logFile.write("_________LOGGEDOUT_BY_TOKEN____________\n")
    logFile.close()

# general logging
global filesDone
filesDone = 0
async def croplog(message):
    global filesDone
    filesDone += 1
    logFile = io.open("localLog.txt", "a", encoding="utf-8")
    logFile.write(str(time.strftime("%X %x")) + "\n")
    # all the info in an attachment
    # if log has no content, user didn't upload a file
    attachList = ['url', 'size', 'proxy_url', 'id', 'filename']
    logFile.write(str(message.author) + "\n")
    logFile.write("message id: " + str(message.id) + "\n")
    for i in attachList:
        if i == 'size':
            logFile.write(i + ": " + str() + " bytes \n")
        else:
            logFile.write(i + ": " + str(message.attachments) + "\n")
    logFile.write("____________FILE_%i__________\n" % filesDone)

async def legallog(message):
    logFile = io.open("localLog.txt", "a", encoding="utf-8")
    logFile.write(str(time.strftime("%X %x")) + "\n")
    logFile.write(str(message.author) + "\n")
    logFile.write("content: " + str(message.content) + "\n")
    logFile.write("message id: " + str(message.id) + "\n")
    logFile.write("_________LEGAL_REQUEST____________\n")
    logFile.close()

async def errorLog(message):
    logFile = io.open("localLog.txt", "a", encoding="utf-8")
    logFile.write(str(time.strftime("%X %x")) + "\n")
    logFile.write(str(message.author) + "\n")
    logFile.write("content: " + str(message.content) + "\n")
    logFile.write("message id: " + str(message.id) + "\n")
    logFile.write("message id: " + str(message.attachments) + "\n")
    logFile.write("_________ERROR_REQUEST____________\n")
    logFile.close()
