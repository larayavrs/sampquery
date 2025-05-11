### sampquery
Better, flexible, re-written and fast SA:MP/OMP query server client

<div align="left">
    <img src="https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=white"/>
    <img src="https://img.shields.io/badge/Windows-000000?style=for-the-badge&logo=windows&logoColor=ffffff"/>
    <img src="https://img.shields.io/badge/version-0.0.6-black?style=for-the-badge"/>
</div>

<hr />

### Introduction
SA:MP Query it is developed to interact with GTA SA:MP/OpenMP servers, allowing to obtain <br/>
important data through mechanisms based on a UDP packet system provided by SA:MP.

> [!NOTE]  
> Learn more about [SA:MP Query Mechanisms](https://sampwiki.blast.hk/wiki/Query_Mechanism)

### Installation
```bash
pip install py-sampquery
```

### Usage
```python
import trio
import sampquery as sampq

async def main() -> None:
  server = sampq.SAMPQuery_Client(
    ip='144.217.174.214',
    port=6969
  )
    
  # Getting server information
  server_info = await server.info()
  print(f"Retrieving server data of {server_info.name)
    
  # Players inside
  player_list = await server.players()
  for player in player_list.players:
    print(f"Nickname: {player.name} (Score: {player.score})")

if __name__ == "__main__":
    trio.run(main)
```

> Wanna see some examples? you can check [this](./examples/) examples folders.

### Contributions
We're open to receiving contributions and improvements for the following enhancements. Feel free to open an [issue](https://github.com/larayavrs/sampquery/issues) or [create a pull request](https://github.com/larayavrs/sampquery/pulls).
