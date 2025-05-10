import trio
from sampquery import SAMPQuery_Client

async def main():
    mxf = SAMPQuery_Client(ip="144.217.174.214", port=8888)
    server_info = await mxf.info()
    print(f"{server_info.name} | ({server_info.players}/{server_info.max_players})")
    detailed_player_list = await mxf.detailed_players()
    print("Printing detailed player list:")
    for player in detailed_player_list.players:
        print(f"id: {player.player_id} | {player.name} (score: {player.score}, {player.ping}ms)")

if __name__ == "__main__":
    trio.run(main)