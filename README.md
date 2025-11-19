# ***Basement Dweller***
A companion Discord bot for a Discord server with an associated Minecraft server, works with Geyser

## DISCLAIMER
This is hardly a production application. I am a student so this project is primarily a tool for me to learn thus it is in constant flux and is primarily designed with my own usage in mind.

## Installation
cd into prefferred installation directory (script is designed to be run on same host as your Minecraft server)
clone the repo and cd into
create a .env file with your DISCORD_TOKEN and RCON_PASS
create and enter python virtual enviroment
pip install -r requirements.txt
run main.py

IF RERUNNNG SCRIPT AFTER INITIAL LAUNCH:
delete line 7 inside of src/userbase.py

## Usage
Before deploying absolutely remember to change permissions for /mcrun command inside your Discord server or any user will be able to run commands on your Minecraft server

If you already have an associated Minecraft server it is recommended to delete your whitelist file to avoid conflicts

Whitelisting - /linkmc yourminecraftusername
Unlinking / Removing user from whitelist - /unlinkmc

The script has a built in check for detecting if an account is a Java or Bedrock account; however, if someones Bedrock username exists also as a Java username the script will whitelist the Java user with the associated name. To combat this the bot will tell the user if a Java account or Bedrock account was added, if the wrong account is added the user can run /unlinkmc then run /linkmc again instead with the keyword "bedrock" added to explicitly state the user is a Bedrock user
Ex. /linkmc yourminecraftusername bedrock

/unlinkmc does not require any other arguments and will simply remove the users attached account from the whitelist as well as clearing their database entry for the Minecraft account

Running commands - /mcrun minecraftcommand
This command simply passes a command to the server through RCON, no "/" is needed
Ex. /mcrun kill @e

## Features
- Creates Discord user database entries for Discord username, Discord user id, Minecraft username, and Minecraft uuid / floodgateuid
- Plug and play solution for whitelisting Minecraft users through associated Discord server
