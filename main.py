import argparse
import asyncio
import json
import os
import time
import urllib.request
import pwinput
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
print(Fore.LIGHTCYAN_EX + "With the wonderful assistance of Kqzz#0001" + Fore.RESET)
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


raw_account = open("account.txt", "r")
account = raw_account.readlines()
raw_account.close()

line = 0
for x in account:
    account[line] = account[line].replace("\n","")
    account[line] = account[line].replace("Email:","")
    account[line] = account[line].replace("Password:","")
    account[line] = account[line].replace("Bearer:","")
    account[line] = account[line].replace(" ","")
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


#update()

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
            scraperset = False


get_config_data()


def autonamemc(email, password):
    return
    cwd = os.getcwd()
    os.chdir(f"{cwd}\\namemc")
    # os.system("python setup.py install")
    os.system(f"python start.py -u {email} -p {password}")


def changeskin(bearer):
    #print(bearer, "this")
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
        print("{Fore.GREEN}Congrats!\n{Fore.LIGHTGREEN_EX}You successfully sniped {Fore.GREEN}{name}{Fore.LIGHTGREEN_EX} at {Fore.GREEN}{snipedtime}{Fore.LIGHTGREEN_EX}!")
        if namemc == "True":
            autonamemc(email, password)
        exit()

machoapi = None
starapi = None
ccapi = None

async def check_connections():
    global scraperset
    print()
    print(f"\r{Fore.YELLOW}Testing connections: [________] 0%", end = "\r")

    try: # Internet
        requests.get("https://google.com", timeout = 5)
        print(f"\r{Fore.YELLOW}Testing connections: [██______] 25%", end = "\r")
    except:
        print(f"\r{Fore.RED}Testing connections: [________] 0% ")
        print()
        print(f"{Fore.RED}Make sure your computer is connected to the internet!")
        exit()
    try: # Coolkidmacho API
        global machoapi
        machoapi = False
        req = requests.get("https://api.coolkidmacho.com/droptime/abc", timeout=5)
        if req.status_code == 404:
            raise Exception
        machoapi = True
    except:
        pass
    finally:
        print(f"\r{Fore.YELLOW}Testing connections: [████____] 50%", end = "\r")
    try: # Star.shopping API
        global starapi
        starapi = False
        req = requests.get("http://api.star.shopping/droptime/abc", timeout=5)
        if req.status_code == 503:
            raise Exception
        starapi = True
    except:
        pass
    finally:
        print(f"\r{Fore.YELLOW}Testing connections: [██████__] 75%", end = "\r")
    try: # Droptime.cc API
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
        if machoapi == False and starapi == False and ccapi == False:
            scraperset = True
        if machoapi == False and scraperset == False:
            print()
            print(f"{Fore.LIGHTRED_EX}Autosniping and searchbased sniping are currently unavailable!")
            act = inp("Do you want to activate them anyway? Y/N: ").lower()
            if act == "y":
                file = open("config.json", "w")
                global webhook
                if webhook == None:
                    webhook = ""
                content = {
                    "namemc": f"{namemc}",
                    "msauth": f"{msauth}",
                    "scraper": "True",
                    "webhook": f"{webhook}",
                    "searches": searches
                }
                file.write(json.dumps(content, indent=2))
                file.close()
                scraperset = True

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
    async with session.get(f"http://api.coolkidmacho.com/droptime/{username}") as r:
        try:
            if machoapi == False:
                raise Exception()
            r_json = await r.json()
            droptime = int(float(r_json["UNIX"]))
            return droptime
        except:
            async with session.get(f"http://api.star.shopping/droptime/{username}", headers={"User-Agent": "Sniper"}) as r2:
                try:
                    if starapi == False:
                        raise Exception()
                    r_json = await r2.json()
                    droptime = int(float(r_json["unix"]))
                    return droptime
                except:
                    async with session.get(f"http://api.droptime.cc/droptime/{username}") as r3:
                        try:
                            if ccapi == False:
                                raise Exception()
                            r_json = await r3.json()
                            droptime = int(float(r_json["unix"]))
                            return droptime
                        except:
                            try:
                                prevOwner = inp(
                                    f"What is the current username of the account that owned {username} before this?:   "
                                )
                                res = requests.post("https://mojang-api.teun.lol/upload-droptime",json={"name": username, "prevOwner": prevOwner}).json()
                                droptime = res["UNIX"]
                                return droptime
                            except:
                                print(f"{Fore.LIGHTRED_EX}Droptime for name not found, make sure you entered the details into the feild correctly!{Fore.RESET}")
                                exit()


async def get_scaper_drop(username: str) -> int:
    nameinfo = scraper.getNameInfo(username)
    drop = nameinfo["droptime"]
    if drop != None:
        return drop
    else:
        return 0

async def get_profile_information(bearer: str, attr: str) -> str:
    async with aiohttp.ClientSession() as s:
        headers = {"Content-type": "application/json", "Authorization": "Bearer " + bearer}
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
    search, char = 0
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
                names = requests.get("https://api.coolkidmacho.com/three").json()
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


async def snipe(target: str, offset: int, bearer_token: str) -> None:
    async with aiohttp.ClientSession() as session:
        if scraperset:
            try:
                droptime = get_scaper_drop(target)
                if droptime == 0:
                    print(f"{Fore.RED}This name isn't dropping!")
                    exit()
            except Exception as e:
                print(e)
                print(f"{Fore.RED}Can't scrape names! Report this to a suport channel!")
                exit()
        else:
            try:
                droptime = await get_droptime(target, session)  # find the droptime!
            except:
                print(f"{Fore.RED}Can't get droptime!")
                exit()
        offset = int(offset)
        print(offset)
        snipe_time = droptime - (offset / 1000)
        print("current time in unix format is: ", time.time())
        print(f"{Fore.YELLOW}Calculating...")
        print(
            f"{Fore.GREEN}sniping {target} at {droptime} unix time{Fore.RESET} sleeping. "
        )
        print(
            f"{Fore.CYAN}You have successfully queued a name!{Fore.BLUE} Please wait till the name drops!"
        )
        while time.time() < snipe_time - 10:
            await asyncio.sleep(0.001)
        if (
            requests.get(
                "https://api.mojang.com/users/profiles/minecraft/" + target
            ).status_code
            == 204
        ):
            while time.time() < snipe_time:
                await asyncio.sleep(0.001)
            coroutines = [send_request(session, bearer_token, target) for _ in range(6)]
            await asyncio.gather(*coroutines)
            store(droptime, offset)
            changeskin(bearer_token)
            custom(email, password, bearer_token, target)
        else:
            print(f"{Fore.RED}{target} is no longer dropping. Skipping...")


async def autosniper(bearer: str) -> None:
    sel = inp(
        f"{Fore.YELLOW}For search based sniping select {Fore.GREEN}s{Fore.RESET}\n{Fore.YELLOW}For Auto 3char Enter {Fore.GREEN}3{Fore.RESET}: "
    )
    if sel == "s":
        try:
            print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
            if scraperset:
                searches = inp(
                    "How many searches do you want?: "
                )
                try:
                    names = scraper.getNameDrops(searches, 0)
                except Exception as e:
                    print(e)
                    print(f"{Fore.RED}Failed to use scaper, report this to a support channel.{Fore.RESET}")
                    exit()
            else:
                searches = inp(
                    "How many searches do you want ( 50, 100, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000 )?: "
                )
                try:
                    names = requests.get(f"http://api.coolkidmacho.com/up/{searches}").json()[
                    "names"
                ]
                except:
                    print(f"{Fore.LIGHTRED_EX}API is down, can't use this feature...")
                    exit()
        except Exception as e:
            print(e)
            print(f"{Fore.RED}Failed to get searched names, report this to a support channel.{Fore.RESET}")
            exit()
    if sel == "3":
        if scraperset:
            try:
                print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
                names = scraper.getNameDrops(0,3)
            except Exception as e:
                print(e)
                print(f"{Fore.RED}Failed to use scaper, report this to a support channel.{Fore.RESET}")
                exit()
        else:
            try:
                print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
                names = requests.get(f"https://api.coolkidmacho.com/three").json()
            except:
                print(
                    f"{Fore.RED}Failed to get 3names names, report this to a support channel but dont ping anyone.{Fore.RESET}"
                )

    delay = inp(f"Delay for snipe:  ")
    if tuned_delay == None:
        pass
    else:
        delay = tuned_delay
    print(tuned_delay, "tuned delay value")
    for nameseg in names:
        tree = requests.get(f"https://api.ashcon.app/mojang/v2/user/{nameseg}")
        #print(tree.status_code)
        if tree.status_code == 404 or tree.status_code == 400:

            name = nameseg
            print(f"Sniping: {name}")
            if tuned_delay is None:
                print(f"{Fore.CYAN}Defaulting...{Fore.RESET}")
                pass
            else:
                delay = tuned_delay
                print(f"{Fore.CYAN}Delay Tuned{Fore.RESET}")
            print(f"{Fore.CYAN}delay is now ", delay + Fore.RESET)
            await snipe(name, delay, bearer)
        else:
            pass


#   Mojang setup and snipe


async def send_mojang_request(s: aiohttp.ClientSession, bearer: str, name: str, num: int) -> None:
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
            print(f"{Fore.LIGHTCYAN_EX}Response {num} received @ {datetime.now()} with the status {Fore.GREEN}{r.status}")
            success = True
        else:
            print(f"{Fore.LIGHTCYAN_EX}Response {num} received @ {datetime.now()} with the status {Fore.RED}{r.status}")
        print(f"{num} sent: {datetime.fromtimestamp(starttime)} recieved: {datetime.fromtimestamp(endtime)} difference: {difftime}s")
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
            if drop == 0:
                droptime = get_scaper_drop(target)
                if droptime == 0:
                    print(f"{Fore.RED}This name isn't dropping!")
                    exit()
            else:
                droptime = drop
        else:
            droptime = await get_droptime(target, session)
        offset = int(offset)
        snipe_time = droptime - (offset / 1000)
        conv_droptime = datetime.fromtimestamp(droptime).strftime('%H:%M:%S on %Y-%m-%d')
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


async def automojangsniper(token: str) -> None:
    print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
    searches = 0
    chars = 0
    sel = inp(
    f"{Fore.YELLOW}For search based sniping select {Fore.GREEN}s{Fore.RESET}\n{Fore.YELLOW}For Auto 3char Enter {Fore.GREEN}3{Fore.RESET}: "
    )
    if sel == "s":
        searches = inp("How many searches do you want?: ")
        searches = int(searches)
    elif sel == "3":
        chars = 3
    if scraperset:
        try:
            names = scraper.getNameDrops(searches, chars)
        except Exception as e:
            print(e)
            print(f"{Fore.RED}Failed to use scaper, report this to a support channel.{Fore.RESET}")
            exit()
    else:
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
                names = requests.get("https://api.coolkidmacho.com/three").json()
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
    for nameseg in names:
        name = nameseg["name"]
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
                await mojang_snipe(name, delay, token, droptime)
        else:
            namecheck = requests.get(f"https://api.ashcon.app/mojang/v2/user/{name}")
            if namecheck.status_code == 404:
                if tuned_delay is None:
                    print(f"{Fore.CYAN}Defaulting...{Fore.RESET}")
                    pass
                else:
                    delay = tuned_delay
                    print(f"{Fore.CYAN}Delay Tuned{Fore.RESET}")
                print("delay is now ", delay)
                await mojang_snipe(name, delay, token, 0)


async def gather_mojang_info() -> None:
    email = inp(f"Account Email:  ")
    password = pwinput.pwinput(prompt=f"{Fore.YELLOW}Password: ", mask="*")
    token = await get_mojang_token(email, password)
    style = inp(
            f"{Fore.YELLOW}What sniper mode?\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}a{Fore.YELLOW} for autosniper{Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}n{Fore.YELLOW} for single name sniping {Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}s{Fore.YELLOW} to show next 3chars: {Fore.RESET}"
        )
    if style == "a":
        await automojangsniper(token)
    elif style == "n" or "s":
        if style == "s":
            get_next_names(10)
        name = inp(f"Name to snipe:  ")
        delay = inp(f"Delay for snipe:  ")
        tuned_delay = delay
        await mojang_snipe(name, delay, token, 0)
        print("Sniping...")
    custom(email, password, token, name)


async def iterate_through_names(session: aiohttp.ClientSession) -> None:
    while True:
        async with session.get("https://api.3user.xyz/list") as r:
            r_json = await r.json()
            if r.status < 300:
                for name in r_json:
                    yield name["name"]
                asyncio.sleep(1)
            else:
                print(f"Failed to get names, retrying... | {r.status}")
                await asyncio.sleep(10)


async def start() -> None:
    global scraperset
    await check_connections()
    mainset = inp(
        f"\n\n{Fore.LIGHTBLUE_EX}What account type? \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}g{Fore.RESET}{Fore.LIGHTBLUE_EX} for giftcard snipes \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}m{Fore.RESET} {Fore.LIGHTBLUE_EX}for mojang snipes \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}ms{Fore.RESET} {Fore.LIGHTBLUE_EX}for microsoft snipes: "
    )
    if mainset == "m":

        reqnum = 3
        print(
            f"{Fore.LIGHTGREEN_EX}Mojang Account Selected, using Mojang Sniper{Fore.RESET}"
        )
        await gather_mojang_info()
        return
    elif mainset == "ms":

        print(
            f"{Fore.LIGHTGREEN_EX}Microsoft Account Selected, using Microsoft Sniper{Fore.RESET}"
        )
        autype = inp(
            f"To use microsoft email and password auth enter {Fore.GREEN}e{Fore.RESET}\n{Fore.YELLOW}To use Token enter {Fore.GREEN}t{Fore.RESET}:  "
        )
        if autype.lower() == "e":
            try:
                if ms_email == "" or ms_pw == "":
                    email = inp(f"Microsoft email: ")
                    password = pwinput.pwinput(prompt=f"{Fore.YELLOW}Password: ", mask="*")
                else:
                    email = ms_email
                    password = ms_pw
                resp = login(email, password)
                token = resp["access_token"]
                try:
                    login_name = await get_profile_information(token, "name")
                    print(f"{Fore.GREEN}Logged into {Fore.LIGHTCYAN_EX}{Style.BRIGHT}{login_name}")
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
                    print(f"{Fore.GREEN}Logged into {Fore.LIGHTCYAN_EX}{Style.BRIGHT}{login_name}")
                except:
                    print(f"{Fore.GREEN}No previous name")
        elif autype.lower() == "t":
            if manual_bearer == "":
                token = inp(f"What is your bearer token:  ")
            else:
                token = manual_bearer
            try:
                login_name = await get_profile_information(token, "name")
                print(f"{Fore.GREEN}Logged into {Fore.LIGHTCYAN_EX}{Style.BRIGHT}{login_name}")
            except:
                print(f"{Fore.GREEN}No previous name")
        else:
            print(f"{Fore.RED}You did not select a valid option.")
            exit()
        style = inp(
            f"{Fore.YELLOW}What sniper mode?\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}a{Fore.YELLOW} for autosniper{Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}n{Fore.YELLOW} for single name sniping {Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}s{Fore.YELLOW} to show next 3chars: {Fore.RESET}"
        )
        if style == "a":
            await automojangsniper(token)
            return
        elif style == "n" or style == "s":
            if style == "s":
                get_next_names(10)
            name = inp(f"Name to snipe:  ")
            global delay
            delay = inp(f"Delay for snipe:  ")
            global tuned_delay
            tuned_delay = delay
            await (mojang_snipe(name, delay, token, 0))
    elif mainset == "g":
        print(
            f"{Fore.LIGHTGREEN_EX}Giftcard Selected, using Microsoft Sniper{Fore.RESET}"
        )

        reqnum = 6
        autype = inp(
            f"To use microsoft email and password auth enter {Fore.GREEN}e{Fore.RESET}\n{Fore.YELLOW}To use Token enter {Fore.GREEN}t{Fore.RESET}:  "
        )
        if autype.lower() == "e":
            try:
                if ms_email == "" or ms_pw == "":
                    email = inp(f"Microsoft email:  ")
                    password = pwinput.pwinput(prompt=f"{Fore.YELLOW}Password: ", mask="*")
                else: 
                    email = ms_email
                    password = ms_pw
                resp = login(email, password)
                token = resp["access_token"]
            except:
                print(f"{Fore.RED}Failed MsAuth for you, use token.")
                if manual_bearer == "":
                    token = inp(f"What is your bearer token:  ")
                else:
                    token = manual_bearer

        elif autype.lower() == "t":
            if manual_bearer == "":
                token = inp(f"What is your bearer token:  ")
            else: 
                token = manual_bearer
        else:
            print(f"{Fore.RED}You did not select a valid option.")
            exit()

        style = inp(
            f"{Fore.YELLOW}What sniper mode?\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}a{Fore.YELLOW} for autosniper{Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}n{Fore.YELLOW} for single name sniping {Fore.RESET}\n"
            f"{Fore.YELLOW}Enter {Fore.GREEN}s{Fore.YELLOW} to show next 3chars: {Fore.RESET}"
        )
        if style == "a":
            await autosniper(token)
        elif style == "n" or style == "s":
            if style == "s":
                get_next_names(10)
            name = inp(f"Name to snipe:  ")
            delay = inp(f"Delay for snipe:  ")
            tuned_delay = delay
            await snipe(name, delay, token)
        else:
            print(f"{Fore.RED}Please select a valid option")
            inp(f"Press enter to exit: ")
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
#print(vars(args))
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
        asyncio.run(mojang_snipe(name, delay, token, 0))
        if success == True:
            custom(email, password, token, name)
    elif mainset == "ms":
        resp = login(email, password)
        token = resp["access_token"]
        asyncio.run(mojang_snipe(name, delay, token, 0))
    elif mainset == "g":
        resp = login(email, password)
        token = resp["access_token"]
        asyncio.run(snipe(name, delay, token))

loop = asyncio.get_event_loop()
loop.run_until_complete(start())
