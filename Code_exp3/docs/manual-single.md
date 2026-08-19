# Experiment 3 — Single-machine manual

[English](manual-single.md) | [繁體中文](manual-single.zh-TW.md)

> [!NOTE]
> Run Server, Proxy, and Client on **one** Ubuntu machine. Add a second IP on the same NIC. No AP is required.

![Single-machine idea](../../docs/assets/topo-single-concept.png)

## Idea

Packets go through a **Gateway** and leave in **FIFO** order. Delay follows the **elevation angle θ** (integer, degrees): every two packets share one angle, starting at 90° and decreasing with packet index, so slant range and propagation delay grow. Run `proxy.sh` (millisecond scale, ~4–5 ms) or `proxy_new.sh` (scaled to 100–800 ms) and compare the latency plots.

## Setup

```bash
ip a
```

Example (replace with yours):

| Role | Example |
| --- | --- |
| Server IP | `192.168.0.225` |
| NIC name | `ens33` |
| Client / Proxy IP | `192.168.0.226` |

```bash
sudo ip addr add <CLIENT_IP>/24 dev <NIC_NAME>
ping -c 3 -I <NIC_NAME> <CLIENT_IP>
ping -c 3 -I <NIC_NAME> <SERVER_IP>
```

Skip the `ip addr add` step if you already did it for Experiment 2.

## Topology

![FIFO topology](../../docs/assets/topo-lossy.png)

| Role | UDP port |
| --- | --- |
| Server (satellite) | `5405` |
| Proxy (Gateway, FIFO + elevation delay) | `5406` |
| Client (terminal) | `5407` |

Client IP and Proxy IP are the same extra address in this mode.

## Steps

Work in `Code_exp3`. Start **client**, then **proxy**, then **server**:

```bash
bash client.sh -c <CLIENT_IP>
bash proxy.sh -p <PROXY_IP> -c <CLIENT_IP>
bash server.sh -s <SERVER_IP> -p <PROXY_IP>
```

To use the other Gateway (`proxy_new.py`) instead of `proxy.py`:

```bash
bash proxy_new.sh -p <PROXY_IP> -c <CLIENT_IP>
```

| Script | Gateway | Delay scale |
| --- | --- | --- |
| `proxy.sh` → `proxy.py` | Gateway A | By packet range, ~4.00–4.96 ms |
| `proxy_new.sh` → `proxy_new.py` | Gateway B | Same elevation trend, 100–800 ms |

See [README.md](../README.md) for the elevation formula and tables.

## Expected result

- Server sends `Hello 1` … `Hello 100` in order (FIFO).
- Proxy prints each packet and the corresponding delay (milliseconds).
- Client prints every received Hello. Because forwarding is FIFO, order stays sequential; the delay curve rises as elevation falls.

## Logs and plot

CSV files are written in `Code_exp3` (`exp3_server.csv`, `exp3_client.csv`). Then:

```bash
pip3 install matplotlib
python3 exp3_result.py
```

The script prints delay in **milliseconds**, writes `exp3_result.csv`, and saves `exp3_result.png` (x: packet index, y: delay in ms). Repeating the run with `proxy_new.sh` should show a much clearer rising trend.

![Sample EXP_3 plot](../../docs/assets/exp3-result.png)

![Sample EXP_3 plot, zoomed](../../docs/assets/exp3-result-zoom.png)

## Demo

[Single-machine FIFO demo](https://youtu.be/H_3eXnDWkdg)
