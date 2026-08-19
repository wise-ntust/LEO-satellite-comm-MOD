# 實驗 2 — 單機版手冊

[English](manual-single.md) | [繁體中文](manual-single.zh-TW.md)

> [!NOTE]
> 在**同一台** Ubuntu 電腦用多個終端機分別跑 Server、Proxy、Client。在同一張網卡上新增第二個 IP，讓兩個角色有不同位址。不需要 Wi-Fi AP。

![單機概念](../../docs/assets/topo-single-concept.png)

## Wireshark 安裝（選用）

透過 apt 指令 (Ubuntu/Debian) 安裝 wireshark 後，重新安裝具有免 root 權限抓包的功能。

```bash
sudo apt install wireshark
sudo dpkg-reconfigure wireshark-common
```

允許一般使用者抓封包時選 Yes。接著把目前使用者加入 wireshark 群組，並用 newgrp 立刻套用（否則要登出再登入）：

```bash
sudo usermod -aG wireshark $USER
newgrp wireshark
wireshark
```

開啟 Wireshark 後選擇監控 `Loopback: lo`（或你用來加 IP 的網卡）。再進 **Statistics → I/O Graphs** 觀察 I/O Graphs。
## 前置步驟

### 1. 查出本機 IP 與網卡名稱

```bash
ip a
```

若已安裝 `net-tools`，也可用 `ifconfig`。

範例（請改成你的環境）：

| 角色 | 範例 |
| --- | --- |
| Server IP | `192.168.0.225` |
| 網卡名稱 | `ens33` |
| Client / Proxy IP | `192.168.0.226` |

### 2. 為 Client（與 Proxy）新增第二個 IP

```bash
sudo ip addr add <CLIENT_IP>/24 dev <NIC_NAME>
```

用 `ip a` 確認，再測試連線：

```bash
ping -c 3 -I <NIC_NAME> <CLIENT_IP>
ping -c 3 -I <NIC_NAME> <SERVER_IP>
```

> [!TIP]
> 這個額外 IP 會在重開機後會消失，除非寫進 netplan / NetworkManager 才能永久保存。

---

## Experiment 1: Lossless data transmission（無損傳輸）

**目標：** 在單純有線路徑上傳送 UDP（不經 Proxy），觀察無損傳輸。

**設備：** Linux 筆電 × 1

**拓樸圖**

![無損拓樸](../../docs/assets/topo-lossless.png)

### 步驟

1. 完成上面的前置步驟。
2. 開起 Wireshark 觀察流量。
3. 在 `Code_exp2/EXP_1` 先啟動 Client，再啟動 Server：

```bash
bash client.sh -c <CLIENT_IP>
bash server.sh -s <SERVER_IP> -c <CLIENT_IP>
```

可加發送間隔（秒，預設 `1`）：

```bash
bash server.sh -s <SERVER_IP> -c <CLIENT_IP> -t 1
```

4. 在 Wireshark 設定以下過濾器，使用 **I/O Graphs** 觀察結果：

```text
udp && ip.src==<SERVER_IP> && ip.dst==<CLIENT_IP>
```

### 預期結果

- Server 印出 `Hello 1` … `Hello 100`，以及 `the latency is 1.0 s`（兩次發送之間的等待）。
- Client 依序收到全部訊息。
- I/O Throuput 圖從閒置跳升至 1 pkt/s，並在傳送期間維持穩定速率。

### 示範影片

[單機無損示範](https://youtu.be/-hyNTx92kDg)

---

## Experiment 2: Lossy data transmission（有損傳輸）

**目標：** 加入 Proxy，模擬延遲與隨機丟包，以模擬現實中無線級衛星鏈路的有損傳輸特性，使實驗結果更貼近真實環境。

**設備：** Linux 筆電 × 1

![有損拓樸](../../docs/assets/topo-lossy.png)

單機模式下，Client IP 與 Proxy IP 是**同一個**額外位址。

### 步驟

1. 若實驗 1 的額外 IP 還在，可直接沿用。
2. 在 `Code_exp2/EXP_2` 開三個終端機，依 **Client → Proxy → Server** 順序執行腳本：

```bash
bash client.sh -c <CLIENT_IP>
bash proxy.sh -p <PROXY_IP> -c <CLIENT_IP> -t <DELAY_S> -l <LOSS_RATE>
bash server.sh -s <SERVER_IP> -p <PROXY_IP>
```

- `-t`：延遲秒數（例如 `1`）
- `-l`：丟包機率，`0` 到 `1`（例如 `0.2` 代表 20% Loss）

省略時預設 `-t 1`、`-l 0`。

### 預期結果

- Server 印出每個 Hello。
- Proxy 先延遲，再轉發（結果 1）或丟棄（結果 0）。
- Client 會看到不連續的編號。

### 紀錄與繪圖

跑完後，`EXP_2` 會出現 `exp2_server.csv` 與 `exp2_client.csv`。

接著安裝 python3 的虛擬環境套件後，建立虛擬環境 `env`。先啟用環境 `env`，再於虛擬環境內安裝 matplotlib。

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv env
source ./env/bin/activate
pip3 install matplotlib
```

在終端機中執行以下指令，觀察實驗的執行結果。

```bash
python3 exp2_result.py
```

程式會印出每個封包的延遲或 `packet is loss`，寫出 `exp2_result.csv`，並儲存 `exp2_result.png`（橫軸：封包編號；縱軸：延遲秒；丟包為空白）。

![EXP_2 範例圖](../../docs/assets/exp2-result.png)

![EXP_2 範例圖（放大）](../../docs/assets/exp2-result-zoom.png)

> [!NOTE]
> 每次圖形都會不同，主要受 `-t` 與 `-l` 影響。

### 示範影片

[單機有損示範](https://youtu.be/pFleC9UVsZ8)
