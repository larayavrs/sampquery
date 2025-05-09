import asyncio
from pysampquery import PySAMPQuery_Client


async def main():
    latam = PySAMPQuery_Client("154.38.184.18", 7777)

    server_info = await latam.info()
    print(f"Server name: {server_info.name}")

    players_list = await latam.players()
    print(f"Players:")

    for player in players_list.players:
        print(f"> {player.name}")


asyncio.run(main())
