# setup.py — Fury AI Assistant
# Allows: pip install -e . for dev mode

from setuptools import setup, find_packages

setup(
    name="fury-ai",
    version="1.0.0",
    description="Fury — Autonomous AI Desktop Assistant",
    author="Fury Dev",
    python_requires=">=3.10",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "pyautogui>=0.9.54",
        "pynput>=1.7.6",
        "mss>=9.0.1",
        "opencv-python>=4.8.0",
        "pytesseract>=0.3.10",
        "numpy>=1.24.0",
        "playwright>=1.40.0",
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pyyaml>=6.0.1",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "fury=fury:start_fury",
        ]
    },
)