from lib2to3.pgen2 import driver
import socket
import ssl
import certifi
import os
import json

import h2.connection
import h2.settings
import h2.events

from colorama import Fore, Style, init

if os.name == "nt":
    init(convert=True, autoreset=True)
else:
    init(convert=False, autoreset=True)

# Scraping module
from bs4 import BeautifulSoup
from datetime import datetime as ddt
import dateutil.parser

DEBUG = False
SERVER_NAME = "namemc.com"
SERVER_PORT = 443


def get_ssl_connection(name: str, port: int = 443) -> ssl.SSLSocket:
    # generic socket and ssl configuration
    socket.setdefaulttimeout(15)
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.set_alpn_protocols(["h2"])

    # open a socket to the server and initiate TLS/SSL
    s = socket.create_connection((SERVER_NAME, SERVER_PORT))
    s = ctx.wrap_socket(s, server_hostname=SERVER_NAME)
    return s


def send_http2_preamble(sock: ssl.SSLSocket):
    sock.send(b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n")


def update_settings(conn: h2.connection.H2Connection, sock: ssl.SSLSocket) -> None:
    conn.update_settings(
        {
            h2.settings.SettingCodes.MAX_CONCURRENT_STREAMS: 65536,
            h2.settings.SettingCodes.INITIAL_WINDOW_SIZE: 65535,
        }
    )

    sock.sendall(conn.data_to_send())


def send_prio_frames(conn: h2.connection.H2Connection, sock: ssl.SSLSocket) -> None:
    conn.prioritize(3, 201, 0, False)
    conn.prioritize(5, 101, 0, False)
    conn.prioritize(7, 1, 0, False)
    conn.prioritize(9, 7, 0, False)
    conn.prioritize(11, 1, 3, False)

    sock.sendall(conn.data_to_send())


def send_headers(conn: h2.connection.H2Connection, sock: ssl.SSLSocket, path) -> None:
    headers = [
        (":method", "GET"),
        (":path", f"/{path}"),
        (":scheme", "https"),
        (":authority", SERVER_NAME),
        ("accept", "*/*"),
        ("user-agent", "ThisIsntImportant"),
    ]
    conn.send_headers(1, headers, end_stream=True)
    sock.sendall(conn.data_to_send())


def receive_data(conn: h2.connection.H2Connection, sock: ssl.SSLSocket) -> str:
    body = b""
    response_stream_ended = False
    while not response_stream_ended:
        # read raw data from the socket
        data = sock.recv(65536 * 1024)
        if not data:
            break

        # feed raw data into h2, and process resulting events
        events = c.receive_data(data)
        for event in events:
            if DEBUG:
                print(event)
            if isinstance(event, h2.events.DataReceived):
                # update flow control so the server doesn't starve us
                conn.acknowledge_received_data(
                    event.flow_controlled_length, event.stream_id
                )
                # more response body data received
                body += event.data
            if isinstance(event, h2.events.StreamEnded):
                # response body completed, let's exit the loop
                response_stream_ended = True
                break
        # send any pending data to the server
        sock.sendall(conn.data_to_send())
    return body.decode()


def get_data(path):
    global s
    s = get_ssl_connection(SERVER_NAME, SERVER_PORT)
    global c
    c = h2.connection.H2Connection()

    # send data to look like a valid client
    send_http2_preamble(s)
    update_settings(c, s)
    send_prio_frames(c, s)
    send_headers(c, s, path)

    # receive data from the server
    body = receive_data(c, s)
    # print(body)

    # close the h2 connection
    c.close_connection()
    s.sendall(c.data_to_send())

    # close the socket
    s.close()
    return body


def getNameInfo(username):
    print(username, "data received")
    # general data
    data = get_data(f"search?q={str(username)}")
    soup = BeautifulSoup(data, "html.parser")
    # drop time
    try:
        dropTime = soup.find(id="availability-time")
        dropp = dropTime["datetime"]
        dropp = dateutil.parser.parse(dropp).timestamp()
    except:
        dropp = None
    # searches
    searches = int(
        soup.find_all("div", class_="tabular")[0].text.replace(" / month", "")
    )
    # Capitals
    capitals = soup.find_all("samp")[0].text
    try:
        ret = {"searches": searches, "droptime": int(dropp), "spelling": capitals}
    except:
        ret = {"searches": searches, "droptime": dropp, "spelling": capitals}
    return ret


def getNameHistory(searches=None, length=None):
    print(searches, length)
    # general data
    if searches == None:
        searches = "&"
    if length == None:
        length = "&"
    data = get_data(
        f"minecraft-names?searches={str(searches)}&length_op=eq&length={str(length)}"
    )
    data = str(data)
    with open("main.html", "w", encoding="utf-8") as f:
        f.write(data)
    soup = BeautifulSoup(data, "html.parser")
    names = []

    # names.append(soup.select_one("div.px-3:nth-child(1)"))
    names.extend(soup.find_all("td", class_="text-left"))
    # print(names)
    rel = soup.select("[rel='next']")
    nl = []
    for name in names:
        try:
            username = name.find("a").text
            # print(username)
            nl.append(username)
        except:
            pass

    return nl


def getNameDrops(searches=None, length=None):
    #print(searches, length)
    # general data
    if searches == None:
        searches = "&"
    if length == None:
        length = "&"
    if length == "&" or length == 0:
        data = get_data(
            f"minecraft-names?searches={str(searches)}"
        )
    elif searches == "&" or searches == 0:
        data = get_data(
            f"minecraft-names?length_op=eq&length={str(length)}"
        )
    else:
        data = get_data(
            f"minecraft-names?searches={str(searches)}&length_op=eq&length={str(length)}"
        )
    data = str(data)
    #with open("main.html", "w", encoding="utf-8") as f:
        #f.write(data)
    soup = BeautifulSoup(data, "html.parser")
    names = []
    drops = []
    #print(soup)
    # names.append(soup.select_one("div.px-3:nth-child(1)"))
    names.extend(soup.find_all("td", class_="text-left"))
    drops.extend(soup.find_all("td", class_="text-left text-nowrap text-ellipsis border-top-0"))
    # print(names)
    # print(drops)
    rel = soup.select("[rel='next']")
    pnl = []
    for name in names:
        try:
            username = name.find("a").text
            # print(username)
            pnl.append(username)
        except:
            pass
    nl = [[0 for x in range(2)] for y in range(len(pnl))]
    for x in range(len(pnl)):
        nl[x][0] = pnl[x]
    x = 0
    for drop in drops:
        try:
            droptime = dateutil.parser.parse(drop.text).timestamp()
            nl[x][1] = droptime
            x = x + 1
        except:
            #print("pass")
            pass
    # print(nl)
    if len(nl) == 0:
        print(f"{Fore.RED}No Names found!")
        return None
    else:
        ret = jsonBuilder(nl)
        return ret

def jsonBuilder(input):
    structure = None
    for x in range(len(input)):
        if x == 0:
            structure = '{"name":"' + str(input[x][0]) + '","droptime":' + str(input[x][1]) + '},'
        elif x != len(input)-1:
            structure = structure + '{"name":"' + str(input[x][0]) + '","droptime":' + str(input[x][1]) + '},'
        else:
            structure = structure + '{"name":"' + str(input[x][0]) + '","droptime":' + str(input[x][1]) + '}'
    structure = '[' + structure + ']'
    jstruct = json.loads(structure)
    return jstruct

