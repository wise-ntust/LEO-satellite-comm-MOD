# 實驗 3 — 雙機版手冊

[English](manual-dual.md) | [繁體中文](manual-dual.zh-TW.md)

兩台 Ubuntu 筆電連同一個 Wi-Fi AP。筆電 1 跑 **Server**；筆電 2 跑 **Client** 與 **Proxy**。也可以從 Client SSH 到 Server。

## 實驗概念

封包經 **Gateway** 以 FIFO 轉發。端到端延遲由**仰角 θ**（整數，°）決定：每兩個封包共用同一仰角，從 90° 起隨封包序號遞減。`proxy.sh` 依封包區間套用毫秒級延遲（約 4–5 ms），`proxy_new.sh` 將同一趨勢放大至 100–800 ms。

## 設備

- Linux 筆電 × 2
- Wi-Fi AP × 1

## 拓樸

![FIFO 拓樸](../../docs/assets/topo-lossy.png)

![雙機實機範例](../../docs/assets/photo-dual-full.jpg)

| 角色 | UDP 埠 |
| --- | --- |
| Server | `5405` |
| Proxy | `5406` |
| Client | `5407` |

在 Client 筆電上，Proxy IP 與 Client IP 相同。

## 步驟

1. 兩台都連上同一個 AP。
2. 使用以下指令查詢 IP 及使用的 Interface：

```bash
ip a
```

僅供參考，請用你自己的位址：

| 機器 | 範例 IP | 範例網卡 |
| --- | --- | --- |
| Server | `192.168.10.250` | `ens33` |
| Client | `192.168.10.77` | `enp3s0f1` |

3. 可選 SSH（兩台都安裝）：

```bash
sudo apt update
sudo apt install ssh -y
ssh <USER>@<SERVER_IP>
cd /path/to/Code_exp3
```

4. 在 **Client 筆電** 的 `Code_exp3`：

```bash
bash client.sh -c <CLIENT_IP>
bash proxy.sh -p <PROXY_IP> -c <CLIENT_IP>
```

若要換成延遲較大的 Gateway：

```bash
bash proxy_new.sh -p <PROXY_IP> -c <CLIENT_IP>
```

5. 在 **Server**：

```bash
bash server.sh -s <SERVER_IP> -p <PROXY_IP>
```

延遲公式與對照表見 [README.zh-TW.md](../README.zh-TW.md)。

## 預期結果

- Server 依 FIFO 送出 Hello。
- Proxy 依封包區間套用對應仰角的延遲，並印出延遲（毫秒）。
- Client 印出收到的封包。順序仍是 FIFO；延遲曲線隨仰角下降而上升。

## 紀錄與繪圖

把 Server 上的 `exp3_server.csv` 複製到 Client 的 `Code_exp3`（透過 USB、Email 或 `scp`）：

```bash
scp exp3_server.csv <USER>@<CLIENT_IP>:/path/to/Code_exp3/
```

在 Client 執行以下指令安裝 python3 的虛擬環境套件後，建立虛擬環境 `env`。先啟用環境 `env`，再於虛擬環境內安裝 matplotlib。

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv env
source ./env/bin/activate
pip3 install matplotlib
```

在終端機中執行以下指令，觀察實驗的執行結果。

```bash
python3 exp3_result.py
```

輸出為毫秒延遲、`exp3_result.csv`、以及 `exp3_result.png`。

![EXP_3 範例圖](../../docs/assets/exp3-result.png)

![EXP_3 範例圖（放大）](../../docs/assets/exp3-result-zoom.png)

## 示範影片

- [SSH 版](https://youtu.be/Dvt-ubPZeYw)
- [兩台各自操作](https://youtu.be/yKwiv8is5-I)
