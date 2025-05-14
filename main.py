"""Official interactive interface menu for SAMPQuery Client"""

import os
import trio
import sys
import re
import time
import colorist as color

from ctypes import windll
from sampquery import SAMPQuery_Client
from sampquery.utils import SAMPQuery_Constants

def console_title(title: str) -> None:
    """
    Set the title of the console window to the given string
    
    :param title: The title to set
    """
    windll.kernel32.SetConsoleTitleW(title)
    
def show_commands():
    """
    Display the list of available commands to the user.

    The commands are retrieved from the SAMPQuery_Constants.MENU_COMMANDS 
    and printed in a formatted manner for easy reading.
    """
    print("Available commands:")
    for command in SAMPQuery_Constants.MENU_COMMANDS:
        print(f"- {command}", end="\n")

async def menu(client: SAMPQuery_Client, ip: str, port: int) -> None:
    """
    This function is the main interactive menu of the program. It sets the window title to the server name and port, and then enters a loop where it continually prompts the user for a command and executes it.

    :param client: The SAMPQuery_Client object to use for querying the server
    :param ip: The IP address of the server
    :param port: The port number of the server
    """
    try:
        info = await client.info()
        console_title(f"SAMP Query Client - {info.name} ({ip}:{port})")
    except Exception:
        console_title(f"SAMP Query Client - {ip}:{port}")
    os.system("cls")
    color.green("Connected successfully to the server!")
    show_commands()
    while True:
        command  = input("> ").strip()
        if command == "exit":
            color.red("Thanks for using SAMPQuery Client! Goodbye.")
            time.sleep(3)
            sys.exit(0)
        elif command == "help":
            show_commands()
        elif command == "players":
            try:
                players_list = await client.players()
                for player in players_list.players:
                    print(f"* {player.name} | Score: {player.score}")
            except Exception as e:
                color.red(f"Error getting player list: {e}")
        elif command == "info":
            try:
                info = await client.info()
                print(f"* {info.name} | Players: {info.players}/{info.max_players}")
                print(f"* Gamemode: {info.gamemode} | Language: {info.language}")
            except Exception as e:
                color.red(f"Error getting server info: {e}")
        elif command == "rules":
            try:
                rules = await client.rules()
                for rule in rules.rules:
                    color.bg_bright_green(f"* {rule.name}: {rule.value}")
            except Exception as e:
                color.red(f"Error getting server rules: {e}")
        elif command == "lagcomp":
            try:
                lagcompmode = await client.lagcomp()
                color.bg_bright_green(f"The server is: {lagcompmode}")
            except ValueError as e:
                color.red(f"Error determining shot type: {e}")
        else:
            color.red("Invalid command. Use 'help' to see available commands.")

        await trio.sleep(0.1)

async def main():
    """
    This is the main function of the program. It takes in a command line argument 
    in the format of --connect <ip:port> and attempts to connect to the server at
    that IP and port. If the connection fails or the wrong arguments are given, it
    will print an error and exit. If the connection is successful, it will enter an
    interactive menu where the user can execute commands to query the server.

    :return None:
    """
    ip = None
    port = None
    if len(sys.argv) == 3 and sys.argv[1] == "--connect":
        match = re.match(r"^([\d\.]+):(\d+)$", sys.argv[2])
        if not match:
            color.red("You have to use the format --connect <ip:port>")
            sys.exit(1)
        ip, port = match.group(1), int(match.group(2))
    elif len(sys.argv) == 1:
        # if no arguments are given then we prompt the user for the IP and port
        ip = input("Enter the IP address to connect: ").strip()
        port_input = input("Enter the server port: ").strip()
        if not re.match(r"^\d{1,5}$", port_input):
            color.red("Invalid port format. Closing the program...")
            time.sleep(3)
            sys.exit(1)
        port = int(port_input)
        if not re.match(r"^([\d\.]+)$", ip):
            color.red("Whoops! You have to use the correct format: --connect <ip:port>")
            sys.exit(1)
    else:
        color.red("You are missing arguments. Use sampquery --connect <ip:port>")
        sys.exit(1)
    client = SAMPQuery_Client(ip, port)
    try:
        await client.info()
    except Exception as e:
        color.red(f"Error connecting to the server: {e}")
        time.sleep(3)
        sys.exit(1)
    await menu(client, ip, port)

if __name__ == "__main__":
    trio.run(main)