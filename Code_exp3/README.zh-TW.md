# 實驗 3：FIFO 傳輸與仰角延遲

[English](README.md) | [繁體中文](README.zh-TW.md)

此實驗讓 UDP 封包經過 **Gateway**，並以 **FIFO**（先進先出）順序轉發。端到端延遲由 Gateway **仰角 θ** 決定：封包序號 `i` 對應的仰角隨 `i` 遞增而下降，斜距與傳播延遲因此增加。

`proxy.py` 依封包區間套用對應仰角的延遲（近似物理公式）；`proxy_new.py` 將同一仰角趨勢放大至 100–800 ms，方便觀察實驗結果。

## 拓樸

**拓樸圖**

![Gateway FIFO 拓樸](../docs/assets/topo-lossy.png)

## 檔案說明

| 路徑 | 用途 |
| --- | --- |
| `server.py`、`server.sh` | 傳送 `Hello 1` … `Hello 100` 給 Gateway，並寫入 `exp3_server.csv` |
| `client.py`、`client.sh` | 在埠 `5407` 接收，寫入 `exp3_client.csv` |
| `proxy.py`、`proxy.sh` | Gateway A：FIFO 轉發，使用物裡模型所計算的延遲 |
| `proxy_new.py`、`proxy_new.sh` | Gateway B：FIFO 轉發，放大版延遲（100–800 ms） |
| `exp3_result.py` | 比對時間戳，繪製延遲圖 |

### 仰角與延遲模型

常數：$R_E = 6371$ km、$h_0 = 1200$ km、光速 $c = 3 \times 10^5$ km/s。

封包 `Hello i` 的仰角為**整數**（°），每兩個封包共用同一仰角，起點 90°：

$$
\theta(i) = 90 - \left\lfloor \frac{i-1}{2} \right\rfloor
$$

斜距：

$$
d = \sqrt{R_E^2 \sin^2\alpha + h_0^2 + 2 h_0 R_E} - R_E \sin\alpha
$$

（此處 $\alpha = \theta$。）理論傳播延遲 $\text{delay} = d / c$。例如 90° 約 4.00 ms、80° 約 4.05 ms、70° 約 4.21 ms、60° 約 4.50 ms、50° 約 4.96 ms、40° 約 5.64 ms。

**Gateway A** — `proxy.py`（預設，`bash proxy.sh`），依封包區間套用延遲：

| 封包 i | 仰角 | 延遲 |
| --- | --- | --- |
| 1–20 | 90° | 4.00 ms |
| 21–40 | 80° | 4.05 ms |
| 41–60 | 70° | 4.21 ms |
| 61–80 | 60° | 4.50 ms |
| 81–100 | 50° | 4.96 ms |

**Gateway B** — `proxy_new.py`（`bash proxy_new.sh`），同一仰角趨勢、放大延遲：

| 封包 i | 仰角 | 延遲 |
| --- | --- | --- |
| 1–65 | 90° | 100 ms |
| 66–83 | 58° | 300 ms |
| 84–92 | 49° | 500 ms |
| 93–97 | 44° | 700 ms |
| 98–100 | 41° | 800 ms |

## 快速開始

安裝 python3 的虛擬環境套件後，建立虛擬環境 `env`。先啟用環境 `env`，在於虛擬環境內相關的套件。

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv env
pip3 install -r ../requirements.txt
```

- 單機（同一網卡加第二個 IP）：[manual-single.zh-TW.md](docs/manual-single.zh-TW.md)
- 雙機：[manual-dual.zh-TW.md](docs/manual-dual.zh-TW.md)

## 埠號

| 行程 | 埠 |
| --- | --- |
| Server | `5405` |
| Proxy（Gateway） | `5406` |
| Client | `5407` |
