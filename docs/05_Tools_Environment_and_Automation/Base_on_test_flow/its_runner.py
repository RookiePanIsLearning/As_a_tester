#!/usr/bin/env python3
"""
Camera ITS 互動式測試小幫手 (its-runner)
========================================
根據 testFlow.md 三階段設計：
  1. 環境準備 (Preparation)
  2. 設定 (Settings)
  3. 執行測試 (Run ITS)

使用方式：
  python3 its_runner.py
  # 或安裝後直接 its-runner
"""

import os
import subprocess
import sys
from pathlib import Path

try:
    import questionary
    import yaml
except ImportError:
    print("缺少必要套件，請執行：pip install questionary pyyaml")
    sys.exit(1)

# ──────────────────────────────────────────────────────────────
# 預設設定與 config.yml 管理
# ──────────────────────────────────────────────────────────────

CONFIG_PATH = Path("config.yml")

DEFAULT_CONFIG: dict = {
    "serial": "DEVICE_DSN",
    "camera_id": "0",
    "chart_distance": 22.0,
    "scene": "scene1_1",
    "debug_mode": True,
    "foldable_device": False,
    "conda_env": "its_env_py3_ffmpeg",
    "its_dir": "/path/to/CameraITS",
}

SCENES = [
    "scene0",
    "scene1_1", "scene1_2",
    "scene2_a", "scene2_b", "scene2_c", "scene2_d", "scene2_e",
    "scene3",
    "scene4",
    "scene5",
    "scene6",
    "scene_extensions",
    "sensor_fusion",
    "自訂輸入 (Custom)",
]

CAMERA_IDS = [
    "0  (Rear Logical)",
    "1  (Front)",
    "2  (Rear Ultra-wide)",
    "3  (Rear Tele)",
    "自訂輸入 (Custom)",
]


def load_config() -> dict:
    """從 config.yml 讀取設定，如不存在則使用預設值。"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return {**DEFAULT_CONFIG, **data}
    return dict(DEFAULT_CONFIG)


def save_config(cfg: dict) -> None:
    """將設定寫入 config.yml。"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print("\n✅ 設定已更新並儲存至 config.yml！")


# ──────────────────────────────────────────────────────────────
# 輔助函式
# ──────────────────────────────────────────────────────────────

def _divider(title: str = "") -> None:
    label = f"  {title}  " if title else ""
    line = "─" * max(0, (50 - len(label)) // 2)
    print(f"\n{line}{label}{line}")


def _run_shell(cmd: str, confirm: bool = True) -> None:
    """可選確認後執行 shell 指令。"""
    if confirm:
        ok = questionary.confirm(f"  要現在執行以下指令嗎？\n  $ {cmd}", default=False).ask()
        if not ok:
            return
    subprocess.run(cmd, shell=True, executable="/bin/bash")


def _ask_safe(prompt_fn):
    """包裝 questionary 呼叫，Ctrl+C 時回傳 None 而非例外。"""
    try:
        return prompt_fn()
    except KeyboardInterrupt:
        return None


# ──────────────────────────────────────────────────────────────
# 階段一：環境準備
# ──────────────────────────────────────────────────────────────

def menu_preparation(cfg: dict) -> None:
    _divider("1. 環境準備 (Preparation)")

    steps = [
        {
            "desc": "前往 go/ab 搜尋 Branch Name，並確認 Build 已完成",
            "hint": "尚未完成前請勿繼續，以免測試基礎版本錯誤。",
            "cmd": None,
        },
        {
            "desc": "Flash Device（刷機）",
            "hint": "確保裝置已刷入正確的 Build 版本。",
            "cmd": None,
        },
        {
            "desc": "下載並解壓縮 android-cts-verifier.zip",
            "hint": "解壓縮後確認 CtsVerifier.apk 存在於目錄中。",
            "cmd": None,
        },
        {
            "desc": "安裝 CtsVerifier.apk",
            "hint": "需要已連線的 adb 裝置。",
            "cmd": f"adb -s {cfg['serial']} install -r -g CtsVerifier.apk",
        },
        {
            "desc": f"啟動 Conda 虛擬環境：{cfg['conda_env']}",
            "hint": "請在執行測試的終端機中手動啟動。",
            "cmd": f"conda activate {cfg['conda_env']}",
        },
    ]

    for i, step in enumerate(steps, 1):
        print(f"\n[{i}/{len(steps)}] {step['desc']}")
        if step["hint"]:
            print(f"      ⚠  {step['hint']}")

        done = _ask_safe(
            lambda s=step: questionary.confirm("  ✔  已完成此步驟？", default=False).ask()
        )
        if done is None:
            print("\n↩  返回主選單")
            return
        if not done:
            print("  ⏸  請完成此步驟後再繼續。")
            return
        if step["cmd"]:
            _run_shell(step["cmd"])

    print("\n✅ 環境準備完成！可以繼續進行設定或執行測試。")


# ──────────────────────────────────────────────────────────────
# 階段二：設定
# ──────────────────────────────────────────────────────────────

def menu_settings(cfg: dict) -> dict:
    _divider("2. 設定 (Settings)")

    while True:
        choice = _ask_safe(lambda: questionary.select(
            "選擇你要修改的參數（Ctrl+C 返回）：",
            choices=[
                f"Camera ID         (目前: {cfg['camera_id']})",
                f"Chart Distance    (目前: {cfg['chart_distance']} cm)",
                f"Scene             (目前: {cfg['scene']})",
                f"Serial            (目前: {cfg['serial']})",
                f"Debug Mode        (目前: {'開啟' if cfg['debug_mode'] else '關閉'})",
                f"Foldable Device   (目前: {'是' if cfg['foldable_device'] else '否'})",
                f"Conda Env         (目前: {cfg['conda_env']})",
                f"CameraITS 目錄    (目前: {cfg['its_dir']})",
                "← 儲存並返回",
            ],
        ).ask())

        if choice is None or "返回" in choice:
            save_config(cfg)
            break

        # Camera ID
        if "Camera ID" in choice:
            val = _ask_safe(lambda: questionary.select(
                "請選擇 Camera ID：",
                choices=CAMERA_IDS,
            ).ask())
            if val and "自訂" in val:
                val = _ask_safe(lambda: questionary.text("請輸入自訂的 Camera ID：").ask())
                cfg["camera_id"] = str(val).strip() if val else cfg["camera_id"]
            elif val:
                cfg["camera_id"] = val.split()[0]

        # Chart Distance
        elif "Chart Distance" in choice:
            val = _ask_safe(lambda: questionary.select(
                "請選擇圖表距離：",
                choices=["22.0 cm", "31.0 cm", "自訂輸入 (Custom)"],
            ).ask())
            if val and "自訂" in val:
                raw = _ask_safe(lambda: questionary.text("請輸入距離（公分）：").ask())
                try:
                    cfg["chart_distance"] = float(raw)
                except (TypeError, ValueError):
                    print("  ⚠  請輸入有效數字，設定未變更。")
            elif val:
                cfg["chart_distance"] = float(val.split()[0])

        # Scene
        elif "Scene" in choice:
            val = _ask_safe(lambda: questionary.select(
                "請選擇 Scene：",
                choices=SCENES,
            ).ask())
            if val and "自訂" in val:
                val = _ask_safe(lambda: questionary.text("請輸入 Scene 名稱：").ask())
                cfg["scene"] = str(val).strip() if val else cfg["scene"]
            elif val:
                cfg["scene"] = val

        # Serial
        elif "Serial" in choice:
            val = _ask_safe(lambda: questionary.text(
                "請輸入裝置 Serial（可透過 adb devices 查詢）：",
                default=cfg["serial"],
            ).ask())
            if val:
                cfg["serial"] = val.strip()

        # Debug Mode
        elif "Debug Mode" in choice:
            val = _ask_safe(lambda: questionary.confirm(
                "啟用 Debug Mode？",
                default=cfg["debug_mode"],
            ).ask())
            if val is not None:
                cfg["debug_mode"] = val

        # Foldable Device
        elif "Foldable" in choice:
            val = _ask_safe(lambda: questionary.confirm(
                "這是折疊螢幕裝置 (Foldable Device)？",
                default=cfg["foldable_device"],
            ).ask())
            if val is not None:
                cfg["foldable_device"] = val

        # Conda Env
        elif "Conda" in choice:
            val = _ask_safe(lambda: questionary.text(
                "請輸入 Conda 環境名稱：",
                default=cfg["conda_env"],
            ).ask())
            if val:
                cfg["conda_env"] = val.strip()

        # CameraITS 目錄
        elif "CameraITS" in choice:
            val = _ask_safe(lambda: questionary.text(
                "請輸入 CameraITS 目錄絕對路徑：",
                default=cfg["its_dir"],
            ).ask())
            if val:
                cfg["its_dir"] = val.strip()

    return cfg


# ──────────────────────────────────────────────────────────────
# 階段三：執行測試
# ──────────────────────────────────────────────────────────────

def menu_run(cfg: dict) -> None:
    _divider("3. 執行測試 (Run ITS)")

    # 燈光提醒
    print("\n💡 提醒：請確認測試燈光已開啟，圖表距離為", cfg["chart_distance"], "cm")

    mode = _ask_safe(lambda: questionary.select(
        "選擇執行模式：",
        choices=[
            "全套測試  run_all_tests.py",
            "單項測試  指定 scene / test",
            "← 返回",
        ],
    ).ask())

    if mode is None or "返回" in mode:
        return

    its = cfg["its_dir"]
    setup_prefix = f"cd {its} && source build/envsetup.sh"

    if "全套" in mode:
        cmd = f"{setup_prefix} && python tools/run_all_tests.py camera={cfg['camera_id']}"
        print(f"\n  指令預覽：\n  {cmd}\n")
        confirmed = _ask_safe(lambda: questionary.confirm("確認執行？", default=True).ask())
        if confirmed:
            subprocess.run(cmd, shell=True, executable="/bin/bash")

    else:
        # 單項測試
        scene = _ask_safe(lambda: questionary.select(
            "選擇 Scene：",
            choices=SCENES,
        ).ask())
        if not scene:
            return
        if "自訂" in scene:
            scene = _ask_safe(lambda: questionary.text("請輸入 Scene 名稱：").ask())
            if not scene:
                return

        test_name = _ask_safe(lambda: questionary.text(
            "請輸入 test 檔案名稱（不含 .py，例如 test_black_white_levels）：",
        ).ask())
        if not test_name:
            return

        testbed = _ask_safe(lambda: questionary.text(
            "請輸入 testbed 名稱（config.yml 內的 Name）：",
            default="TRAILBLAZER",
        ).ask()) or "TRAILBLAZER"

        cmd = (
            f"{setup_prefix} && "
            f"python3 tests/{scene}/{test_name}.py "
            f"-c config.yml --test_bed {testbed}"
        )
        print(f"\n  指令預覽：\n  {cmd}\n")
        confirmed = _ask_safe(lambda: questionary.confirm("確認執行？", default=True).ask())
        if confirmed:
            subprocess.run(cmd, shell=True, executable="/bin/bash")


# ──────────────────────────────────────────────────────────────
# 主程式
# ──────────────────────────────────────────────────────────────

BANNER = """
╔══════════════════════════════════════════════╗
║   歡迎使用 Camera ITS 測試小幫手 🚀            ║
║   Camera ITS Interactive Test Runner         ║
╚══════════════════════════════════════════════╝"""


def main() -> None:
    print(BANNER)
    cfg = load_config()

    while True:
        # 狀態列
        print(
            f"\n  裝置: {cfg['serial']}  │  "
            f"Camera: {cfg['camera_id']}  │  "
            f"Scene: {cfg['scene']}  │  "
            f"Distance: {cfg['chart_distance']} cm"
        )

        choice = _ask_safe(lambda: questionary.select(
            "請問你要執行什麼操作？",
            choices=[
                "1. 環境準備 (Preparation)",
                "2. 進入設定 (Settings)",
                "3. 執行測試 (Run ITS)",
                "4. 離開 (Exit)",
            ],
        ).ask())

        if choice is None or choice.startswith("4"):
            print("\n再見！👋\n")
            break
        elif choice.startswith("1"):
            menu_preparation(cfg)
        elif choice.startswith("2"):
            cfg = menu_settings(cfg)
        elif choice.startswith("3"):
            menu_run(cfg)


if __name__ == "__main__":
    main()
