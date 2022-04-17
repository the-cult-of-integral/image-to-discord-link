# Created by "The Cult of Integral" @ https://github.com/the-cult-of-integral/image-to-discord-link/
# License: MIT

import asyncio
import discord
import os
import re 
import sys
import platform
from alive_progress import alive_bar
from colorama import Fore, init
from discord.ext import commands
from datetime import datetime
init()  # Initalise Colorama


def clear() -> None:
    """Clears the screen for the three major platforms: Windows, Mac, and Linux.
    """
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Darwin" or platform.system() == "Linux":
        os.system("clear")
    else:
        pass


try:
    IMG_PATH = os.path.normpath(sys.argv[1])
    LINK_PATH = os.path.normpath(sys.argv[2])
    TOKEN = sys.argv[3]
    SERVER_ID = sys.argv[4]
except:
    clear()
    print(f"""{Fore.LIGHTRED_EX}Improper arguments passed. 
{Fore.RESET}See https://github.com/the-cult-of-integral/image-to-discord-link/ for help.

{Fore.LIGHTBLUE_EX}Enter anything to exit.
>>> {Fore.RESET}""", end="")
    input()
    os._exit(1)

if platform.system() == "Windows":
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())


@bot.event
async def on_ready() -> None:
    """Creates a channel and uploads pictures from IMG_PATH into it.
    Then, runs through that channel's message history and gets all of
    the URLs of the images posted; stores the URLs in LINK_PATH.
    """
    clear()
    server = bot.get_guild(int(SERVER_ID))
    if not server:
        print(f"{Fore.LIGHTRED_EX}Invalid Server ID{Fore.RESET}")
        await bot.close()
    else:
        channel_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        channel = await server.create_text_channel(name=channel_name)
        
        # Get compatible images in IMG_PATH

        with os.scandir(IMG_PATH) as files:
            images = []
            for f in list(files):
                if temp := re.search(
                    r".+\.(jpg|jpeg|png|gif|gifv)$", f.name.lower()):
                    images.append(f)
            if not images:
                print(f"{Fore.LIGHTRED_EX}No Compatible Images In Image Path\
{Fore.RESET}")
                await bot.close()
        
        # Send images to channel and retrieve their URLs
        # alive_bar(processes) is the progress bar

        print(f"""{Fore.LIGHTGREEN_EX}Converting images to \
cdn.discordapp.com links...

{Fore.LIGHTBLUE_EX}Total Processes: {len(images) * 3}
{Fore.LIGHTWHITE_EX}{len(images)} images to upload.
{len(images)} URLs to retrieve.
{len(images)} URLs to save.\n\n

{Fore.LIGHTYELLOW_EX}""")
        processes = len(images) * 3
        with alive_bar(processes) as bar:
            for image in images:
                try:
                    await channel.send(file=discord.File(image))
                except:
                    continue
                bar()  # increments progress bar value by 1
            
            urls = []
            async for message in channel.history():
                for attachment in message.attachments:
                    urls.append(attachment.url)
                    bar()
        
            save_path = os.path.normpath(f"{LINK_PATH}\\{channel_name}.txt")
            with open(save_path, "w") as f:
                for url in urls:
                    f.writelines(f"{url}\n")
                    bar()
        
        clear()
        await bot.close()


def check_inputs() -> bool:
    """Checks if user inputs follow the standard discord conventions
    before attempting to run the bot and start converting images.

    Returns:
        bool: true if all checks have passed, false otherwise.
    """
    succeed = True
    if not os.path.isdir(IMG_PATH):
        print(f"{Fore.LIGHTRED_EX}Invalid Image Path: {Fore.RESET}{IMG_PATH}")
        succeed = False
    if not os.path.isdir(LINK_PATH):
        print(f"{Fore.LIGHTRED_EX}Invalid Link Path: {Fore.RESET}{LINK_PATH}")
        succeed = False
    if len(TOKEN) != 59:
        print(f"{Fore.LIGHTRED_EX}Invalid Token: {Fore.RESET}{TOKEN}")
        succeed = False
    if len(SERVER_ID) != 18:
        print(f"{Fore.LIGHTRED_EX}Invalid Server ID: {Fore.RESET}{SERVER_ID}")
        succeed = False
    return succeed


def main() -> None:
    clear()
    if check_inputs():
        print(f"{Fore.LIGHTBLUE_EX}Running Bot. . .{Fore.RESET}")
        try:
            bot.run(TOKEN)
            print(f"""{Fore.LIGHTGREEN_EX}Task Completed!

{Fore.LIGHTBLUE_EX}You can find the links in this directory: 
{Fore.LIGHTYELLOW_EX}{LINK_PATH}{Fore.RESET}

{Fore.LIGHTGREEN_EX}Created by "The Cult of Integral": https://github.com/the-cult-of-integral/
{Fore.LIGHTBLUE_EX}Enter anything to exit.
>>> {Fore.RESET}""", end="")
            input()
            clear()
            return
        except discord.LoginFailure:
            print(f"{Fore.LIGHTRED_EX}Invalid Token{Fore.RESET}")
            return
    else:
        print(f"""
{Fore.LIGHTBLUE_EX}Enter anything to exit.
>>> {Fore.RESET}""", end="")
        input()
        clear()
        return


if __name__ == "__main__":
    main()
