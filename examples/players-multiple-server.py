import trio

from sampquery import SAMPQuery_Client

async def main() -> None:

    # Now we can query multiple servers like this
    servers = [
        SAMPQuery_Client(ip="34.231.191.151", port=7777),
        SAMPQuery_Client(ip="144.217.174.214", port=6969)
    ]

    # Get the results of the queries
    results = await SAMPQuery_Client.players_multi_servers(servers)

    # Which will look like this
    for result in results:
        print(result)

trio.run(main)