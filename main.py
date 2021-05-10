import asyncio
import time
from datetime import datetime
import aiohttp
import requests
import warnings
import sys
from colorama import Fore, Back, Style
from colorama import init

init(convert=True, autoreset=True)

logo = rf"""{Fore.GREEN}
  __  __ __  __  ___ _____    __  __  _ _ ___ ___ ___
/' _/|  V  |/  \| _ \_   _| /' _/|  \| | | _,\ __| _ \
`._`.| \_/ | /\ | v / | |   `._`.| | ' | | v_/ _|| v /
|___/|_| |_|_||_|_|_\ |_|   |___/|_|\__|_|_| |___|_|_\
"""
print(logo)
print(Fore.BLUE + "Created by Coolkidmacho#7567")
print("With the wonderful assistance of Kqzz#0001\n")
end = []
orgdel = 0
global delay
delay = 0
global changeversion
changeversion = ""
global reqnum
reqnum = 0
global tuned_delay
tuned_delay = None


def store(droptime: int, offset: int) -> None:
    print(offset, "inputted delay")
    stamp = end[reqnum - 1]
    datetime_time = datetime.fromtimestamp(droptime)
    ti = str(stamp - datetime_time)
    print(ti)
    finaldel = ti.split(":")[2].split(".")
    print(finaldel)
    if int(finaldel[0]) != 0:
        print(
            "Cannot tune your delay, please sync your time"
            " using http://www.thinkman.com/dimension4/download.htm")
        changeversion = "inc"
        tuned_delay = 0
        print(
            "program will continue, if it fails again please restart after "
            "installing dimension4 and also set the delay to 0 for that"
        )

    else:
        change = finaldel[1]
        change3 = f"{change[0]}{change[1]}{change[2]}"
        if int(change[0]) == 0:
            changeversion = "dec"
            changeint = 100 - int(f"{change[1]}{change[2]}")
            print("changeint", changeint)
        else:
            changeversion = "inc"
            changeint = int(change3) - 100
            print("changeint", changeint)

        if changeversion == "dec":
            tuned_delay = int(offset) - int(changeint)
        if changeversion == "inc":
            tuned_delay = int(offset) + int(changeint)
        print(f"delay: {offset}  tuned_delay  {tuned_delay}")


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
            f"Response received @ {datetime.now()}"
            f" with the status {r.status}"
        )
        end.append(datetime.now())


async def get_droptime(username: str, session: aiohttp.ClientSession) -> int:
    async with session.get(
            f"https://api.kqzz.me/api/namemc/droptime/{username}"
    ) as r:
        if r.status < 300:
            r_json = await r.json()
            droptime = r_json["droptime"]
            print(f"droptime: {droptime}")
            return droptime
        else:
            print("failed to get droptime, name not dropping")
            time.sleep(2)
            print("exiting")
            time.sleep(2)
            exit()


async def snipe(target: str, offset: int, bearer_token: str) -> None:
    async with aiohttp.ClientSession() as session:
        droptime = await get_droptime(target, session)
        offset = int(offset)
        snipe_time = droptime - (offset / 1000)
        while time.time() < snipe_time:
            await asyncio.sleep(.001)
        coroutines = [
            send_request(session, bearer_token, target) for _ in range(6)
        ]
        await asyncio.gather(*coroutines)
        store(droptime, offset)


async def autosniper(bearer: str) -> None:
    print("starting")
    names = requests.get("https://api.3user.xyz/list").json()
    delay = int(input("What delay:  "))
    tuned_delay = delay
    for nameseg in names:
        print(nameseg)
        name = nameseg["name"]
        if tuned_delay is None:
            print("defaulting")
            pass
        else:
            delay = tuned_delay
            print("delay tuned")
        print("delay is now ", delay)
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
    async with aiohttp.ClientSession() as session:
        authenticate_json = {"username": email, "password": password}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
                   "Content-Type": "application/json"}
        async with session.post("https://authserver.mojang.com/authenticate", json=authenticate_json,
                                headers=headers) as r:
            print(r.status)
            if r.status == 200:
                resp_json = await r.json()
                print(resp_json)
                auth = {"Authorization": "Bearer: " + resp_json["accessToken"]}
                access_token = resp_json["accessToken"]
            else:
                print("INVALID CREDENTIALS")

        async with session.post("https://api.mojang.com/user/security/challenges", headers=auth) as r:
            print(r.status)
            if r.status == 200:
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
                                print("Logged into your account successfully!")
                        except Exception:
                            print("Logged into your account successfully!")
    return access_token


async def mojang_snipe(target: str, offset: int, bearer_token: str) -> None:
    async with aiohttp.ClientSession() as session:
        droptime = await get_droptime(target, session)
        offset = int(offset)
        snipe_time = droptime - (offset / 1000)
        while time.time() < snipe_time:
            await asyncio.sleep(.001)
        coroutines = [
            send_mojang_request(session, bearer_token, target)
            for _ in range(3)
        ]
        await asyncio.gather(*coroutines)
        store(droptime, offset)


async def automojangsniper(token: str) -> None:
    print("starting")
    r = requests.get("https://api.3user.xyz/list")
    if r.status_code != 200:
        print(f"Failed to get names from 3user | {r.status}")
        quit()
    else:
        names = r.json()
    delay = int(input("What delay:  "))
    tuned_delay = delay
    for nameseg in names:
        print(nameseg)
        name = nameseg["name"]
        if tuned_delay is None:
            print("defaulting")
            pass
        else:
            delay = tuned_delay
            print("delay tuned")
        print("delay is now ", delay)
        await mojang_snipe(name, delay, token)


async def gather_mojang_info() -> None:
    email = input("Account Email:  ")
    password = input("Password:  ")
    token = await get_mojang_token(email, password)
    style = input(
        "What sniper mode? Enter `a` for autosniper"
        " and `n` for single name sniping:  "
    )
    if style == "a":
        await automojangsniper(token)
    elif style == "n":
        name = input("what name do you want to snipe:  ")
        delay = input("what delay do you want:  ")
        tuned_delay = delay
        await mojang_snipe(name, delay, token)


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
        f"What account type? Enter `g` for giftcard "
        f"and `m` for mojang and `ms` for microsoft accounts:  "
    )
    if mainset == "m":
        print("selected mojang account, transferring to mojang sniper.")
        await gather_mojang_info()
        return
    elif mainset == "ms":
        print(
            "Microsoft account selected,"
            " transferring to microsoft sniper."
        )
        token = input("What is your bearer token:  ")
        style = input(
            "What sniper mode? Enter `a` for autosniper"
            " and `n` for single name sniping:  "
        )
        if style == "a":
            await automojangsniper(token)
            return
        elif style == "n":
            name = input("what name do you want to snipe:  ")
            global delay
            delay = input("what delay do you want:  ")
            global tuned_delay
            tuned_delay = delay
            await (mojang_snipe(name, delay, token))
    elif mainset == "g":
        token = input("What is your bearer token:  ")
        style = input(
            "What sniper mode? Enter `a` for autosniper and"
            " `n` for single name sniping:  "
        )
        if style == "a":
            await autosniper(token)
        elif style == "n":
            name = input("what name do you want to snipe:  ")
            delay = input("what delay do you want:  ")
            tuned_delay = delay
            loop = asyncio.get_event_loop()
            loop.run_until_complete(snipe(name, delay, token))
        else:
            print("You did not enter a valid option please reselect.")
            time.sleep(3)
            print("exiting")
            exit()
    else:
        print("You did not enter a proper value. Ending.")
        exit()


if __name__ == '__main__':
    try:
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start())
    except Exception as e:
        print(e)
        print("ending, if this is unexpected please report to devs")
