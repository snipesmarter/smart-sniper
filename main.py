import argparse
import asyncio
import json
import os
import time
import urllib.request
import pwinput
import traceback
from datetime import datetime, timezone

import aiohttp
import requests
from colorama import Fore, Style, init

from msauth import PreAuthResponse, login
import scraper

if os.name == "nt":
    init(convert=True, autoreset=True)
else:
    init(convert=False, autoreset=True)

cl = False
if cl:
    os.system("cls" if os.name == "nt" else "clear")
logo = rf"""{Fore.GREEN}
  __  __ __  __  ___ _____    __  __  _ _ ___ ___ ___
/' _/|  V  |/  \| _ \_   _| /' _/|  \| | | _,\ __| _ \
`._`.| \_/ | /\ | v / | |   `._`.| | ' | | v_/ _|| v /
|___/|_| |_|_||_|_|_\ |_|   |___/|_|\__|_|_| |___|_|_\
"""
print(logo)
print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "Created by Coolkidmacho#0001" + Fore.RESET)
print(Fore.LIGHTCYAN_EX + "With the wonderful assistance of "+ Style.BRIGHT + "Kqzz#0606" + Style.NORMAL + " and " + Style.BRIGHT + "MatrixGraphicz#7585" + Fore.RESET)
print(f"{Fore.MAGENTA}Make sure to join https://discord.gg/KweaD6G97f\n")
print(
    f"{Style.BRIGHT}{Fore.YELLOW}If you want to boost or donate message Coolkidmacho#0001 on discord"
)
# print(f"{Style.DIM}This file is fully editable and changable, but all changes must be open source, changing the logo or the credits are against the request of the owner.")
end = []
orgdel = 0
global delay
delay = 0
global changeversion
changeversion = ""
global tuned_delay
tuned_delay = None
global success
success = False
reqnum = 3
global mcsauth
mcsauth = ""
global scraperset
scraperset = ""
global webhook
autoskin = True
account = []
global ms_email
ms_email = ""
global ms_pw
ms_pw = ""
global m_email
m_email = ""
global m_pw
m_pw = ""
global manual_bearer
manual_bearer = ""
global logger
logger = []

codes = {
    "mainset": [
        {
            "ms": "Microsoft",
            "m": "Mojang",
            "g": "Giftcard"
        }
    ],
    "style": [
        {
            "a": "Autosniper",
            "n": "Single Snipe",
            "s": "Show next"
        }
    ]
}

raw_account = open("account.txt", "r")
account = raw_account.readlines()
raw_account.close()

line = 0
for x in account:
    account[line] = account[line].replace("\n", "")
    account[line] = account[line].replace("Email:", "")
    account[line] = account[line].replace("Password:", "")
    account[line] = account[line].replace("Bearer:", "")
    account[line] = account[line].replace(" ", "")
    line = line + 1

ms_email = account[1]
ms_pw = account[2]
m_email = account[5]
m_pw = account[6]
manual_bearer = account[9]


def inp(text):
    print(f"{Fore.YELLOW}{text}", end="")
    ret = input("")
    return ret


def update():
    c = requests.get(
        "https://raw.githubusercontent.com/snipesmarter/smart-sniper/main/config.json"
    )
    file = open("config.json", "w")
    file.write(json.dumps(c.json(), indent=2))
    file.close()
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/snipesmarter/smart-sniper/main/skin.png",
        "skin.png",
    )


# update()


def get_config_data():
    with open("config.json") as e:
        menu = json.loads(e.read())
        # print(menu)
        global namemc
        namemc = menu["namemc"]
        global msauth
        msauth = menu["msauth"]
        global scraperset
        scraperset = menu["scraper"]
        global webhook
        webhook = menu["webhook"]
        if webhook == "":
            webhook = None
        global searches
        searches = menu["searches"]
        if scraperset == "False":
            scraperset = False
        elif scraperset == "True":
            scraperset = True




def autonamemc(email, password):
    return
    cwd = os.getcwd()
    os.chdir(f"{cwd}\\namemc")
    # os.system("python setup.py install")
    os.system(f"python start.py -u {email} -p {password}")


def changeskin(bearer):
    # print(bearer, "this")
    headers = {"Authorization": "Bearer " + bearer}
    files = {
        "variant": (None, "classic"),
        "file": ("skin.png", open("skin.png", "rb")),
    }
    response = requests.post(
        "https://api.minecraftservices.com/minecraft/profile/skins",
        headers=headers,
        files=files,
    )
    time.sleep(1)
    if response.status_code == 200 or response.status_code == 204:
        print(f"{Fore.GREEN}Successfully changed skin!")
    else:
        print(f"{Fore.RED}Failed to change skin.")


def store(droptime: int, offset: int) -> None:  # Dodgy timing script!
    print(offset, ": Delay Used")
    stamp = end[-1]
    datetime_time = datetime.fromtimestamp(droptime)
    finaldel = str(stamp - datetime_time).split(":")[2].split(".")

    print(finaldel)
    if int(finaldel[0]) != 0:
        changeversion = "inc"
        tuned_delay = delay

        print(
            f"""{Fore.LIGHTRED_EX}Cannot tune your delay, please sync your time\n
            using http://www.thinkman.com/dimension4/download.htm
            \nprogram will continue, if it fails again please restart after \n
            installing dimension4 and also set the delay to 0 for that{Fore.RESET}, also you can get this issue if you set your delay to 0"""
        )

    else:
        change = finaldel[1]
        change3 = f"{change[0]}{change[1]}{change[2]}"
        if int(change[0]) == 0:
            changeversion = "dec"
            changeint = 100 - int(f"{change[1]}{change[2]}")
            print("Change Delay:", changeint)
        else:
            changeversion = "inc"
            changeint = int(change3) - 100
            print("Change Delay:", changeint)

        if changeversion == "dec":
            tuned_delay = int(offset) - int(changeint)
        if changeversion == "inc":
            tuned_delay = int(offset) + int(changeint)
        print(
            f"{Fore.CYAN}Delay:{Fore.RESET} {offset}  {Fore.LIGHTGREEN_EX}Tuned Delay:{Fore.RESET}  {tuned_delay}"
        )


def custom(email, password, token, name):
    if success == True:
        try:
            if webhook != None:
                snipedtime = datetime.now(timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%S.%f%Z"
                )

                webhookjson = {
                    "content": "",
                    "embeds": [
                        {
                            "title": f"You sniped {name}",
                            "description": f"Congratulations on your new snipe!\nYou sniped {name.upper()}! \nYou sniped {name} at exactly {snipedtime}",
                            "color": 5814783,
                            "footer": {"text": "Sniper Made by Coolkidmacho#0001"},
                        }
                    ],
                    "username": "Smart Sniper",
                    "avatar_url": "https://cdn.discordapp.com/icons/840342619329658921/a_d3e87d7774f9c82b684c3a667e9cf23e.webp?size=128",
                }
                requests.post(webhook, json=webhookjson)
        except:
            print(f"{Fore.RED}Failed to send webhook!")
        try:
            changeskin(token)
        except:
            print(f"{Fore.RED}Failed to send change skin!")
        print(
            "{Fore.GREEN}Congrats!\n{Fore.LIGHTGREEN_EX}You successfully sniped {Fore.GREEN}{name}{Fore.LIGHTGREEN_EX} at {Fore.GREEN}{snipedtime}{Fore.LIGHTGREEN_EX}!"
        )
        if namemc == "True":
            autonamemc(email, password)
        exit()

threeapi = None
starapi = None
ccapi = None


async def check_connections():
    global scraperset
    print()
    print(f"\r{Fore.YELLOW}Testing connections: [________] 0%", end="\r")

    try:  # Internet
        requests.get("https://google.com", timeout=5)
        print(f"\r{Fore.YELLOW}Testing connections: [██______] 25%", end="\r")
    except:
        print(f"\r{Fore.RED}Testing connections: [________] 0% ")
        print()
        print(f"{Fore.RED}Make sure your computer is connected to the internet!")
        exit()
    try: # 3C API
        global threeapi
        threeapi = False
        req = requests.get("http://minecraftservicess.com/", headers = {"Content-type": "application/json", "User-Agent": "Sniper"}, timeout=5)
        if req.status_code == 404:
            raise Exception
        threeapi = True
    except:
        pass
    finally:
        print(f"\r{Fore.YELLOW}Testing connections: [████____] 50%", end="\r")
    try:  # Star.shopping API
        global starapi
        starapi = False
        req = requests.get("http://api.star.shopping/droptime/abc", headers = {"Content-type": "application/json", "User-Agent": "Sniper"}, timeout=5)
        if req.status_code == 503:
            raise Exception
        starapi = True
    except:
        pass
    finally:
        print(f"\r{Fore.YELLOW}Testing connections: [██████__] 75%", end="\r")
    try:  # Droptime.cc API
        global ccapi
        ccapi = False
        req = requests.get("http://api.droptime.cc/droptime/abc", timeout=5)
        if req.status_code != 200:
            raise Exception
        ccapi = True
    except:
        pass
    finally:
        print(f"\r{Fore.YELLOW}Testing connections: [████████] 100%")
        print()
        print(f"{Fore.YELLOW}3Char API: {threeapi} | Star API: {starapi} | CC API: {ccapi}")
        print()
        if threeapi == False and starapi == False and ccapi == False and scraperset == False:
            print(f"{Fore.LIGHTRED_EX}Can't reach any droptime API!")
            if scraper.check_scraper() == True:
                scraperset = True
                print(f"{Fore.LIGHTYELLOW_EX}Forcing scraper...")
            else:
                print(f"{Fore.RED}Can't use scraper in your country!")
                print(f"{Fore.RED}Quitting...")
                exit()
        elif threeapi == False and scraperset == False:
            if scraper.check_scraper() == True:
                scraperset = True
            else:
                print(f"{Fore.LIGHTRED_EX}Autosniping and searchbased sniping are currently unavailable!")
            
            print()
        if scraperset == True:
            if scraper.check_scraper() == True:
                print(f"{Fore.GREEN}Successfully activated scraper")
            else:
                scraperset = False
                print(f"{Fore.RED}Warning! It seems that the scraper doesn't work in your region!")
                print(f"{Fore.RED}Deactivating scraper...")
                if threeapi == False and starapi == False and ccapi == False:
                    print(f"{Fore.RED}The sniper has no way to get the droptime!")
                    print(f"{Fore.YELLOW}If you know a public API that gets the droptime of names\nyou can report this to a support channel:\nhttps://discord.gg/KweaD6G97f")
                    print(f"{Fore.RED}Shutting down sniper")
                    exit()
        print()
        


async def send_request(s: aiohttp.ClientSession, bearer: str, name: str) -> None:
    headers = {"Content-type": "application/json", "Authorization": "Bearer " + bearer}

    json = {"profileName": name}

    async with s.post(
        "https://api.minecraftservices.com/minecraft/profile",
        json=json,
        headers=headers,
    ) as r:
        print(
            f"{Fore.LIGHTRED_EX if r.status != 200 else Fore.LIGHTGREEN_EX}Response received @ {datetime.now()}{Fore.RESET} {Fore.LIGHTRED_EX if r.status != 200 else Fore.LIGHTGREEN_EX} with the status {r.status}{Fore.RESET}"
        )
        end.append(datetime.now())
        if r.status == 200:
            print(f"{Fore.GREEN}C")
            global success
            success = True


async def get_droptime(username: str, session: aiohttp.ClientSession) -> int:
    try:
        r = requests.get(f"https://api.star.shopping/droptime/{username}", headers = {"Content-type": "application/json", "User-Agent": "Sniper"})
        r_json = r.json()
        droptime = int(float(r_json["unix"]))
        return droptime
    except:
        try:
            r2 = requests.get(f"https://buxflip.com/data/droptime/{username}", headers = {"Content-type": "application/json", "User-Agent": "Sniper"})
            r_json = r2.json()["data"]
            droptime = int(float(r_json["droptime"]))
            return droptime
        except:
            try:
                r3 = requests.get(f"http://api.droptime.cc/droptime/{username}")
                r_json = r3.json()
                droptime = int(float(r_json["unix"]))
                return droptime
            except:
                try:
                    if scraperset == False:
                        raise Exception
                    res = scraper.getNameInfo(username)
                    return res["droptime"]
                except:
                    prevOwner = inp(
                        f"What is the current username of the account that owned {username} before this?:   "
                    )
                    try:
                        droptime = scraper.prevOwnerDroptime(prevOwner)
                    except:
                        droptime = None
                    if droptime != None:
                        return droptime
                    else:
                        print(f"{Fore.LIGHTRED_EX}Droptime for name not found, make sure you entered the details into the field correctly!{Fore.RESET}")
                        exit()


async def get_scaper_drop(username: str) -> int:
    nameinfo = scraper.getNameInfo(username)
    drop = nameinfo["droptime"]
    return drop


async def get_profile_information(bearer: str, attr: str) -> str:
    async with aiohttp.ClientSession() as s:
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + bearer,
        }
        async with s.get(
            f"https://api.minecraftservices.com/minecraft/profile",
            headers=headers,
        ) as r:
            try:
                p_infos = await r.json()
                return p_infos[attr]
            except:
                print(f"{Fore.RED}Failed to login!")


def get_next_names(amount: int) -> None:
    search = 0
    char = 0
    sel = inp(
        f"{Fore.YELLOW}For search based sniping select {Fore.GREEN}s{Fore.RESET}\n{Fore.YELLOW}For Auto 3char Enter {Fore.GREEN}3{Fore.RESET}: "
    )
    if sel == "s":
        search = inp("How many searches do you want?: ")
        search = int(search)
    elif sel == "3":
        char = 3
    else:
        print(f"{Fore.RED}Wrong input, skipping")
        return
    if scraperset:
        try:
            names = scraper.getNameDrops(search, char)
        except Exception as e:
            print(e)
            print(f"{Fore.RED}Failed to use scraper! Report this to a support channel!")
            return
    else:
        if char == 3:
            try:
                raw = requests.get("http://minecraftservicess.com/", headers = {"Content-type": "application/json", "User-Agent": "Sniper"}).json()["data"]
                halfdrops = sorted(raw.items(), key=lambda x:x[1])
                drops = dict([(k,v) for k,v in halfdrops])
                dl = list(drops)
                rn = [[0 for x in range(2)] for y in dl]
                count = 0
                for x in dl:
                    rn[count][0] = x
                    rn[count][1] = drops[x]/1000
                    count+=1
                names = scraper.jsonBuilder(rn)
            except:
                print(f"{Fore.LIGHTRED_EX}API is down...")
                return
        else:
            try:
                names = requests.get(f"http://api.coolkidmacho.com/up/{search}").json()
            except:
                print(f"{Fore.LIGHTRED_EX}API is down...")
                return
    namecount = 0
    for nameseg in names:
        if namecount <= amount:
            name = nameseg["name"]
            droptime = int(float(nameseg["droptime"]))
            droptime = datetime.fromtimestamp(droptime)
            print(f"{Fore.LIGHTGREEN_EX}{name}{Fore.LIGHTCYAN_EX} at {droptime}")
            namecount = namecount + 1
        else:
            return


#   Mojang setup and snipe


async def send_mojang_request(
    s: aiohttp.ClientSession, bearer: str, name: str, num: int
) -> None:
    headers = {"Content-type": "application/json", "Authorization": "Bearer " + bearer}
    starttime = time.time()
    async with s.put(
        f"https://api.minecraftservices.com/minecraft/profile/name/{name}",
        headers=headers,
    ) as r:
        global success
        success = False
        endtime = time.time()
        difftime = float(endtime) - float(starttime)
        if r.status == 200:
            print(
                f"{Fore.LIGHTCYAN_EX}Response {num} received @ {datetime.now()} with the status {Fore.GREEN}{r.status}"
            )
            success = True
        else:
            print(
                f"{Fore.LIGHTCYAN_EX}Response {num} received @ {datetime.now()} with the status {Fore.RED}{r.status}"
            )
        print(
            f"{num} sent: {datetime.fromtimestamp(starttime)} recieved: {datetime.fromtimestamp(endtime)} difference: {difftime}s"
        )
        end.append(datetime.now())


async def get_mojang_token(email: str, password: str) -> str:
    # Login code is partially from mcsniperpy thx!
    questions = []

    async with aiohttp.ClientSession() as session:
        authenticate_json = {"username": email, "password": password}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
            "Content-Type": "application/json",
        }
        async with session.post(
            "https://authserver.mojang.com/authenticate",
            json=authenticate_json,
            headers=headers,
        ) as r:
            # print(r.status)
            if r.status == 200:
                resp_json = await r.json()
                # print(resp_json)
                auth = {"Authorization": "Bearer: " + resp_json["accessToken"]}
                access_token = resp_json["accessToken"]
                # print(f"{Fore.LIGHTGREEN_EX}Auth: {auth}\n\nAccess Token: {access_token}")
            else:
                print(f"{Fore.LIGHTRED_EX}INVALID CREDENTIALS{Fore.RESET}")

        async with session.get(
            "https://api.mojang.com/user/security/challenges", headers=auth
        ) as r:
            answers = []
            if r.status < 300:
                resp_json = await r.json()
                if resp_json == []:
                    async with session.get(
                        "https://api.minecraftservices.com/minecraft/profile/namechange",
                        headers={"Authorization": "Bearer " + access_token},
                    ) as nameChangeResponse:
                        ncjson = await nameChangeResponse.json()
                        print(ncjson)
                        try:
                            if ncjson["nameChangeAllowed"] is False:
                                print(
                                    "Your Account is not" " eligible for a name change!"
                                )
                                exit()
                            else:
                                print(
                                    f"{Fore.LIGHTGREEN_EX}Logged into your account successfully!{Fore.RESET}"
                                )
                        except Exception:
                            print("logged in correctly")
                else:
                    try:
                        for x in range(3):
                            ans = inp({resp_json[x]["question"]["question"]})
                            answers.append(
                                {"id": resp_json[x]["answer"]["id"], "answer": ans}
                            )
                    except IndexError:
                        print(
                            f"{Fore.LIGHTRED_EX}Please provide answers to the security questions{Fore.RESET}"
                        )
                        return
                    async with session.post(
                        "https://api.mojang.com/user/security/location",
                        json=answers,
                        headers=auth,
                    ) as r:
                        if r.status < 300:
                            print(f"{Fore.LIGHTGREEN_EX}Logged in{Fore.RESET}")
                        else:
                            print(
                                f"{Fore.LIGHTRED_EX}Security Questions answers were incorrect, restart the program!{Fore.RESET}"
                            )
    return access_token


async def mojang_snipe(target: str, offset: int, bearer_token: str, drop: int) -> None:
    async with aiohttp.ClientSession() as session:
        if scraperset:
            if drop == None:
                droptime = await get_scaper_drop(target)
                if droptime == None:
                    droptime = await get_droptime(target, session)
                    if droptime == None:
                        print(f"{Fore.RED}This name isn't dropping!")
                        return
            else:
                droptime = drop
        else:
            if drop == None:
                droptime = await get_droptime(target, session)
            else:
                droptime = drop
        offset = int(offset)
        snipe_time = droptime - (offset / 1000)
        conv_droptime = datetime.fromtimestamp(droptime).strftime(
            "%H:%M:%S on %Y-%m-%d"
        )
        print(f"{Fore.MAGENTA}sniping {target} at {conv_droptime}")
        while time.time() < snipe_time - 10:
            await asyncio.sleep(0.001)
        if (
            requests.get(
                "https://api.mojang.com/users/profiles/minecraft/" + target
            ).status_code
            == 204
        ):
            while time.time() < snipe_time - 0.001:
                await asyncio.sleep(0.001)
            coroutines = [
                send_mojang_request(session, bearer_token, target, x) for x in range(2)
            ]
            await asyncio.gather(*coroutines)
            store(droptime, offset)
        else:
            print(f"{Fore.RED}{target} is no longer dropping. Skipping...")
        if success == True:
            custom(email, password, token, name)


async def autosniper(token: str) -> None:
    print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
    searches = 0
    chars = 0
    sel = inp(
        f"{Fore.YELLOW}For search based sniping select {Fore.GREEN}s{Fore.RESET}\n{Fore.YELLOW}For Auto 3char Enter {Fore.GREEN}3{Fore.RESET}: "
    )
    logger.append(sel)
    if sel == "s":
        searches = inp("How many searches do you want?: ")
        searches = int(searches)
        logger.append(searches)
    elif sel == "3":
        chars = 3
    while True:
        if scraperset:
            names = scraper.getNameDrops(searches, chars)
        else:
            if chars == 0:
                print(f"{Fore.RED}No search based API available")
                ask = inp("Do you want to autosnipe 3chars? Y/N: ")
                if ask.lower() == "y":
                    chars = 3
                else:
                    print(f"{Fore.RED}Quitting")
                    exit()
            if chars == 0:
                try:
                    names = requests.get(f"https://api.coolkidmacho.com/up/{searches}").json()
                except:
                    print(f"{Fore.LIGHTRED_EX}API is down, can't use this feature...")
                    print(
                        f"{Fore.LIGHTRED_EX}You can activate it in config.json by setting\n"
                        f'{Fore.LIGHTRED_EX}"scraper": "True"'
                        )
                    exit()
            else:
                try:
                    raw = requests.get("http://minecraftservicess.com/", headers = {"Content-type": "application/json", "User-Agent": "Sniper"}).json()["data"]
                    halfdrops = sorted(raw.items(), key=lambda x:x[1])
                    drops = dict([(k,v) for k,v in halfdrops])
                    dl = list(drops)
                    rn = [[0 for x in range(2)] for y in dl]
                    count = 0
                    for x in dl:
                        rn[count][0] = x
                        rn[count][1] = drops[x]/1000
                        count+=1
                    names = scraper.jsonBuilder(rn)
                except:
                    print(f"{Fore.LIGHTRED_EX}API is down, can't use this feature...")
                    print(
                        f"{Fore.LIGHTRED_EX}You can activate it in config.json by setting\n"
                        f'{Fore.LIGHTRED_EX}"scraper": "True"'
                        )
                    exit()
        #print(names)
        delay = inp(f"Delay for snipe:  ")
        print(tuned_delay, "tuned delay value")
        logger.append(None)
        logger.append(delay)
        for nameseg in names:
            name = nameseg["name"]
            logger[-2] = name
            if scraperset:
                droptime = nameseg["droptime"]
                namecheck = requests.get(f"https://api.ashcon.app/mojang/v2/user/{name}")
                if namecheck.status_code == 404:
                    if tuned_delay is None:
                        print(f"{Fore.CYAN}Defaulting...{Fore.RESET}")
                        pass
                    else:
                        delay = tuned_delay
                        print(f"{Fore.CYAN}Delay Tuned{Fore.RESET}")
                    print("delay is now ", delay)
                    logger[-1] = delay
                    await mojang_snipe(name, delay, token, droptime)
            else:
                try:
                    droptime = nameseg["droptime"]
                except:
                    droptime = None
                namecheck = requests.get(f"https://api.ashcon.app/mojang/v2/user/{name}")
                if namecheck.status_code == 404:
                    if tuned_delay is None:
                        print(f"{Fore.CYAN}Defaulting...{Fore.RESET}")
                        pass
                    else:
                        delay = tuned_delay
                        print(f"{Fore.CYAN}Delay Tuned{Fore.RESET}")
                    print("delay is now ", delay)
                    logger[-1] = delay
                    await mojang_snipe(name, delay, token, droptime)
    


async def gather_mojang_info() -> None:
    email = inp(f"Account Email:  ")
    password = pwinput.pwinput(prompt=f"{Fore.YELLOW}Password: ", mask="")
    token = await get_mojang_token(email, password)
    style = inp(
            f"{Fore.YELLOW}What sniper mode?\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}a{Fore.YELLOW} for autosniper{Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}n{Fore.YELLOW} for single name sniping {Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}s{Fore.YELLOW} to show next 3chars: {Fore.RESET}"
        )
    logger.append(style)
    if style == "a":
        await autosniper(token)
    elif style == "n" or "s":
        if style == "s":
            get_next_names(10)
        name = inp(f"Name to snipe:  ")
        delay = inp(f"Delay for snipe:  ")
        logger.append(name)
        logger.append(delay)
        tuned_delay = delay
        await mojang_snipe(name, delay, token, None)

async def iterate_through_names(session: aiohttp.ClientSession) -> None:
    while True:
        async with session.get("https://api.3user.xyz/list") as r:
            r_json = await r.json()
            if r.status < 300:
                for name in r_json:
                    yield name["name"]
                await asyncio.sleep(1)
            else:
                print(f"Failed to get names, retrying... | {r.status}")
                await asyncio.sleep(10)

def namechange_eligibility(token):
    headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + token,
        }
    resp = requests.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers=headers)
    if resp.status_code == 200:
        resp = resp.json()
        if resp["nameChangeAllowed"] == False:
            print(f"{Fore.RED}You cant change your name yet!")
            print(f"{Fore.RED}Choose another account to snipe!")
            exit()
    else:
        print(f"{Fore.RED}Cannot auth you account!")
        exit()
    


async def start() -> None:
    global scraperset
    get_config_data()
    await check_connections()
    mainset = inp(
        f"\n{Fore.LIGHTBLUE_EX}What account type? \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}g{Fore.RESET}{Fore.LIGHTBLUE_EX} for giftcard snipes \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}m{Fore.RESET} {Fore.LIGHTBLUE_EX}for mojang snipes \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}ms{Fore.RESET} {Fore.LIGHTBLUE_EX}for microsoft snipes: "
    )
    logger.append(mainset)
    if mainset == "m":

        reqnum = 3
        print(
            f"{Fore.LIGHTGREEN_EX}Mojang Account Selected, using Mojang Sniper{Fore.RESET}"
        )
        await gather_mojang_info()
        return
    elif mainset == "ms" or mainset == "g":
        if mainset == "ms":
            print(f"{Fore.LIGHTGREEN_EX}Microsoft Account Selected, using Microsoft Sniper{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTGREEN_EX}Giftcard Selected, using Microsoft Sniper{Fore.RESET}")
            
        autype = inp(
            f"To use microsoft email and password auth enter {Fore.GREEN}e{Fore.RESET}\n{Fore.YELLOW}To use Token enter {Fore.GREEN}t{Fore.RESET}:  "
        )
        if autype.lower() == "e":
            try:
                if ms_email == "" or ms_pw == "":
                    email = inp(f"Microsoft email: ")
                    password = pwinput.pwinput(prompt=f"{Fore.YELLOW}Password: ", mask="")
                else:
                    email = ms_email
                    password = ms_pw
                resp = login(email, password)
                
                token = resp["access_token"]
                try:
                    login_name = await get_profile_information(token, "name")
                    print(
                        f"{Fore.GREEN}Logged into {Fore.LIGHTCYAN_EX}{Style.BRIGHT}{login_name}"
                    )
                except:
                    print(f"{Fore.GREEN}No previous name")
            except:
                print(f"{Fore.RED}Failed MsAuth for you, use token.")
                if manual_bearer == "":
                    token = inp(f"What is your bearer token:  ")
                else:
                    token = manual_bearer
                try:
                    login_name = await get_profile_information(token, "name")
                    print(
                        f"{Fore.GREEN}Logged into {Fore.LIGHTCYAN_EX}{Style.BRIGHT}{login_name}"
                    )
                except:
                    print(f"{Fore.GREEN}No previous name")
        elif autype.lower() == "t":
            if manual_bearer == "":
                token = inp(f"What is your bearer token:  ")
            else:
                token = manual_bearer
            try:
                login_name = await get_profile_information(token, "name")
                print(
                    f"{Fore.GREEN}Logged into {Fore.LIGHTCYAN_EX}{Style.BRIGHT}{login_name}"
                )
            except:
                print(f"{Fore.GREEN}No previous name")
        else:
            print(f"{Fore.RED}You did not select a valid option.")
            exit()
        namechange_eligibility(token)
        style = inp(
            f"{Fore.YELLOW}What sniper mode?\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}a{Fore.YELLOW} for autosniper{Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}n{Fore.YELLOW} for single name sniping {Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}s{Fore.YELLOW} to show next 3chars: {Fore.RESET}"
        )
        logger.append(style)
        if style == "a":
            await autosniper(token)
            return
        elif style == "n" or style == "s":
            if style == "s":
                get_next_names(10)
            name = inp(f"Name to snipe:  ")
            global delay
            delay = inp(f"Delay for snipe:  ")
            global tuned_delay
            tuned_delay = delay
            logger.append(None)
            logger.append(name)
            logger.append(delay)
            await (mojang_snipe(name, delay, token, None))
        else:
            print(f"{Fore.RED}Please select a valid option")
            inp(f"Press enter to exit")
            exit()
    else:
        print(f"{Fore.RED}You did not enter a proper value. Ending.")
        exit()


parser = argparse.ArgumentParser()

parser.add_argument("-t", "--Type", help="Name")
parser.add_argument("-n", "--Name", help="Name")
parser.add_argument("-d", "--Delay", help="Delay")
parser.add_argument("-e", "--Email", help="Email")
parser.add_argument("-p", "--Password", help="Password")

args = parser.parse_args()
# print(vars(args))
boot = vars(args)
if boot["Type"] != None:
    mainset = boot["Type"].replace(" ", "")
    email = boot["Email"].replace(" ", "")
    password = boot["Password"].replace(" ", "")
    delay = boot["Delay"].replace(" ", "")
    name = boot["Name"].replace(" ", "")
    if mainset == "m":
        loop = asyncio.get_event_loop()
        token = loop.run_until_complete(get_mojang_token(email, password))
    elif mainset == "ms" or mainset == "g":
        resp = login(email, password)
        token = resp["access_token"]
    asyncio.run(mojang_snipe(name, delay, token, None))
    
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
except Exception as exc:
    logs = []
    logs.append(f"Account: {codes['mainset'][0][logger[0]]}")
    logs.append(f"Type: {codes['style'][0][logger[1]]}")
    logs.append(f"Style: {logger[2]}")
    logs.append(f"Name: {logger[3]}")
    logs.append(f"Delay: {logger[4]}")
    logs.append(f"Scraper: {str(scraperset)}")
    logs.append(f"Check: {str(scraper.check_scraper())}")
    print(f"\n\n\n{Fore.RED}Error! Report a screenshot of the following section in a support channel on Discord!\n")
    print(f"{Fore.RED}{logs}\n")
    print(f"{Fore.RED}{traceback.format_exc()}")
    print()
    exit()
    