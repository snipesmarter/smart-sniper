<h1 align="center">
Smart Sniper
</h1>

<h1 align="center"><b>Discontinued!</b><br><br>
Namesniping was terminated by Mojang with the removal of the public namehistory for accounts. <br><br>
<a href="https://help.minecraft.net/hc/en-us/articles/8969841895693-Username-History-API-Removal-FAQ-">Official Announcement</a></h1>
<p align="center">
	<a href="https://github.com/snipesmarter/smart-sniper">
	<img
		alt="GitHub Stars"
		src="https://img.shields.io/github/stars/snipesmarter/smart-sniper?color=%2370a1d2&label=Stars%20%E2%AD%90"></a>
    <a href="https://discord.gg/2MeaJvrS2p"><img src="https://img.shields.io/discord/840342619329658921?color=%2370a1d2&label=Discord&logo=discord&logoColor=white"></a>
</p>
<span>Created and maintained by Coolkidmacho#0001</span>

<h5><b>Donations are appreciated for testing and further development, they also help me out.</b></h5>

## The most adaptive minecraft username sniper in the industry 

SmartSniper is a high tech adaptive sniper. This sniper's autosniping and automatic delay tuning assists in helping you obtain the best username possible!


### Join the Discord for live updates, polls, and support: https://discord.gg/KweaD6G97f

## Features

- Autosniping 3 Letters
- Auto Delay Tuning
- Gift Card Sniping
- Intuitive CUI
- Normal Sniping
- Automatic Microsoft Authorization
- Automatic NameMC Claiming
- Webhook on Success



> The overseeing design goal for SmartSniper
> is to make the experience for all users
> to be as interactive and hands free as possible.

We hope to make the sniping experience so automated that once you let it run, it will snipe a name without any interaction.


# Table of Contents

 - [Installation](#installation)
 - [Usage](#usage)
   * [Starting the program](#starting-the-program)
   * [Choosing account type](#choosing-account-type)
     + [MS or GC](#ms-ms-or-gc-g)
     + [Mojang](#mojang-m)
   * [Choosing a mode](#choosing-a-mode)
     + [Autosniping](#autosniping)
     + [Manual](#manual)
   * [How to get a bearer token](#how-to-get-a-bearer-token)
     + [Manually](#manually)
     + [Getting your bearer token with V](#getting-your-bearer-token-with-v)
 - [NameMC Auto Claimer](#namemc-auto-claimer)
   * [Setup and Usage](#setup-and-usage)
 - [Development](#development)
 - [License](#license)
 - [Credits](#credits)


# Installation

SmartSniper requires [Python v3.8](https://www.python.org/downloads/release/python-3811/) or higher to run.
It also helps to install [Git](https://git-scm.com/download/win) for installation of SmartSniper.

Install the dependencies and start the program.

```sh
git clone https://github.com/snipesmarter/smart-sniper.git
cd smart-sniper
pip install -r requirements.txt
```
If this doesn't work at all, do this for every line in requirements.txt:
```sh
pip install <name>
(replace <name> with the name of the import)
```

You can replace the first step with just downloading the zipped file of this and extracting. You will, however, need to open CMD/*sh to the folder afterwards.

# Usage

## Starting the program

Open CMD/*sh in the folder and run this command:
```sh
python main.py
```

## Choosing account type

```sh
What account type?
Enter g for giftcard snipes
Enter m for mojang snipes
Enter ms for microsoft snipes:
(Choose your option)
```

### Microsoft (ms) or Giftcard (g)
```sh
Microsoft Account/Giftcard Selected, using Microsoft Sniper
To use Microsoft email and password enter e
To use Token enter t: (choose your option)
```
e - normal authentication with email and password
t - [Bearer Token](#how-to-get-a-bearer-token)
```sh
e
Microsoft Email: (your microsoft email)
Password: (your microsoft password)
```
```sh
t
What is your bearer token: (your token)
```

### Mojang (m) [OUTDATED](https://help.minecraft.net/hc/en-us/articles/360050865492-Minecraft-Java-Edition-Account-Migration-FAQ)
```sh
Account Email: (enter your mojang email here)
Password:   (enter your password here)
200
{clientToken: , accessToken: }
200
```
If you have security questions applied, you have to answer them

## Choosing a mode
Here, you will choose autosniper or manual sniping.

### Autosniping
```sh
What sniper mode? Enter `a` for autosniper and `n` for single name sniping: a
starting
What delay:  (enter 0 if you dont know what to do here)
{'name': 'l1c', 'dropdate': 1620408382}
delay tuned
delay is now: 0
droptime: 1620408382
```
Now you are set to autosnipe with your giftcard.

### Manual

```sh
What sniper mode? Enter `a` for autosniper and `n` for single name sniping: n
what name do you want to snipe:  (enter the name you want to snipe)
what delay do you want:  (try 250 at the start)
droptime: 1620607024 (this will vary on the name)
Response received @ 2021-05-09 17:37:04.086939 with the status 429
Response received @ 2021-05-09 17:37:04.105448 with the status 403
Response received @ 2021-05-09 17:37:04.123321 with the status 200
265 inputted delay
0:00:00.123813
['00', '123813']
changeint 23
delay: 265  tuned_delay  288
```

## How to get a bearer token

### Manually
To get your bearer token manually:
 - Sign in to your Minecraft account at minecraft.net
 - open the chrome / firefox dev tools (ctrl + shift + i) or right click and click inspect
 - Go to the "console" tab
 - paste the following code into the console:
```js
console.log(document.cookie.match(/bearer_token=([^;]+)/)?.[1] ?? 'There is no bearer token in your cookies, make sure you are on minecraft.net and that you are logged into your account.')
```
Copy the output, this is your bearer token.

[Source][bearer-info]

### Getting your bearer token with V

```
warning, if you have generated a token in the past 12 hours dont do it again your token is saved to the token txt file!, click enter to continue...
NOTE: IF YOU HAVE NOT INSTALLED THE AUTHENTICATION SERVER GO HERE  ( https://github.com/coolkidmacho/McMsAuth ), THIS WILL NOT WORK WITHOUT IT, click enter to continue
Microsoft email: (email)
Microsoft password: (password)

(your token)
```

# NameMC Auto Claimer

## Setup and Usage
If you plan to use NameMC auto-claimer, you must be using Mojang accounts. This process works on Windows and Linux.

Your first task is to unzip the file called `namemc` after doing that, follow these instructions to the T (run in CMD/*sh):

```sh
cd namemc
python setup.py install
```
This is a very important step. After completing this, edit your config.json file to have NameMC autoclaim set to `True`.

Thanks to Cypheriel#3837 for the original code, this could not be done without him. Check him out here: [GitHub](https://github.com/Cypheriel) 

# Resources


Smart Sniper utilizes public APIs and software made by me [coolkidmacho] and others.

 - Kqzz's API
   - Used to determine drop times.
   - [https://github.com/Kqzz/MC-API](https://github.com/Kqzz/MC-API)
 - PyCraft
   - Used to help auto-claim NameMC profiles.
   - [https://github.com/ammaraskar/pyCraft](https://github.com/ammaraskar/pyCraft)
 - Zodiac API
   - alternative droptime api
   - https://github.com/0yq
 - NameMC
   - used for search-based and 3char sniping
   - https://namemc.com

# Useful Programs

The programs listed here are helpful, but not required.

 - Dimension 4
   - Used to sync time with world time servers (NTP).
   - [http://www.thinkman.com/dimension4/download.htm](http://www.thinkman.com/dimension4/download.htm)

# Development

Want to contribute? Great!

Contribute to our GitHub at [https://github.com/snipesmarter/smart-sniper/](https://github.com/snipesmarter/smart-sniper/).

Here are some suggested contributions:
 - Work on issues!
   - Fix bugs, determine invalid or valid, get info.
 - Vanity edits!
   - Things like tidying the README, cleaning code, etc.

Note that you don't have to do one something from this list, it's just some ideas.

# License

SmartSniper is licensed under the GNU General Public License v3.0.

You may:
 - Commercially use this software.
   - Make sure to disclose source upon request if done.
 - Modify and redistribute.
   - Disclose modifications and keep the license the same.
 - Patent and private use.

Head to /LICENSE for full license information.

# Credits

Thanks to [coolkidmacho] for:
 - maintaining this repo
 - lots of code

Thanks to [Kqzz] for:
 - helping a lot with this project
 - code snippets from [MCsniperPY](https://github.com/MCsniperPY) for Mojang authentication

Thanks to [Cypheriel](https://github.com/Cypheriel) for:
 - NameMC automatic claim script

Thanks to [MohanadHosny] for:
 - Microsoft authentication code (specifically `msauth.py`).
   - found at https://github.com/MohanadHosny/Microsoft-Minecraft-Auth

Thanks to [chrommie] and [kenny] for:
 - `main.py` updates
   - prompt tidying

Thanks to [chrommie] for:
 - `main.py` updates
   - type declarations
  
Thanks to [peet] for:
  - NameMc scraping script
  - `main.py` tidying

Thanks to [surprise] for:
  - updated bearer grabber script
  - `main.py` tidying

Thanks to [coolkidmacho], [overestimate], [TanujKS], and [Kqzz] for:
 - this README and it's contents

Thanks to [MatrixCodeDE] for:
 - `main.py` updates
   - cross platform optimisation
   - Name Checking for auto 3 char
   - optional scraper usage
 - `scraper.py` updates
   - droptime including

Thanks to issue submitters, issue commenters, stargazers, and anyone missed here for:
 - making this project grow
 - helping to find and fix bugs

   [coolkidmacho]: <https://github.com/coolkidmacho>
   [Kqzz]: <https://github.com/Kqzz>
   [MohanadHosny]: <https://github.com/MohanadHosny>
   [chrommie]: <https://github.com/chrommie>
   [peet]: <https://github.com/wwhtrbbtt>
   [surprise]: <https://github.com/surprise>
   [overestimate]: <https://github.com/overestimate>
   [TanujKS]: <https://github.com/TanujKS>
   [kenny]: <https://github.com/cyberseckenny>
   [MCsniperPY]: <https://mcsniperpy.com/>
   [bearer-info]: <https://kqzz.github.io/mc-bearer-token/>
   [MatrixCodeDE]: <https://github.com/MatrixCodeDE>

Keywords
Minecraft Api, Minecraft Username, Python, Requests, Smart Sniper
