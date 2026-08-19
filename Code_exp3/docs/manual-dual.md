# Experiment 3 — Two-machine manual

[English](manual-dual.md) | [繁體中文](manual-dual.zh-TW.md)

Two Ubuntu laptops share a Wi-Fi AP. Run **Server** on laptop 1. On laptop 2, run **Client** and **Proxy**. You may SSH from the client into the server.

## Idea

FIFO forwarding through a **Gateway**. End-to-end delay follows the **elevation angle θ** (integer, degrees): every two packets share one angle, starting at 90° and decreasing with packet index. `proxy.sh` applies millisecond-scale banded delays (~4–5 ms); `proxy_new.sh` amplifies the same trend to 100–800 ms.

## Hardware

- 2 × Linux laptops (Ubuntu 22.04)
- 1 × Wi-Fi AP

## Topology

![FIFO topology](../../docs/assets/topo-lossy.png)

![Example two-machine setup](../../docs/assets/photo-dual-full.jpg)

| Role | UDP port |
| --- | --- |
| Server | `5405` |
| Proxy | `5406` |
| Client | `5407` |

On the client laptop, Proxy IP equals Client IP.

## Steps

1. Join both laptops to the same AP.
2. Read addresses with `ip a`. Example only: Server `192.168.10.225`, Client/Proxy `192.168.10.54`.
3. Optional SSH (install on both machines):

```bash
sudo apt update
sudo apt install ssh -y
ssh <USER>@<SERVER_IP>
cd /path/to/Code_exp3
```

> [!WARNING]
> Older notes sometimes used `Code_exp2/EXP_2` for this lab. The correct directory is **`Code_exp3`**.

4. On the **client laptop**, in `Code_exp3`:

```bash
bash client.sh -c <CLIENT_IP>
bash proxy.sh -p <PROXY_IP> -c <CLIENT_IP>
```

Larger-delay Gateway:

```bash
bash proxy_new.sh -p <PROXY_IP> -c <CLIENT_IP>
```

5. On the **server**:

```bash
bash server.sh -s <SERVER_IP> -p <PROXY_IP>
```

Elevation formula and tables: [README.md](../README.md).

## Expected result

- Server sends Hello messages in FIFO order.
- Proxy applies banded delays by packet range (matching elevation bands) and prints delay in milliseconds.
- Client prints received packets. Order stays FIFO; the delay curve rises as elevation falls.

## Logs and plot

Copy `exp3_server.csv` from the server into the client `Code_exp3` folder (USB, email, or `scp`):

```bash
scp exp3_server.csv <USER>@<CLIENT_IP>:/path/to/Code_exp3/
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
python3 exp3_result.py
```

Output is delay in milliseconds, `exp3_result.csv`, and `exp3_result.png`.

![Sample EXP_3 plot](../../docs/assets/exp3-result.png)

![Sample EXP_3 plot, zoomed](../../docs/assets/exp3-result-zoom.png)

## Demos

- [SSH version](https://youtu.be/Dvt-ubPZeYw)
- [Two-keyboard version](https://youtu.be/yKwiv8is5-I)
