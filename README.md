# image-to-discord-link
A simple python CLI to convert images to cdn.discordapp.com links.

![image_2022-04-17_215550113](https://user-images.githubusercontent.com/98130822/163731723-783d047c-d948-4519-baad-888562fb9020.png)

---
### Usage
#### General Syntax
`python image-to-discord-link.py <IMAGE_PATH> <LINK_PATH> <BOT_TOKEN> <SERVER_ID>`
- `IMAGE_PATH`: path to a directory containing one or more images of types: .png, .jpg, .jpeg, .gif, .gifv.
- `LINK_PATH`: path to a directory you want to store cdn.discordapp.com links in; stored in a .txt file.
- `BOT_TOKEN`: a token of a discord bot; the discord bot is used to upload images to a channel and retrieve URLs.
- `SERVER_ID`: the server ID in which the bot will create a channel to upload images and retrieve URLs.

#### Example
`python image-to-discord-link.py "I:\images\cute snakes" "D:\documents" "OTA0MDI4ODI1ODc1MjYzNDg4.YX1kdA.MZ0KKq29MTvLk3naZNS3GgRoHd4" "123456789123456789"`

---

### Installation
1. [Download the latest version of Python at python.org](https://python.org) (if you already have Python, make sure it is 3.7 or higher).
2. **When installing Python, make sure to check "Add to PATH"**.
3. Either clone this repository, or download the `image-to-discord-link.py` and `install_requirements.bat` files independently.
4. Run the `install_requirements.bat` file.
5. You are ready to use image-to-discord-link using the syntax described in the usage section!

---

### How it all works
#### Input Validation
At the start of the program, there is a check performed to check whether all user inputs follow standard discord conventions. If False is returned, a warning is displayed, and the program stops. If True is returned, the bot is ran.
```py
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
```
#### Uploading Images
After the bot is ran, the bot will create a channel named `datetime.now().strftime("%Y-%m-%d-%H-%M-%S")` (e.g. 2022-04-17-21-46-04) in the server given by SERVER_ID. If server is None, a warning is displayed, and the program stops. In this channel, the bot will upload any compatible images from the IMAGE_PATH directory to the channel.
```py
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

        print(f"Converting images to cdn.discordapp.com links...\n\n{Fore.LIGHTYELLOW_EX}")
        processes = len(images) * 3
        with alive_bar(processes) as bar:
            for image in images:
                try:
                    await channel.send(file=discord.File(image))
                except:
                    continue
                bar()  # increments progress bar value by 1
                ...
```
#### Retreiving URLs
Finally, once all compatible images have been uploaded, the bot will run through the channel's history and grab the URL of each attachment sent. It will store these URLs in a .txt file within the LINK_PATH specified. The .txt file will have the same name as the channel name the images were uploaded into.
```py
            ...
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
```
[Back To Top](#)
