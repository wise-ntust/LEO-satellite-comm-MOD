# Experiment 2: Lossless and Lossy UDP Transfer

[English](README.md) | [繁體中文](README.zh-TW.md)

This folder simulates satellite-style UDP delivery.

1. **EXP_1** — lossless transfer (wired path, no proxy)
2. **EXP_2** — lossy transfer (proxy injects delay and packet loss)

## Topology

Lossless (EXP_1):

![Lossless topology](../docs/assets/topo-lossless.png)

Lossy (EXP_2):

![Lossy topology](../docs/assets/topo-lossy.png)

## Files

| Path | Purpose |
| --- | --- |
| `EXP_1/server.py`, `EXP_1/server.sh` | Send `Hello 1` … `Hello 100` to the client |
| `EXP_1/client.py`, `EXP_1/client.sh` | Bind port `5407` and print received messages |
| `EXP_2/server.py`, `EXP_2/server.sh` | Send to the proxy; write `exp2_server.csv` |
| `EXP_2/proxy.py`, `EXP_2/proxy.sh` | Delay (`-t`) and loss (`-l`) before forwarding |
| `EXP_2/client.py`, `EXP_2/client.sh` | Receive and write `exp2_client.csv` |
| `EXP_2/exp2_result.py` | Compare timestamps, plot latency / loss |

## Quick start

Install Python 3 and the virtual environment package, then create and activate a virtual environment `env`. Install dependencies inside the virtual environment:

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv env
source ./env/bin/activate
pip3 install -r ../requirements.txt
```

Then follow a full manual:

- Single machine (extra IP on one NIC): [manual-single.md](docs/manual-single.md)
- Two machines: [manual-dual.md](docs/manual-dual.md)

## Ports

| Process | Port |
| --- | --- |
| Server | `5405` |
| Proxy (EXP_2 only) | `5406` |
| Client | `5407` |
