import argparse
import asyncio
import json
import os
import time
import urllib.request
from datetime import datetime, timezone

import aiohttp
import requests
from colorama import Fore, Style, init

from msauth import login

init(convert=True, autoreset=True)

# os.system("cls" if os.name == "nt" else "clear")
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
global webhook
autoskin = True


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


update()


def get_config_data():
    with open("config.json") as e:
        menu = json.loads(e.read())
        # print(menu)
        global namemc
        namemc = menu["namemc"]
        global msauth
        msauth = menu["msauth"]
        global webhook
        webhook = menu["webhook"]
        if webhook == "":
            webhook = None
        global searches
        searches = menu["searches"]


get_config_data()


def autonamemc(email, password):
    return
    cwd = os.getcwd()
    os.chdir(f"{cwd}\\namemc")
    # os.system("python setup.py install")
    os.system(f"python start.py -u {email} -p {password}")


def changeskin(bearer):
    print(bearer, "this")
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
    stamp = end[0]
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


def custom(email, password):
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

        if namemc == "True":
            autonamemc(email, password)


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
    async with session.get(f"https://api.coolkidmacho.com/droptime/{username}") as r:
        try:
            r_json = await r.json()
            print(r_json)
            droptime = int(r_json["UNIX"])
            return droptime
        except:
            try:
                prevOwner = inp(
                    f"What is the current username of the account that owned {username} before this?:   "
                )
                r = requests.post(
                    "https://mojang-api.teun.lol/upload-droptime",
                    json={"name": username, "prevOwner": prevOwner},
                )
                print(r.text)
                droptime = r.json()["UNIX"]
                return droptime
            except:
                print(
                    f"{Fore.LIGHTRED_EX}Droptime for name not found, make sure you entered the details into the feild correctly!{Fore.RESET}"
                )


async def snipe(target: str, offset: int, bearer_token: str) -> None:
    async with aiohttp.ClientSession() as session:
        droptime = await get_droptime(target, session)  # find the droptime!
        offset = int(offset)
        print(offset)
        snipe_time = droptime - (offset / 1000)
        print("current time in unix format is: ", time.time())
        print("Calculating...")
        print(f"sniping {target} at {droptime} unix time")
        while time.time() < snipe_time:
            await asyncio.sleep(0.001)
        coroutines = [send_request(session, bearer_token, target) for _ in range(6)]
        await asyncio.gather(*coroutines)
        store(droptime, offset)
        changeskin(bearer_token)


async def autosniper(bearer: str) -> None:
    sel = inp(
        f"For search based sniping select {Fore.GREEN}s{Fore.RESET}\nFor Auto 3char Enter {Fore.GREEN}3{Fore.RESET}"
    )
    if sel == "s":
        try:
            print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
            names = requests.get(
                f"https://api.kqzz.me/api/namemc/upcoming/?searches={searches}"
            ).json()
        except:
            print(
                f"{Fore.Red}Failed to get searched names, report this to a support channel.{Fore.RESET}"
            )
    if sel == "3":
        try:
            print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
            names = requests.get(f"https://api.3user.xyz/list").json()
        except:
            print(
                f"{Fore.Red}Failed to get 3names names, report this to a support channel but dont ping anyone.{Fore.RESET}"
            )

    delay = inp(f"Delay for snipe:  ")
    if tuned_delay == None:
        pass
    else:
        delay = tuned_delay
    print(tuned_delay, "tuned delay value")

    for nameseg in names:
        name = nameseg["name"]
        print(f"Sniping: {name}")
        if tuned_delay is None:
            print(f"{Fore.CYAN}Defaulting...{Fore.RESET}")
            pass
        else:
            delay = tuned_delay
            print(f"{Fore.CYAN}Delay Tuned{Fore.RESET}")
        print(f"{Fore.CYAN}delay is now ", delay + Fore.RESET)
        await snipe(name, delay, bearer)


#   Mojang setup and snipe


async def send_mojang_request(s: aiohttp.ClientSession, bearer: str, name: str) -> None:
    headers = {"Content-type": "application/json", "Authorization": "Bearer " + bearer}

    async with s.put(
        f"https://api.minecraftservices.com/minecraft/profile/name/{name}",
        headers=headers,
    ) as r:
        print(f"Response received @ {datetime.now()}" f" with the status {r.status}")
        global success
        if r.status == 200:

            success = True
        else:
            success = False
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


async def mojang_snipe(target: str, offset: int, bearer_token: str) -> None:
    async with aiohttp.ClientSession() as session:
        droptime = await get_droptime(target, session)
        offset = int(offset)
        print(offset)
        snipe_time = droptime - (offset / 1000)
        print(time.time())
        print(f"sniping {target} at {droptime}")
        while time.time() < snipe_time:
            await asyncio.sleep(0.001)
        coroutines = [
            send_mojang_request(session, bearer_token, target) for _ in range(2)
        ]
        await asyncio.gather(*coroutines)
        store(droptime, offset)


async def automojangsniper(token: str) -> None:
    print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
    names = requests.get("https://api.3user.xyz/list").json()
    delay = inp(f"Delay for snipe:  ")
    print(tuned_delay, "tuned delay value")
    for nameseg in names:
        name = nameseg["name"]
        if tuned_delay is None:
            print(f"{Fore.CYAN}Defaulting...{Fore.RESET}")
            pass
        else:
            delay = tuned_delay
            print(f"{Fore.CYAN}Delay Tuned{Fore.RESET}")
        print("delay is now ", delay)
        await mojang_snipe(name, delay, token)


async def gather_mojang_info() -> None:
    email = inp(f"Account Email:  ")
    password = inp(f"Password:  ")
    print(password)
    token = await get_mojang_token(email, password)
    style = inp(
        "What sniper mode? Enter `a` for autosniper"
        " and `n` for single name sniping:  "
    )
    if style == "a":
        await automojangsniper(token)
    elif style == "n":
        name = inp(f"Name to snipe:  ")
        delay = inp(f"Delay for snipe:  ")
        tuned_delay = delay
        await mojang_snipe(name, delay, token)
        print("doin")
    custom(email, password)


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
    mainset = inp(
        f"\n\n{Fore.LIGHTBLUE_EX}What account type? \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}g{Fore.RESET}{Fore.LIGHTBLUE_EX} for giftcard snipes \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}m{Fore.RESET} {Fore.LIGHTBLUE_EX}for mojang snipes \n"
        f"{Fore.LIGHTBLUE_EX}Enter {Fore.GREEN}ms{Fore.RESET} {Fore.LIGHTBLUE_EX}for microsoft snipes!:  "
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
                email = inp(f"what is your microsoft email:  ")
                password = inp("password:  ")
                resp = login(email, password)
                token = resp["access_token"]
            except:
                print(f"{Fore.RED}Failed MsAuth for you, use token.")
                token = inp(f"What is your bearer token:  ")
        elif autype.lower() == "t":
            token = inp(f"What is your bearer token:  ")
        else:
            print(f"{Fore.RED}You did not select a valid option.")
        style = inp(
            "What sniper mode? Enter `a` for autosniper"
            " and `n` for single name sniping:  "
        )
        if style == "a":
            await automojangsniper(token)
            return
        elif style == "n":
            name = inp(f"Name to snipe:  ")
            global delay
            delay = inp(f"Delay for snipe:  ")
            global tuned_delay
            tuned_delay = delay
            await (mojang_snipe(name, delay, token))
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
                email = inp(f"what is your microsoft email:  ")
                password = inp("password:  ")
                resp = login(email, password)
                token = resp["access_token"]
            except:
                print(f"{Fore.RED}Failed MsAuth for you, use token.")
                token = inp(f"What is your bearer token:  ")

        elif autype.lower() == "t":
            token = inp(f"What is your bearer token:  ")
        else:
            print(f"{Fore.RED}You did not select a valid option.")
            exit()

        style = inp(
            f"What sniper mode? Enter `a` for autosniper and"
            f" `n` for single name sniping:  "
        )
        if style == "a":
            await autosniper(token)
        elif style == "n":
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
print(vars(args))
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
        asyncio.run(mojang_snipe(name, delay, token))
        if success == True:
            custom(email, password)
    elif mainset == "ms":
        resp = login(email, password)
        token = resp["access_token"]
        asyncio.run(mojang_snipe(name, delay, token))
    elif mainset == "g":
        resp = login(email, password)
        token = resp["access_token"]
        asyncio.run(snipe(name, delay, token))

else:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
