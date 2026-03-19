# Camera ITS 互動式測試小幫手 — 規格與設計紀錄

> **檔案用途：** 記錄此 CLI 工具的發想、設計決策與架構說明，供接手者快速理解背景脈絡。

---

## 一、為什麼要做這個工具？

Camera ITS（Image Test Suite）的原廠測試流程，要求工程師在終端機逐步完成：

1. 確認 Branch/Build
2. 刷機 → 安裝 APK
3. 手動修改 `config.yml`（Serial、Camera ID、Scene、距離…）
4. 切換到正確目錄、啟動 Conda 環境
5. 手打冗長的 `python tools/run_all_tests.py` 指令

這些步驟**容易出錯、需要記憶、新人學習成本高**。每次測試都要翻文件確認參數，也很難追蹤「這次跑的是哪組設定」。

### 痛點對照

| 原本做法 | 問題 |
|----------|------|
| 手動改 `config.yml` | 容易打錯、忘記改回去 |
| 靠記憶打指令 | 人員交接困難 |
| 沒有設定狀態顯示 | 不確定目前設定是什麼 |
| 沒有操作引導 | 新手容易跳過步驟 |

---

## 二、解決方案：互動式 CLI 工具

打造一個 **防呆、有引導、狀態可見** 的互動式命令列工具，把整個測試流程包裝成選單操作。

### 核心目標

- **防呆（Error Prevention）**：用選單限制輸入範圍，杜絕打錯 Camera ID 或 Scene 名稱。
- **狀態管理（State Management）**：設定統一寫入 `config.yml`，下次執行自動讀取，不用重複設定。
- **降低學習門檻**：新手跟著 CLI 提示走，不需要先看完文件才能跑測試。
- **指令透明化**：執行前先預覽組好的指令，確認才真正執行，避免黑盒子操作。

---

## 三、流程設計（對應 testFlow.md）

整個工具對應 testFlow.md 的三個測試階段：

```
its-runner
│
├── 1. 環境準備 (Preparation)
│   ├── 確認 go/ab Branch & Build 完成
│   ├── Flash Device（刷機）
│   ├── 下載解壓縮 android-cts-verifier.zip
│   ├── adb install CtsVerifier.apk
│   └── conda activate <env>
│
├── 2. 設定 (Settings)  ←─ 讀取 / 寫入 config.yml
│   ├── Camera ID
│   ├── Chart Distance (22.0 / 31.0 cm 或自訂)
│   ├── Scene
│   ├── Serial (device DSN)
│   ├── Debug Mode
│   ├── Foldable Device
│   ├── Conda Env 名稱
│   └── CameraITS 目錄路徑
│
└── 3. 執行測試 (Run ITS)
    ├── 全套測試：python tools/run_all_tests.py camera=<id>
    └── 單項測試：python3 tests/<scene>/<test>.py -c config.yml --test_bed <name>
```

主選單上方會持續顯示當前關鍵設定（Serial / Camera / Scene / Distance），讓工程師一眼確認狀態。

---

## 四、技術選型

| 技術 | 選用理由 |
|------|----------|
| **Python 3** | 測試環境本身就有 Conda + Python，零額外安裝成本 |
| **questionary** | 提供上下鍵互動選單，比 `input()` 體驗好得多，且只需 pip install |
| **PyYAML** | 原廠 `config.yml` 就是 YAML 格式，直接讀寫不需轉換 |
| **subprocess** | 標準函式庫，用來執行原廠測試指令，不引入額外依賴 |

---

## 五、架構決策紀錄（ADR）

### ADR-1：單一檔案 vs 多模組拆分

**討論背景：**  
曾考慮將程式拆成 `main.py` / `menus.py` / `config_parser.py` / `runner.py` 四個模組（Gemini 的建議）。

**決定：保留單一檔案（`its_runner.py`）**

**理由：**
- 目前程式約 270 行，拆分後閱讀時需要在 4 個檔案間跳來跳去，反而增加認知負擔。
- 三個功能區（選單、設定、執行）高度耦合，不會被單獨重用。
- 拆分的觸發條件是「因為太大而難以維護」，不是「因為功能不同」。

**重新評估時機：**  
當任一功能區超過 200 行、或需要加入 `--headless` / CI 模式時，再考慮拆模組。

---

### ADR-2：工具存放位置

**決定：** CLI 工具源碼放在知識庫（`As_a_tester`）的 `Base_on_test_flow/`；  
實際執行時，複製到測試機上，與 `android-cts-verifier/` 並排放置。

**原廠目錄與 CLI 的關係：**

```
camera-its-workspace/          ← 測試機上的工作目錄
├── android-cts-verifier/      ← 原廠不動，升版時直接替換這個資料夾
│   └── CameraITS/
├── its_runner.py              ← 從知識庫複製過來
├── config.yml                 ← CLI 讀寫，ITS 也讀這個
├── requirements.txt
└── README.md
```

**理由：** CLI 工具與原廠程式碼完全分離，ITS 升版時不會覆蓋到自己寫的工具。

---

## 六、目錄說明

```
Base_on_test_flow/
├── its_runner.py     # CLI 主程式（含環境準備、設定、執行三大功能）
├── testFlow.md       # Mermaid 流程圖，記錄原廠測試三階段步驟
├── requirements.txt  # Python 依賴（questionary, pyyaml）
├── pyproject.toml    # 讓 its-runner 成為可安裝的系統指令
└── spec.md           # 本文件：設計紀錄與規格說明
```

---

## 七、安裝與使用

### 在測試機上初次安裝

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 安裝為系統指令（可選）
pip install -e .

# 3. 啟動
its-runner
# 或不安裝直接執行：
python3 its_runner.py
```

### 設定檔說明（config.yml）

工具啟動時會自動讀取同目錄下的 `config.yml`。若不存在，會以預設值建立。

```yaml
serial: DEVICE_DSN          # 裝置序號，adb devices 可查
camera_id: '0'              # Camera ID
chart_distance: 22.0        # 測試圖表距離（cm）
scene: scene1_1             # 測試場景
debug_mode: true
foldable_device: false
conda_env: its_env_py3_ffmpeg
its_dir: /path/to/CameraITS
```

---

## 八、未來可擴充的方向

- `--headless` 模式：跳過互動式選單，直接讀 `config.yml` 執行，適合 CI 腳本呼叫。
- 測試結果解析：執行後自動掃描 log 輸出，標出 PASS / FAIL 的 scene。
- 自動上傳報告：整合 Google Sheet 或內部 Dashboard API，一鍵上傳測試數據。
- 多裝置管理：主選單加入「選擇裝置」功能，支援多台 DUT 同時測試。
- Profile 機制：存多組 `config.yml`（如 `config_rear.yml` / `config_front.yml`），快速切換設備設定。
