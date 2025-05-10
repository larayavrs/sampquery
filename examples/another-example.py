import trio
from sampquery import SAMPQuery_Client

async def main():
    mxf = SAMPQuery_Client(
        ip="144.217.174.214",
        port=8888
    )

    server_info = await mxf.info()

    print(f"{server_info.name} | ({server_info.players}/{server_info.max_players})")

    player_list = await mxf.players()

    print("Players:")
    for player in player_list.players:
        print(f"{player.name} | {player.score}")

    rule_list = await mxf.rules()

    print("Rules:")
    for rule in rule_list.rules:
        print(f"{rule.name} | {rule.value}")
    
    print(f"Is password protected: {server_info.password}")
    print(f"Encodings: {server_info.encodings}")

if __name__ == "__main__":
    trio.run(main)