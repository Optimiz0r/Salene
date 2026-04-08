#!/usr/bin/env python3
"""
SALENE - Setup script for pip install

Installation:
    pip install .
    
Or from GitHub:
    pip install git+https://github.com/YOUR_USERNAME/salene.git
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text() if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [
        line.strip() 
        for line in requirements_path.read_text().splitlines() 
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="salene",
    version="2.0.0",
    author="SALENE Team",
    author_email="salene@example.com",
    description="Neural Consciousness Agent with Physiological Grounding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Optimiz0r/Salene",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "vision": ["opencv-python>=4.5.0", "pillow>=8.0.0"],
        "voice": ["SpeechRecognition>=3.8.0", "pyaudio>=0.2.11", "faster-whisper>=0.10.0"],
        "platforms": ["python-telegram-bot>=20.0", "discord.py>=2.3.0", "slack-sdk>=3.21.0"],
        "memory": ["sentence-transformers>=2.2.0", "chromadb>=0.4.0"],
        "dev": ["pytest>=7.0.0", "pytest-asyncio>=0.20.0", "black", "ruff"],
    },
    entry_points={
        "console_scripts": [
            "salene=salene:main",
        ],
    },
    include_package_data=True,
    package_data={
        "salene": [
            "config/*.yaml",
            "skins/*.yaml",
        ],
    },
)
