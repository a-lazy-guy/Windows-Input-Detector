# Windows-Input-Detector

> [flow-state](https://github.com/Cai643/flow-state) 的衍生项目 | A derivative project of [flow-state](https://github.com/Cai643/flow-state)

[中文](#中文) | [English](#english)

---

## 中文

### 简介

本项目是 [flow-state](https://github.com/Cai643/flow-state) 的轻量级衍生版本，专注于 Windows 平台的输入事件检测。它提供了一个简洁的 Python 程序，用于实时追踪用户的键盘输入、鼠标操作以及当前活动窗口的焦点变化。

### 功能特性

- **🖱️ 鼠标追踪**：实时监控鼠标移动、点击事件，记录坐标位置和移动距离
- **⌨️ 键盘追踪**：捕获键盘按下和释放事件，支持常规按键和小键盘
- **🪟 窗口焦点追踪**：检测当前活动窗口的切换，获取窗口标题和进程信息
- **⚡ 实时输出**：所有事件实时打印到控制台，便于调试和观察
- **🔧 模块化设计**：各个检测器独立封装，易于扩展和维护

### 技术栈

- `pynput` - 跨平台输入监听库
- `pywin32` - Windows API 接口
- `psutil` - 进程信息获取

### 快速开始

```bash
# 安装依赖
pip install pynput pywin32 psutil

# 运行程序
python main.py
```

### 项目结构

```
.
├── main.py          # 主程序入口，协调各检测器
├── keyboard.py      # 键盘事件检测器
├── mouse.py         # 鼠标事件检测器
├── focus.py         # 窗口焦点检测器
└── README.md        # 项目说明文档
```

**注**：项目还包含 `original.py` 文件，作为项目原型（完整的单文件实现版本）。

### 使用说明

运行 `main.py` 后，程序将开始监听：
- 鼠标移动和点击
- 键盘按键
- 窗口焦点变化

按 `Ctrl+C` 可安全退出程序。

---

## English

### Introduction

This project is a lightweight derivative of [flow-state](https://github.com/Cai643/flow-state), focusing on input event detection on the Windows platform. It provides a concise Python program for real-time tracking of keyboard input, mouse operations, and active window focus changes.

### Features

- **🖱️ Mouse Tracking**: Real-time monitoring of mouse movements and click events, recording coordinates and travel distance
- **⌨️ Keyboard Tracking**: Captures key press and release events, supports standard keys and numpad
- **🪟 Window Focus Tracking**: Detects active window switches, retrieves window titles and process information
- **⚡ Real-time Output**: All events are printed to the console in real-time for debugging and observation
- **🔧 Modular Design**: Each detector is independently encapsulated for easy extension and maintenance

### Tech Stack

- `pynput` - Cross-platform input monitoring library
- `pywin32` - Windows API interface
- `psutil` - Process information retrieval

### Quick Start

```bash
# Install dependencies
pip install pynput pywin32 psutil

# Run the program
python main.py
```

### Project Structure

```
.
├── main.py          # Main entry point, coordinates all detectors
├── keyboard.py      # Keyboard event detector
├── mouse.py         # Mouse event detector
├── focus.py         # Window focus detector
└── README.md        # Project documentation
```

**Note**：The project also includes an `original.py` file, which serves as the project prototype (complete single-file implementation).

### Usage

After running `main.py`, the program will start listening for:
- Mouse movements and clicks
- Keyboard keystrokes
- Window focus changes

Press `Ctrl+C` to safely exit the program.

---

## 许可证 / License

Apache-2.0 License
