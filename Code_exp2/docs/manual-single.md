# Experiment 2 — Single-machine manual

[English](manual-single.md) | [繁體中文](manual-single.zh-TW.md)

> [!NOTE]
> Run Server, Proxy, and Client as separate terminals on **one** Ubuntu machine. Add a second IP on the same NIC so the two roles have different addresses. No Wi-Fi AP is required.

![Single-machine idea](../../docs/assets/topo-single-concept.png)

## Wireshark (optional)

Install Wireshark via apt (Ubuntu/Debian), then reconfigure it to allow packet capture without root.

```bash
sudo apt install wireshark
sudo dpkg-reconfigure wireshark-common
```

When asked whether non-superusers may capture packets, choose **Yes**. Then add your user to the `wireshark` group and apply it immediately with `newgrp` (otherwise log out and back in):

```bash
sudo usermod -aG wireshark $USER
newgrp wireshark
wireshark
```

Capture on `Loopback: lo` (or the NIC you used for the extra IP). I/O graphs: **Statistics → I/O Graphs**.
## Shared setup

### 1. Read the host IP and NIC name

```bash
ip a
```

`ifconfig` also works if `net-tools` is installed.

Example (replace with yours):

| Role | Example |
| --- | --- |
| Server IP | `192.168.0.225` |
| NIC name | `ens33` |
| Client / Proxy IP | `192.168.0.226` |

### 2. Add a second IP for Client (and Proxy)

```bash
sudo ip addr add <CLIENT_IP>/24 dev <NIC_NAME>
```

Check with `ip a`, then:

```bash
ping -c 3 -I <NIC_NAME> <CLIENT_IP>
ping -c 3 -I <NIC_NAME> <SERVER_IP>
```

> [!TIP]
> The extra address is not persistent across reboot unless you add it to netplan/NetworkManager.

---

## Experiment 1: Lossless data transmission

**Goal:** send 100 UDP messages with no proxy and confirm none are lost.

**Hardware:** one Linux laptop (Ubuntu 22.04).

![Lossless topology](../../docs/assets/topo-lossless.png)

### Steps

1. Complete the shared setup above.
2. Start Wireshark if you want to watch traffic.
3. In `Code_exp2/EXP_1`, start the client, then the server:

```bash
bash client.sh -c <CLIENT_IP>
bash server.sh -s <SERVER_IP> -c <CLIENT_IP>
```

Optional send interval (seconds, default `1`):

```bash
bash server.sh -s <SERVER_IP> -c <CLIENT_IP> -t 1
```

4. Wireshark display filter:

```text
udp && ip.src==<SERVER_IP> && ip.dst==<CLIENT_IP>
```

Use **Statistics → I/O Graphs** for throughput.

### Expected result

- Server prints `Hello 1` … `Hello 100` and `the latency is 1.0 s` (the sleep between sends).
- Client receives every message in order.
- I/O graph stays near zero, then jumps and holds a flat rate while the burst runs.

### Demo

[Single-machine lossless demo](https://youtu.be/-hyNTx92kDg)

---

## Experiment 2: Lossy data transmission

**Goal:** insert a proxy that delays and randomly drops packets, simulating the lossy transmission characteristics of a real-world wireless satellite link to make the experiment results closer to reality.

**Hardware:** one Linux laptop.

![Lossy topology](../../docs/assets/topo-lossy.png)

Client IP and Proxy IP are the **same** extra address in single-machine mode.

### Steps

1. Reuse the extra IP from Experiment 1 if it is still configured.
2. Open three terminals in `Code_exp2/EXP_2`. Start **client**, then **proxy**, then **server**:

```bash
bash client.sh -c <CLIENT_IP>
bash proxy.sh -p <PROXY_IP> -c <CLIENT_IP> -t <DELAY_S> -l <LOSS_RATE>
bash server.sh -s <SERVER_IP> -p <PROXY_IP>
```

- `-t`: delay in seconds (example: `1`)
- `-l`: drop probability from `0` to `1` (example: `0.2` is 20%)

Defaults if omitted: `-t 1`, `-l 0`.

### Expected result

- Server prints `Hello 1` … `Hello 100`.
- Proxy prints each packet, the configured delay, and `loss probability` with `0` (drop) or `1` (forward).
- Client prints a **subset** of Hello messages; gaps mean loss.

### Logs and plot

After the run, `exp2_server.csv` and `exp2_client.csv` appear in `EXP_2`. Then:

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv env
source ./env/bin/activate
pip3 install matplotlib
```

In a terminal, run:

```bash
python3 exp2_result.py
```

The script prints per-packet delay or `packet is loss`, writes `exp2_result.csv`, and saves `exp2_result.png` (x: packet index, y: delay in seconds; losses are gaps).

![Sample EXP_2 plot](../../docs/assets/exp2-result.png)

![Sample EXP_2 plot, zoomed](../../docs/assets/exp2-result-zoom.png)

> [!NOTE]
> Each run looks different. The scatter is mainly shaped by `-t` and `-l`.

### Demo

[Single-machine lossy demo](https://youtu.be/pFleC9UVsZ8)
