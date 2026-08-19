# Experiment 3: FIFO Transfer with Elevation-Angle Delay

[English](README.md) | [繁體中文](README.zh-TW.md)

This experiment sends UDP packets through a **Gateway** that forwards them in **FIFO** (first-in, first-out) order. End-to-end delay follows the **elevation angle θ**: as packet index `i` increases, θ (an integer, in degrees) decreases and propagation delay grows.

`proxy.py` applies banded delays by packet range (millisecond scale, approximating the physical formula). `proxy_new.py` amplifies the same elevation trend to 100–800 ms for easier plotting.

## Topology

![Gateway FIFO topology](../docs/assets/topo-lossy.png)

## Files

| Path | Purpose |
| --- | --- |
| `server.py`, `server.sh` | Send `Hello 1` … `Hello 100` to the Gateway; write `exp3_server.csv` |
| `client.py`, `client.sh` | Receive on port `5407`; write `exp3_client.csv` |
| `proxy.py`, `proxy.sh` | Gateway A: FIFO forward, millisecond-scale delay |
| `proxy_new.py`, `proxy_new.sh` | Gateway B: FIFO forward, amplified delay (100–800 ms) |
| `exp3_result.py` | Compare timestamps and plot delay in milliseconds |

### Elevation and delay model

Constants: $R_E = 6371$ km, $h_0 = 1200$ km, speed of light $c = 3 \times 10^5$ km/s.

Elevation for packet `Hello i` is an **integer** (degrees). Two packets share one angle; starts at 90°:

$$
\theta(i) = 90 - \left\lfloor \frac{i-1}{2} \right\rfloor
$$

Slant range:

$$
d = \sqrt{R_E^2 \sin^2\alpha + h_0^2 + 2 h_0 R_E} - R_E \sin\alpha
$$

($\alpha = \theta$.) Theoretical propagation delay: $\text{delay} = d / c$. Examples: 90° ≈ 4.00 ms, 80° ≈ 4.05 ms, 70° ≈ 4.21 ms, 60° ≈ 4.50 ms, 50° ≈ 4.96 ms, 40° ≈ 5.64 ms.

**Gateway A** — `proxy.py` (default, `bash proxy.sh`), banded delays by packet range:

| Packet i | Elevation | Delay |
| --- | --- | --- |
| 1–20 | 90° | 4.00 ms |
| 21–40 | 80° | 4.05 ms |
| 41–60 | 70° | 4.21 ms |
| 61–80 | 60° | 4.50 ms |
| 81–100 | 50° | 4.96 ms |

**Gateway B** — `proxy_new.py` (`bash proxy_new.sh`), same elevation trend with amplified delay:

| Packet i | Elevation | Delay |
| --- | --- | --- |
| 1–65 | 90° | 100 ms |
| 66–83 | 58° | 300 ms |
| 84–92 | 49° | 500 ms |
| 93–97 | 44° | 700 ms |
| 98–100 | 41° | 800 ms |

## Quick start

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv env
source ./env/bin/activate
pip3 install -r ../requirements.txt
```

- Single machine: [manual-single.md](docs/manual-single.md)
- Two machines: [manual-dual.md](docs/manual-dual.md)

## Ports

| Process | Port |
| --- | --- |
| Server | `5405` |
| Proxy (Gateway) | `5406` |
| Client | `5407` |
