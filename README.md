# Smart Sniper

# JOIN THE DISCORD FOR LIVE UPDATES, POLLS AND SUPPORT https://discord.gg/KweaD6G97f

## The most adaptive sniper in the industry 

Smartsniper is a high tech adaptive sniper. This sniper's autosniping and automatic delay tuning assists in helping you obtain the best username possible!

## Features

- Autosniping 3 Letters.
- Auto Delay Tuning.
- Gift Card Sniping.
- Intuitive Gui.
- Normal Sniping!
- Automatic Microsoft auth soon!

Made By expert snipers!

Credits to [Kqzz] who made [McSniperPY]

> The overriding design goal for smart sniper
> is to make the experience for all users
> to be as interactive and hands free as possible.

We hope to make the sniping experience so automated that once you let it run it will snipe a name without any interaction
# Warning this is a very first release, there are bugs we need to squash.
## Installation

SmartSniper requires [Python](https://www.python.org/) v3.8 to run.
It also helps to install [Git Bash](https://git-scm.com/download/win)

Install the dependencies and start the program.

```sh
git clone https://github.com/snipesmarter/smart-sniper.git
cd smart-sniper
pip install -r requirements.txt
```
You can replace the first step with just downloading the ziped file of this.

# Usage

## AutoSniping

Open command prompt in the folder and run this command!
```sh
python main.py
```
#### Interacting with the program.

```sh
What account type? Enter `g` for giftcard and `m` for mojang and `ms` for microsoft accounts: (choose your account)
```
### If you choose ms or gc you will be faced with this menu
```sh
What is your bearer token:  (look at the section below if you dont know what this means, or how to get it!)
```
#### If you choose mojang you will be faced with this menu
```sh
selected mojang account, transferring to mojang sniper.
Account Email: (enter your mojang email here)
Password:   (enter your password here)
200
{clientToken: , accessToken: }
200
```
Then you will both be directed to this menu
```sh
What sniper mode? Enter `a` for autosniper and `n` for single name sniping: a
starting
What delay:  (enter 0 if you dont know what to do here)
{'name': 'l1c', 'dropdate': 1620408382}
delay tuned
delay is now: 0
droptime: 1620408382
```
Now you are set to autosnipe with your giftcard

## How to get your bearer token?
To get your bearer token 
 - Sign in to your Minecraft account at minecraft.net
 - open the chrome / firefox dev tools (ctrl + shift + i) or right click and click inspect
 - Go to the "console" tab
 - paste this code into the console:
```js
console.log(document.cookie.match(/bearer_token=([^;]+)/)?.[1] ?? 'There is no bearer token in your cookies, make sure you are on minecraft.net and that you are logged into your account.')
```
Now you have your bearer token!

Information from: https://kqzz.github.io/mc-bearer-token/ and danktrain#0001

# Normal Sniping

```sh
What account type? Enter `g` for giftcard and `m` for mojang and `ms` for microsoft accounts: (choose your account)
```
### If you choose ms or gc you will be faced with this menu
```sh
What is your bearer token:  (look at the section below if you dont know what this means, or how to get it!)
```
#### If you choose mojang you will be faced with this menu
```sh
selected mojang account, transferring to mojang sniper.
Account Email: (enter your mojang email here)
Password:   (enter your password here)
200
{clientToken: , accessToken: }
200
```
Then you will both be directed to this menu
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

## Resources

Smart Sniper utilizes public api's made by me and others.

| Plugin | LINK | REASON |
| ------ | ------ | ------ |
| 3USER | [https://api.3user.xyz/list](https://api.3user.xyz/list) | Public Api to check upcoming 3 letter names!
| Kqzz's Api | [https://github.com/Kqzz/MC-API](https://github.com/Kqzz/MC-API) | To check droptimes for snipes.
| Dimension4 | [http://www.thinkman.com/dimension4/download.htm](http://www.thinkman.com/dimension4/download.htm) | To sync time with world servers.


## Development

Want to contribute? Great!

Contribute to our github at [https://github.com/snipesmarter/smart-sniper/](https://github.com/snipesmarter/smart-sniper/)


## License

GNU General Public License v3.0



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Kqzz]: <https://github.com/Kqzz>
   [McSniperPy]: <https://mcsniperpy.com/>

#### Credits

Thanks to kqzz for like helping alot for this project.
Thanks to kqzz's mcsniperpy project for code snippets in mojang auth!

# Made by Coolkidmacho#7567
