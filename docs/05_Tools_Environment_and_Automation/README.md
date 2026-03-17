# 工具、環境與自動化

此目錄用於存放測試環境建置指南與自動化工具文檔。

## 建議內容
- 測試環境建置指南
- 本機端設定檔（如 .config 相關設定）
- CI/CD 管道的自動化構建腳本
- 自動化測試框架（如 Playwright、Selenium 等）的最佳實踐與工具使用手冊

## CLI Testing Tips

在測試過程中，使用 CLI（命令列介面）工具可以大幅提升效率，請參考以下文件：

- [CLI Testing Tips](./cli_testing_tips.md)

## Camera Logcat Tool

這是一個互動式的 CLI 工具，用於過濾和分析 Camera Logcat 資料。

- **檔案名稱**: [camera_logcat_tool.sh](./camera_logcat_tool.sh)
- **功能**:
  - 提供 24 種相機 Log 過濾情境。
  - 支援快捷鍵操作（如 `adb devices`、`adb kill-server`）。
  - 攔截 Ctrl+C 信號，優雅地返回主選單。

### 使用方式
1. 確保已安裝 `adb` 並連接設備。
2. 執行腳本：
   ```bash
   ./camera_logcat_tool.sh
   ```
3. 根據選單選擇需要的 Log 過濾情境。

更多細節請參考腳本內的註解。
