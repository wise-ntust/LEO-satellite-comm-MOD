# Experiment 2 — Two-machine manual

[English](manual-dual.md) | [繁體中文](manual-dual.zh-TW.md)

Use two Ubuntu laptops. Experiment 1 is wired through an Ethernet hub. Experiment 2 uses a Wi-Fi AP. You can run each role on its own keyboard, or SSH from the client machine into the server.

## Wireshark (optional)

Install Wireshark via apt (Ubuntu/Debian), then reconfigure it to allow packet capture without root.

```bash
sudo apt install wireshark
sudo dpkg-reconfigure wireshark-common
```

Choose **Yes** for non-superuser capture. Then add your user to the `wireshark` group and apply it immediately with `newgrp` (otherwise log out and back in):

```bash
sudo usermod -aG wireshark $USER
newgrp wireshark
wireshark
```

Pick the NIC that carries the experiment traffic, then **Statistics → I/O Graphs**.
---

## Experiment 1: Lossless data transmission

**Goal:** UDP over a simple wired path with no proxy; confirm lossless delivery.

**Hardware:**

- 2 × Linux laptops (Ubuntu 22.04)
- 1 × Ethernet hub
- 2 × Ethernet cables

![Lossless topology](../../docs/assets/topo-lossless.png)

![Example wired setup](../../docs/assets/photo-dual-exp1.jpg)

| Role | UDP port |
| --- | --- |
| Server (satellite) | `5405` |
| Client (terminal) | `5407` |

### Steps (two keyboards)

1. Disable Wi-Fi on both laptops so only the wired path is used.
2. Read addresses:

```bash
ip a
```

Example only — use your own:

| Machine | Example IP | Example NIC |
| --- | --- | --- |
| Server | `192.168.10.250` | `ens33` |
| Client | `192.168.10.77` | `enp3s0f1` |

3. Start Wireshark on either machine and select that NIC.
4. From the **client**, check reachability:

```bash
ping -c 5 <SERVER_IP>
```

5. In `Code_exp2/EXP_1` on the client, then on the server:

```bash
bash client.sh -c <CLIENT_IP>
bash server.sh -s <SERVER_IP> -c <CLIENT_IP>
```

Optional interval in seconds (default `1`):

```bash
bash server.sh -s <SERVER_IP> -c <CLIENT_IP> -t 1
```

6. Wireshark filter:

```text
udp && ip.src==<SERVER_IP> && ip.dst==<CLIENT_IP>
```

### Expected result

- Server prints `Hello 1` … `Hello 100` and `the latency is 1.0 s`.
- Client receives every message in order.
- I/O graph jumps from idle to a steady rate for the duration of the burst.

### Same lab via SSH

Install OpenSSH on **both** machines:

```bash
sudo apt update
sudo apt install ssh -y
```

From the client:

```bash
ssh <USER>@<SERVER_IP>
cd /path/to/Code_exp2/EXP_1
```

Keep a local terminal in `EXP_1` for the client, and the SSH session for the server. Commands are the same as above.

> [!WARNING]
> Do not copy the old lab path `/home/<user>/Desktop/Code_exp2/EXP_1` literally. Use the clone location on your machine.

### Demos

- [SSH version](https://youtu.be/7__p9velytY)
- [Two-keyboard version](https://youtu.be/W1oNWTd6RF8)

---

## Experiment 2: Lossy data transmission

**Goal:** Wi-Fi path plus a proxy that adds delay and loss, simulating the lossy transmission characteristics of a real-world wireless satellite link to make the experiment results closer to reality.

**Hardware:**

- 2 × Linux laptops (Ubuntu 22.04)
- 1 × Wi-Fi AP

Run **Server** on laptop 1. On laptop 2, run **Client** and **Proxy** in two terminals.

![Lossy topology](../../docs/assets/topo-lossy.png)

![Example two-machine wireless setup](../../docs/assets/photo-dual-full.jpg)

| Role | UDP port |
| --- | --- |
| Server | `5405` |
| Proxy | `5406` |
| Client | `5407` |

On the client laptop, Proxy IP equals Client IP (same host, two processes).

### Steps

1. Join both laptops to the same AP.
2. Read IPs with `ip a`. Example only: Server `192.168.10.225`, Client/Proxy `192.168.10.54`.
3. Optional: install `ssh` on both machines and open the server directory over SSH:

```bash
ssh <USER>@<SERVER_IP>
cd /path/to/Code_exp2/EXP_2
```

4. Capture on the interface that carries the Wi-Fi traffic (or `lo` if you only watch local proxy-to-client).
5. On the **client laptop**, in `Code_exp2/EXP_2`:

```bash
bash client.sh -c <CLIENT_IP>
bash proxy.sh -p <PROXY_IP> -c <CLIENT_IP> -t <DELAY_S> -l <LOSS_RATE>
```

`-t` is delay in seconds; `-l` is drop probability (`0`–`1`). Defaults: `-t 1`, `-l 0`.

6. On the **server**:

```bash
bash server.sh -s <SERVER_IP> -p <PROXY_IP>
```

### Expected result

- Server prints every Hello.
- Proxy delays, then forwards (`1`) or drops (`0`).
- Client sees missing sequence numbers.

### Logs and plot

CSV files are written in `EXP_2` on each machine (`exp2_server.csv` on the server, `exp2_client.csv` on the client). Copy the server CSV onto the client (USB, email, or `scp`):

```bash
scp exp2_server.csv <USER>@<CLIENT_IP>:/path/to/Code_exp2/EXP_2/
```

On the client:

After installing the Python 3 venv package, create a virtual environment `env`. Then activate `env` and install `matplotlib` inside the virtual environment.

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

Output: per-packet delay or loss, `exp2_result.csv`, and `exp2_result.png` (x: packet index, y: delay in seconds; losses are blank).

![Sample EXP_2 plot](../../docs/assets/exp2-result.png)

![Sample EXP_2 plot, zoomed](../../docs/assets/exp2-result-zoom.png)

> [!NOTE]
> Shape of the plot depends mainly on the loss rate.

### Demos

- [SSH version](https://youtu.be/vreE52qI2y0)
- [Two-keyboard version](https://youtu.be/4_SLUV8H_1M)
