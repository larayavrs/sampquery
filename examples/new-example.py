"""In this example, we will retrieve server information, lagcomp-mode, player list, and server rules."""

import trio
import sampquery as sampq

async def main() -> None:
    server = sampq.SAMPQuery_Client(
        ip='144.217.174.214',
        port=6969
    )

    server_info = await server.info()
    print(f"Retrieving server data of {server_info.name}")
    print(f"Players online: {server_info.players} / Max players slots: {server_info.max_players}")
    
    server_rules = await server.rules()
    print("Rules:")
    for rule in server_rules.rules:
        print(f"* {rule.name}: {rule.value}")
    
    try:
        lagcompmode = await server.lagcomp()
        print(f"The server is: {lagcompmode}.")
    except ValueError as e:
        print(f"Error determining shot type: {e}")

if __name__ == '__main__':
    trio.run(main)