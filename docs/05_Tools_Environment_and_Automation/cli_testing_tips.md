# CLI Testing Tips

在測試過程中，使用 CLI（命令列介面）工具可以大幅提升效率，以下是一些實用的建議：

1. **自動化腳本**：
   - 將常用的測試指令寫成腳本（如 Bash 或 Python），減少重複輸入。
   - 使用參數化腳本來處理不同的測試場景。

2. **命令別名**：
   - 利用 shell 的別名功能（如 `alias`），為常用指令設定簡短的名稱。
   - 範例：`alias runtest='python3 test_runner.py'`

3. **日誌與輸出**：
   - 使用 `tee` 或重定向（`>`）將測試輸出保存到文件中，方便後續分析。
   - 範例：`python3 test_runner.py | tee output.log`

4. **CLI 工具推薦**：
   - **jq**：處理 JSON 輸出。
   - **grep**：快速篩選關鍵字。
   - **awk**：格式化輸出。
   - **curl**：模擬 HTTP 請求。

5. **環境管理**：
   - 使用 `.env` 文件或環境變數來管理測試配置。
   - 範例：`export TEST_ENV=staging`

6. **持續優化**：
   - 定期整理和優化常用指令，確保工具鏈高效運作。

透過這些技巧，測試工程師可以更高效地執行測試，並減少手動操作的錯誤率。

## 📸 Camera Logcat 篩選工具 (CLI) 開發紀錄

### 📌 專案簡介
為了解決 adb logcat 輸出資訊過於龐雜的問題，開發了一支互動式的 Bash CLI 腳本 (cam_logger.sh)。此工具內建多種 Camera 與 Tuning 的專屬過濾情境（如 Calibration Data, HAL parameters, AWB 等），讓工程師能快速且精準地抓取並分析目標 Log。

### ✨ 核心功能演進

**基本選單與過濾整合**
- 將 24 種相機 Log 情境與對應的 grep 指令整合進腳本。
- 支援透過指令參數指定特定裝置（例如 ./cam_logger.sh -s 12345ABCDE）。

**防呆與互動體驗優化 (無縫迴圈)**
- 加入 while true 無窮迴圈。
- 攔截 Ctrl+C (SIGINT Signal)：當使用者按下 Ctrl+C 時，只會中斷當前的 adb logcat 程序，而不會直接退出整個腳本。

**優雅的 Log 檢閱機制 (暫停與保留畫面)**
- 終端機暫停技巧：在介面上增加 [Ctrl+S] (暫停滾動) 與 [Ctrl+Q] (恢復滾動) 的快捷鍵提示。
- 保留檢閱畫面：按下 Ctrl+C 停止抓取後，程式會暫停並提示 Press ANY KEY to return to the main menu，確保關鍵 Log 不會因畫面立刻被 clear 清除而遺失。

**快捷鍵與按鍵偵測 (read -rsn1)**
- 捨棄傳統需按 Enter 的輸入方式，改為讀取單一字元。
  - [a]：快速執行 adb devices。
  - [k]：快速執行 adb kill-server (解決設備 offline 或找不到的問題)。
  - [ESC]：一鍵完全退出程式。

**終端機 UI 美化**
- 導入 ANSI Color Codes，利用顏色（如綠色、黃色、青色）區分分隔線、執行指令與警告提示，提升閱讀舒適度。

### 💡 關鍵技術與知識點筆記

**grep --line-buffered (行緩衝)**
- **問題**：當 adb logcat 透過 pipe (|) 傳給 grep 時，預設會啟動「區塊緩衝」，導致 Log 會卡住幾秒才一次大量印出，無法即時監控。
- **解法**：加入 --line-buffered 參數，強制 grep 只要讀到換行符號就立刻輸出，達成零延遲的即時 Log 顯示。

**grep --color=always (強制顏色高亮)**
- **問題**：一般終端機打 grep 會有紅色關鍵字，是因為系統 .bashrc 預設綁定了 alias grep='grep --color=auto'。但 Bash Script 在背景執行時不會載入使用者的 alias，導致 Log 失去顏色。
- **解法**：在腳本內的 grep 加上 --color=always，強制在輸出中加入顏色控制碼，完美重現終端機裡的高亮效果。