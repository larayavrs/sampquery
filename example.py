from trio import run
from sampquery import SAMPQuery_Client

async def main():
    latam = SAMPQuery_Client(
        ip='144.217.174.214',
        port=6969,
        rcon_password=None
    )
    server_info = await latam.info()
    print(f"Server name: {server_info.name}")
    players_list = await latam.players()
    for player in players_list.players:
        print(f"> {player.name}")

run(main)
