"""
Simple project launcher helper.

Usage:
    python main.py train
    python main.py api
    python main.py ui
"""

import subprocess
import sys


def run_train() -> None:
    subprocess.run([sys.executable, "backend/train.py"], check=True)


def run_api() -> None:
    subprocess.run([sys.executable, "backend/app.py"], check=True)


def run_ui() -> None:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/streamlit_app.py"], check=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide one argument: train | api | ui")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "train":
        run_train()
    elif command == "api":
        run_api()
    elif command == "ui":
        run_ui()
    else:
        print("Invalid argument. Use: train | api | ui")
        sys.exit(1)
