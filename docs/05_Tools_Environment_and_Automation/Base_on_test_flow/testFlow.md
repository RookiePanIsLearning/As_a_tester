``` mermiad
graph TD
    %% 階段一：環境準備
    subgraph Preparation [1. 環境準備與安裝]
        A[前往 go/ab 搜尋 Branch Name] --> B{檢查測試專案與<br/>Build 是否完成?}
        B -- Yes --> C[Flash Device 刷機]
        B -- No --> A
        C --> D[下載並解壓縮 <br/>android-cts-verifier.zip]
        D --> E[安裝 CtsVerifier.apk<br/>adb install -r -g]
        E --> F[啟動 Conda 虛擬環境<br/>its_env_py3_ffmpeg / vic / 25Q2]
    end

    %% 階段二：配置設定
    subgraph Configuration [2. 修改 config.yml]
        F --> G[設定 Serial: DEVICE_DSN]
        G --> H[設定 Chart_distance: 22.0 或 31.0]
        H --> I[設定 debug_mode: True]
        I --> J[指定 Camera ID & Scenes]
        J --> K[設定 foldable_device: True]
    end

    %% 階段三：執行測試
    subgraph Execution [3. 執行測試]
        K --> L[進入 CameraITS 目錄]
        L --> M[執行 source build/envsetup.sh]
        M --> N[開啟光源]
        N --> O{執行模式?}
        
        O -- 全測試 --> P[python tools/run_all_tests.py<br/>camera=1]
        O -- 單項測試 --> Q[python3 tests/sceneX/test_Y.py<br/>-c config.yml --test_bed...]
    end

    %% 結尾
    P --> R[檢查測試結果]
    Q --> R
```
