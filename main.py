import asyncio
import os
import time
import warnings
from datetime import datetime
from getpass import getpass
import aiohttp
import requests
from colorama import Fore
from colorama import init
import json
import subprocess


init(convert=True, autoreset=True)

# os.system("cls" if os.name == "nt" else "clear")
logo = rf"""{Fore.GREEN}
  __  __ __  __  ___ _____    __  __  _ _ ___ ___ ___
/' _/|  V  |/  \| _ \_   _| /' _/|  \| | | _,\ __| _ \
`._`.| \_/ | /\ | v / | |   `._`.| | ' | | v_/ _|| v /
|___/|_| |_|_||_|_|_\ |_|   |___/|_|\__|_|_| |___|_|_\
"""
print(logo)
print(Fore.BLUE + "Created by coolkidmacho#0001" + Fore.RESET)
print(Fore.BLUE + "With the wonderful assistance of Kqzz#0001\n" + Fore.RESET)
print("Make sure to join https://discord.gg/KweaD6G97f")
print("If you want to boost or donate message coolkidmacho#0001 on discord")
end = []
orgdel = 0
global delay
delay = 0
global changeversion
changeversion = ""
global tuned_delay
tuned_delay = None
global success
success=False

reqnum = 3



def get_config_data():
    with open("config.json") as e:
        menu = json.loads(e.read())
        print(menu)
        global namemc
        namemc = menu["namemc"]

get_config_data()


def autonamemc(email, password  ):
    return
    cwd = os.getcwd()
    os.chdir(f"{cwd}\\namemc")
    # os.system("python setup.py install")
    os.system(f"python start.py -u {email} -p {password}")


def store(droptime: int, offset: int) -> None:                        # Dodgy timing script!
    print(offset, ": Delay Used")
    global reqnum
    if reqnum == 3:
        set = 1
    else:
        set=2
    stamp = end[set]
    datetime_time = datetime.fromtimestamp(droptime)
    finaldel = str(stamp - datetime_time).split(":")[2].split(".")

    print(finaldel)
    if int(finaldel[0]) != 0:
        changeversion = "inc"
        tuned_delay = 0

        print(
            f"""{Fore.LIGHTRED_EX}Cannot tune your delay, please sync your time\n
            using http://www.thinkman.com/dimension4/download.htm
            \nprogram will continue, if it fails again please restart after \n
            installing dimension4 and also set the delay to 0 for that{Fore.RESET}"""
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
        print(f"{Fore.CYAN}Delay:{Fore.RESET} {offset}  {Fore.LIGHTGREEN_EX}Tuned Delay:{Fore.RESET}  {tuned_delay}")


async def send_request(s: aiohttp.ClientSession, bearer: str, name: str) -> None:
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + bearer
    }

    json = {"profileName": name}

    async with s.post(
            "https://api.minecraftservices.com/minecraft/profile",
            json=json,
            headers=headers
    ) as r:
        print(
            f"{Fore.LIGHTRED_EX if r.status != 200 else Fore.LIGHTGREEN_EX}Response received @ {datetime.now()}{Fore.RESET}"
            f"{Fore.LIGHTRED_EX if r.status != 200 else Fore.LIGHTGREEN_EX} with the status {r.status}{Fore.RESET}"
        )
        end.append(datetime.now())
        if r.status==200:
            success=True


async def get_droptime(username: str, session: aiohttp.ClientSession) -> int:
    async with session.get(
            f"https://mojang-api.teun.lol/droptime/{username}"
    ) as r:
        try:
            r_json = await r.json()
            droptime = r_json["UNIX"]
            return droptime
        except:
            try:
                prevOwner = input(
                    f'{Fore.CYAN}What is the current username of the account that owned {username} before this?:   {Fore.RESET}')
                r = requests.post('https://mojang-api.teun.lol/upload-droptime',
                                  json={'name': username, 'prevOwner': prevOwner})
                print(r.text)
                droptime = r.json()['UNIX']
                return droptime
            except:
                print(f"{Fore.LIGHTRED_EX}Droptime for name not found, make sure you entered the details into the feild correctly!{Fore.RESET}")

    # else:
    #     print(f"{Fore.LIGHTRED_EX}Droptime for name not found, Please check if name is still dropping{Fore.RESET}")
    #     time.sleep(2)
    #     input(f"{Fore.LIGHTRED_EX}Press Enter to exit: {Fore.RESET}")
    #     exit()


async def snipe(target: str, offset: int, bearer_token: str) -> None:
    async with aiohttp.ClientSession() as session:
        droptime = await get_droptime(target, session) # find the droptime!
        offset = int(offset)
        print(offset)
        snipe_time = droptime - (offset / 1000)
        print("current time in unix format is: ",time.time())
        print("Calculating...")
        print(f"sniping {target} at {droptime} unix time")
        while time.time() < snipe_time:
            await asyncio.sleep(.001)
        coroutines = [
            send_request(session, bearer_token, target) for _ in range(6)
        ]
        await asyncio.gather(*coroutines)
        store(droptime, offset)


async def autosniper(bearer: str) -> None:
    print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
    names = requests.get("https://api.3user.xyz/list").json()
    delay = input(f"{Fore.CYAN}Delay for snipe:  {Fore.RESET}")
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
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + bearer
    }

    async with s.put(
            f"https://api.minecraftservices.com/minecraft/profile/name/{name}",
            headers=headers
    ) as r:
        print(
            f"Response received @ {datetime.now()}"
            f" with the status {r.status}"
        )
        end.append(datetime.now())


async def get_mojang_token(email: str, password: str) -> str:
    # Login code is partially from mcsniperpy thx!
    questions = []

    async with aiohttp.ClientSession() as session:
        authenticate_json = {"username": email, "password": password}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
                   "Content-Type": "application/json"}
        async with session.post("https://authserver.mojang.com/authenticate", json=authenticate_json,
                                headers=headers) as r:
            # print(r.status)
            if r.status == 200:
                resp_json = await r.json()
                # print(resp_json)
                auth = {"Authorization": "Bearer: " + resp_json["accessToken"]}
                access_token = resp_json["accessToken"]
                # print(f"{Fore.LIGHTGREEN_EX}Auth: {auth}\n\nAccess Token: {access_token}")
            else:
                print(f"{Fore.LIGHTRED_EX}INVALID CREDENTIALS{Fore.RESET}")

        async with session.get("https://api.mojang.com/user/security/challenges", headers=auth) as r:
            answers = []
            if r.status < 300:
                resp_json = await r.json()
                if resp_json == []:
                    async with session.get("https://api.minecraftservices.com/minecraft/profile/namechange",
                                           headers={"Authorization": "Bearer " + access_token}) as nameChangeResponse:
                        ncjson = await nameChangeResponse.json()
                        print(ncjson)
                        try:
                            if ncjson["nameChangeAllowed"] is False:
                                print(
                                    "Your Account is not"
                                    " eligible for a name change!"
                                )
                                exit()
                            else:
                                print(f"{Fore.LIGHTGREEN_EX}Logged into your account successfully!{Fore.RESET}")
                        except Exception:
                            print("logged in correctly")
                else:
                    try:
                        for x in range(3):
                            ans = input(resp_json[x]["question"]["question"])
                            answers.append({"id": resp_json[x]["answer"]["id"], "answer": ans})
                    except IndexError:
                        print(f"{Fore.LIGHTRED_EX}Please provide answers to the security questions{Fore.RESET}")
                        return
                    async with session.post("https://api.mojang.com/user/security/location", json=answers,
                                            headers=auth) as r:
                        if r.status < 300:
                            print(f"{Fore.LIGHTGREEN_EX}Logged in{Fore.RESET}")
                        else:
                            print(f"{Fore.LIGHTRED_EX}Security Questions answers were incorrect, restart the program!{Fore.RESET}")
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
            await asyncio.sleep(.001)
        coroutines = [
            send_mojang_request(session, bearer_token, target)
            for _ in range(3)
        ]
        await asyncio.gather(*coroutines)
        store(droptime, offset)


async def automojangsniper(token: str) -> None:
    print(f"{Fore.LIGHTGREEN_EX}Starting...{Fore.RESET}")
    names = requests.get("https://api.3user.xyz/list").json()
    delay = input(f"{Fore.CYAN}Delay for snipe:  {Fore.RESET}")
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
    email = input(f"Account Email:  ")
    password = getpass(f"Password:  ")
    print(password)
    token = await get_mojang_token(email, password)
    style = input(
        "What sniper mode? Enter `a` for autosniper"
        " and `n` for single name sniping:  "
    )
    if style == "a":
        await automojangsniper(token)
    elif style == "n":
        name = input(f"Name to snipe:  ")
        delay = input(f"Delay for snipe:  ")
        tuned_delay = delay
        await mojang_snipe(name, delay, token)
        if namemc=="True":
            autonamemc(email, password)


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
    mainset = input(
        f"What account type? Enter `g` for giftcard snipes "
        f"and `m` for mojang and `ms` for microsoft accounts:  "
    )
    if mainset == "m":

        reqnum = 3
        print(f"{Fore.LIGHTGREEN_EX}Mojang Account Selected, using Mojang Sniper{Fore.RESET}")
        await gather_mojang_info()
        return
    elif mainset == "ms":

        reqnum = 3
        print(
            f"{Fore.LIGHTGREEN_EX}Microsoft Account Selected, using Microsoft Sniper{Fore.RESET}"
        )
        token = input(f"What is your bearer token:  ")
        style = input(
            "What sniper mode? Enter `a` for autosniper"
            " and `n` for single name sniping:  "
        )
        if style == "a":
            await automojangsniper(token)
            return
        elif style == "n":
            name = input(f"Name to snipe:  ")
            global delay
            delay = input(f"Delay for snipe:  ")
            global tuned_delay
            tuned_delay = delay
            await (mojang_snipe(name, delay, token))
    elif mainset == "g":


        reqnum=6
        token = input(f"What is your bearer token:  ")
        style = input(
            f"What sniper mode? Enter `a` for autosniper and"
            f" `n` for single name sniping:  "
        )
        if style == "a":
            await autosniper(token)
        elif style == "n":
            name = input(f"Name to snipe:  ")
            delay = input(f"Delay for snipe:  ")
            tuned_delay = delay
            await snipe(name, delay, token)
        else:
            print(f"Please select a valid option")
            input(f"Press enter to exit: ")
            exit()
    else:
        print("You did not enter a proper value. Ending.")
        exit()


# if __name__ == '__main__':
#     try:
#         warnings.filterwarnings("ignore", category=RuntimeWarning)
loop = asyncio.get_event_loop()
loop.run_until_complete(start())
    #
    # except Exception as e:
    #     print(e)
    #     print(f"{Fore.LIGHTRED_EX}An Error Occured, If this is unexpected please report the error to devs{Fore.RESET}")
