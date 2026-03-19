# As_a_tester
Knowledge as a Test Engineer.

## 專案結構

這個專案用來存放測試工程師的專業知識文獻。檔案架構如下：

- `docs/` - 文獻根目錄
  - `01_Test_Strategy_and_Policies/` - 測試策略與規範
  - `02_Testing_Methods_and_Theories/` - 測試手法與理論
  - `03_Test_Case_Design_and_Repository/` - 測項設計與案例庫
  - `04_Skills_and_Heuristics/` - 常用技巧與啟發式思維
  - `05_Tools_Environment_and_Automation/` - 工具、環境與自動化
    - `Automation_Frameworks/` - 自動化框架相關文獻
  - `06_Reports_and_Metrics_Archive/` - 報告與指標封存
  - `07_Personal_Insights/` - 個人經驗與學習紀錄
    - `Case_Studies/` - 案例研究
    - `Experience_Stories/` - 經驗故事
    - `Lessons_Learned/` - 經驗教訓
  - `08_Strategy_Generation/` - 策略生成資源
    - `Templates/` - 模板
    - `Guidelines/` - 指南
    - `Automation_Tools/` - 自動化工具

每個子資料夾內可以放置相關的 Markdown 檔案來記錄知識點。

## 文獻處理指南

### 1. 分類原則
- 根據內容主題將文獻放入對應的子資料夾
- 如果文獻涵蓋多個主題，可以複製到相關資料夾或在主要資料夾中放置，並使用內部連結

### 2. 檔案命名規範
- 使用英文或拼音命名，格式：`YYYY-MM-DD_主題_簡述.md`
- 例如：`2024-01-15_Boundary_Value_Analysis.md`
- 避免中文檔案名以確保相容性

### 3. 內容格式
- 使用 Markdown 格式
- 在檔案開頭添加元資料：
  ```
  ---
  title: 文獻標題
  author: 作者
  date: YYYY-MM-DD
  tags: [tag1, tag2]
  category: 對應分類
  ---
  ```

### 4. 索引維護
- 每個子資料夾的 `index.md` 應列出該資料夾的所有檔案
- 定期更新索引以保持最新

### 5. 版本控制
- 使用 Git 提交變更
- 提交訊息格式：`Add: [分類] 文獻標題`

### 6. 工具建議
- 使用 VS Code 或 Obsidian 編輯 Markdown
- 考慮使用 GitHub Issues 或 Projects 來追蹤文獻整理進度
- 使用 `process_literature.py` 腳本快速生成檔案模板：
  ```
  python3 process_literature.py "文獻標題" "作者" "分類路徑"
  ```
