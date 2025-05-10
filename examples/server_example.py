import trio
from sampquery import SAMPQuery_Client

async def main():
    """
    Connects to a SA:MP server, retrieves and displays server details, 
    the list of players with their scores, and server rules.

    This coroutine establishes a connection using the SAMPQuery_Client 
    with the specified IP and port. It fetches server information, 
    player list, and server rules asynchronously and prints the results 
    to the console.
    """
    server = SAMPQuery_Client(ip="54.37.142.75", port=7777)
    details = await server.info()
    player_list = await server.players()
    rules_list = await server.rules()
    print(f"Players online in {details.name}: ({details.players} / {details.max_players})")
    for player in player_list.players:
        print(player.name, player.score)
    print("Rules:")
    for rule in rules_list.rules:
        print(rule.name, rule.value)

trio.run(main)