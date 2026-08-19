# LEO Satellite Network UDP Experiments

[English](README.md) | [繁體中文](README.zh-TW.md)

UDP-based lab experiments that emulate satellite-to-terminal data transfer: lossless vs. lossy links, and FIFO forwarding with elevation-angle-dependent delay.

## Overview

Each experiment uses UDP sockets to play the roles of a satellite, an optional gateway, and a ground terminal:

![Gateway topology](docs/assets/topo-lossy.png)

| Role | Role in the lab | UDP port |
| --- | --- | --- |
| Server | Satellite sender | `5405` |
| Proxy | Gateway (delay / loss / FIFO) | `5406` |
| Client | Ground terminal receiver | `5407` |

Experiment 2-1 (lossless) skips the proxy and sends Server → Client directly.

## Features

- Lossless UDP transfer over a wired path, observed with Wireshark I/O graphs
- Lossy transfer through a proxy that injects delay and packet loss
- FIFO forwarding at a gateway; delay rises as elevation angle decreases
- Single-machine mode (extra IP on one NIC) and two-machine mode (Ethernet hub or Wi-Fi AP)
- CSV logs plus `matplotlib` latency plots for the proxy-based experiments

## Repository structure

```text
.
├── Code_exp2/          # Lossless and lossy UDP transfer
│   ├── EXP_1/          # Server → Client (no proxy)
│   ├── EXP_2/          # Server → Proxy → Client
│   └── docs/           # Single-machine and two-machine manuals
├── Code_exp3/          # FIFO transfer with elevation-angle delay
│   └── docs/
├── docs/assets/        # Topology photos and sample plots
├── LICENSE
└── requirements.txt
```

## Requirements

- Ubuntu 22.04 (or a similar Linux distribution)
- Python 3
- [matplotlib](https://matplotlib.org/) for latency plots (`pip install -r requirements.txt`)
- Wireshark (optional, for packet capture and I/O graphs)
- OpenSSH server/client (optional, two-machine remote control)

## Quick start

Pick an experiment, then follow the matching manual.

| Experiment | Goal | Single machine | Two machines |
| --- | --- | --- | --- |
| [Code_exp2](Code_exp2/README.md) EXP_1 | Lossless UDP | [Manual](Code_exp2/docs/manual-single.md#experiment-1-lossless-data-transmission) | [Manual](Code_exp2/docs/manual-dual.md#experiment-1-lossless-data-transmission) |
| [Code_exp2](Code_exp2/README.md) EXP_2 | Lossy UDP via proxy | [Manual](Code_exp2/docs/manual-single.md#experiment-2-lossy-data-transmission) | [Manual](Code_exp2/docs/manual-dual.md#experiment-2-lossy-data-transmission) |
| [Code_exp3](Code_exp3/README.md) | FIFO + elevation delay | [Manual](Code_exp3/docs/manual-single.md) | [Manual](Code_exp3/docs/manual-dual.md) |

Minimal example (Experiment 2-1 on one machine, after adding a second IP):

```bash
cd Code_exp2/EXP_1
bash client.sh -c <CLIENT_IP>
bash server.sh -s <SERVER_IP> -c <CLIENT_IP>
```

Replace the addresses with your own. Default send interval is 1 second (`-t`).

## Documentation

- [Experiment 2 README](Code_exp2/README.md) · [中文](Code_exp2/README.zh-TW.md)
- [Experiment 3 README](Code_exp3/README.md) · [中文](Code_exp3/README.zh-TW.md)

## Demo videos

YouTube recordings for each experiment's steps and sample results are linked from the matching experiment manual.

## Contributing

Issues and pull requests are welcome. Please describe the experiment (`Code_exp2` / `Code_exp3`), whether you used single-machine or two-machine mode, and the commands you ran.

## Acknowledgements

We thank Senior Sister 詩涵, Senior Brother 應詰, and Senior Brother 名初, as well as the senior members of WISE Lab for their contributions to developing this educational material.

## License

This project is licensed under the [MIT License](LICENSE).
