# As_a_tester
Knowledge as a Test Engineer.

## 專案結構

這個專案用來存放測試工程師的專業知識文獻。檔案架構如下：

- `docs/` - 文獻根目錄
  - `01_Strategy_&_Planning/` - 測試策略與規劃
    - `Test_Strategy_Templates/` - 不同專案類型的策略模板
    - `Risk_Assessment/` - 風險評估與優先等級劃分
    - `Test_Plan_Samples/` - 標準測試計畫書範本
  - `02_Methodologies/` - 常用測試手法
    - `Black_Box/` - 黑箱測試手法
    - `White_Box/` - 白箱測試手法
    - `Non-Functional/` - 非功能性測試
    - `Exploratory_Testing/` - 探索性測試
  - `03_Test_Design_&_Writing/` - 測項撰寫規範
    - `Test_Case_Standards/` - 測項結構標準
    - `Checklists/` - 功能檢查表
    - `Boundary_Conditions/` - 邊界條件清單
  - `04_Tips_&_Best_Practices/` - 常用技巧與實務
    - `Troubleshooting/` - 問題排查技巧
    - `Tools_Guide/` - 工具使用指南
    - `Test_Data_Management/` - 測試資料管理
  - `05_Templates_&_Resources/` - 模板與資源
    - `Bug_Report_Templates/` - Bug 報告模板
    - `Glossary/` - 專業術語表

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
