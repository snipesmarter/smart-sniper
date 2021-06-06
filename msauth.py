from re import search
from typing import NamedTuple, Union

import requests
from requests import Response
from requests import Session

AUTHORIZE = "https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"
XBL = "https://user.auth.xboxlive.com/user/authenticate"
XSTS = "https://xsts.auth.xboxlive.com/xsts/authorize"

userAgent = "Mozilla/5.0 (XboxReplay; XboxLiveAuth/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

login_with_xbox = "https://api.minecraftservices.com/authentication/login_with_xbox"
ownership = "https://api.minecraftservices.com/entitlements/mcstore"
profile = "https://api.minecraftservices.com/minecraft/profile"


class PreAuthResponse(NamedTuple):
    response: Response
    url_post: str
    ppft: str


class UserLoginResponse(NamedTuple):
    refresh_token: str
    access_token: str
    expires_in: int
    loggedin: bool = False


class XBLAuthenticateResponse(NamedTuple):
    user_hash: str
    token: str


class XSTSAuthenticateResponse(NamedTuple):
    user_hash: str
    token: str


class UserProfile(NamedTuple):
    username: Union[str, None]
    uuid: Union[str, None]


class Microsoft:
    def __init__(self, client: Session = None) -> None:
        self.client = client if client is not None else Session()

    def xbl_authenticate(self, login_resp: UserLoginResponse) -> XBLAuthenticateResponse:
        headers = {
            "User-Agent": userAgent,
            "Accept": "application/json",
            "x-xbl-contract-version": "0"
        }

        payload = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": login_resp.access_token,
            }
        }

        resp = self.client.post(XBL, json=payload, headers=headers)

        if resp.status_code != 200:
            raise Exception("XBL Authentication failed")

        data = resp.json()

        return XBLAuthenticateResponse(
            token=data["Token"],
            user_hash=data["DisplayClaims"]["xui"][0]["uhs"]
        )

    def xsts_authenticate(self, xbl_resp: XBLAuthenticateResponse) -> XSTSAuthenticateResponse:
        headers = {
            "User-Agent": userAgent,
            "Accept": "application/json",
            "x-xbl-contract-version": "1"
        }

        payload = {
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT",
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [
                    xbl_resp.token
                ]
            }
        }

        resp = self.client.post(XSTS, json=payload, headers=headers)

        if resp.status_code != 200:
            if resp.status_code == 401:
                json = resp.json()
                if json["XErr"] == "2148916233":
                    raise Exception("This account doesn't have an Xbox account")
                elif json["XErr"] == "2148916238":
                    raise Exception("The account is a child (under 18)")
                else:
                    raise Exception(f"Unknown XSTS error code: {json['XErr']}")
            else:
                raise Exception("XSTS Authentication failed")

        data = resp.json()

        return XSTSAuthenticateResponse(
            token=data["Token"],
            user_hash=data["DisplayClaims"]["xui"][0]["uhs"]
        )

    def login_with_xbox(self, token: str, user_hash: str) -> str:
        headers = {
            "Accept": "application/json",
            "User-Agent": userAgent
        }

        payload = {"identityToken": f"XBL3.0 x={user_hash};{token}"}

        resp = self.client.post(login_with_xbox, json=payload, headers=headers)

        if "access_token" not in resp.text:
            raise Exception("LoginWithXbox Authentication failed")

        return resp.json()["access_token"]

    def user_hash_game(self, access_token: str) -> bool:
        headers = {
            "Accept": "application/json",
            "User-Agent": userAgent,
            "Authorization": f"Bearer {access_token}"
        }

        resp = self.client.get(ownership, headers=headers)

        return len(resp.json()["items"]) > 0

    def get_user_profile(self, access_token: str) -> UserProfile:
        headers = {
            "Accept": "application/json",
            "User-Agent": userAgent,
            "Authorization": f"Bearer {access_token}"
        }

        resp = self.client.get(profile, headers=headers).json()

        return UserProfile(
            username=resp.get("name"),
            uuid=resp.get("id")
        )


class XboxLive:
    def __init__(self, client: requests.Session = None) -> None:
        self.client = client if client is not None else requests.Session()

    def pre_auth(self) -> PreAuthResponse:
        resp = self.client.get(AUTHORIZE, headers={"User-Agent": userAgent}, allow_redirects=True)

        ppft = search(r"value=\"(.*?)\"", search(r"sFTTag:'(.*?)'", resp.text).group(1)).group(1)
        urlPost = search(r"urlPost:'(.+?(?=\'))", resp.text).group(1)

        if urlPost is None or ppft is None:
            raise Exception("Failed to extract PPFT or urlPost")

        return PreAuthResponse(
            response=resp,
            ppft=ppft,
            url_post=urlPost
        )

    def user_login(self, email: str, password: str, preauth: PreAuthResponse) -> UserLoginResponse:
        postData = f"login={self.encode(email)}&loginfmt={self.encode(email)}&passwd={self.encode(password)}&PPFT={preauth.ppft}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": userAgent
        }

        resp = self.client.post(url=preauth.url_post, data=postData, cookies=preauth.response.cookies, headers=headers,
                                allow_redirects=True)

        if "access_token" not in resp.url and resp.url == preauth.url_post:
            if "Sign in to" in resp.text:
                raise Exception("Invalid credentials.")
            elif "Help us protect your account" in resp.text:
                raise Exception("2FA is enabled but not supported yet!")
            else:
                raise Exception(f"Something went wrong. Status Code: {resp.status_code}")

        data = resp.url.split("#")[1].split("&")

        return UserLoginResponse(
            refresh_token=data[4].split("=")[1],
            access_token=data[0].split("=")[1],
            expires_in=int(data[2].split("=")[1]),
            loggedin=True
        )

    def encode(self, data: str) -> str:
        return requests.utils.quote(data)


def login(email: str, password: str) -> Union[dict, str]:
    client = Session()

    xbx = XboxLive(client)
    mic = Microsoft(client)

    login = xbx.user_login(email, password, xbx.pre_auth())

    xbl = mic.xbl_authenticate(login)
    xsts = mic.xsts_authenticate(xbl)

    access_token = mic.login_with_xbox(xsts.token, xsts.user_hash)
    hasGame = mic.user_hash_game(access_token)

    if hasGame:
        profile = mic.get_user_profile(access_token)
        data = {
            "access_token": access_token,
            "username": profile.username,
            "uuid": profile.uuid
        }

        return data
    else:
        return "Not a premium account"

# credits to https://github.com/MohanadHosny/Microsoft-Minecraft-Auth for the original code, this is all thanks to him!
