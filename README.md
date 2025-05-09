<div align="center">
    <h3>SA:MP Query</h3>
    <i>a better and fixed SA:MP Query Client written in Python</i>
</div>

<hr>

### Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)

### Installation
You can install the package using:

```bash
pip install py-sampquery
```

### Usage

```python
from trio import run
from sampquery import SAMPQuery_Client

async def main():
    server = SAMPQuery_Client(
        ip='127.0.0.1',
        port=7777,
        rcon_password=None
    )

    server_details = await server.info()
    print(f"Server name: {server_details.name}, Gamemode: {server_details.gamemode}")

run(main)
```

### Examples
Here you can find a collection of some examples

#### Listing players in a server

```python
from trio import run
from sampquery import SAMPQuery_Client

async def main():
    server = SAMPQuery_Client(
        ip='144.217.174.214',
        port=6969,
        rcon_password=None
    )

    players = await server.players()

    for player in players.players:
        print(player.name)

run(main)
```

#### Getting server details

```python
from trio import run
from sampquery import SAMPQuery_Client

async def main():
    server = SAMPQuery_Client(
        ip='144.217.174.214',
        port=6969,
        rcon_password=None
    )

    server_details = await server.info()

    print(f"Server name: {server_details.name}, Gamemode: {server_details.gamemode}, Players: {server_details.players}")

run(main)
```

Thanks for using SA:MP Query, you can report any issues or suggestions [here](https://github.com/larayavrs/sampquery/issues)