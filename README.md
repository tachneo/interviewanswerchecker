# Advanced Interview Evaluation Tool

A professional GUI-based tool built with Python and Tkinter to evaluate candidate responses during interviews. This tool leverages the Gemini API for generating detailed evaluations and provides a certificate-style report card for candidates.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Building the Executable](#building-the-executable)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Advanced Interview Evaluation Tool is designed to streamline the candidate assessment process during interviews. It presents a two-pane interface where one side is dedicated to inputting interview questions and candidate answers, and the other displays a score card and detailed evaluation report. Additionally, a minimal certificate-style report card can be generated with key evaluation information.

---

## Features

- **Intuitive Interface:** User-friendly GUI built with Tkinter and Ttk.
- **Detailed Evaluation:** Provides numeric scores, recommendations (Pass/Fail), and an in-depth analysis.
- **Certificate Generation:** Automatically creates a minimal certificate-style report card.
- **Visual Score Chart:** Generates a dynamic bar chart visualization using Matplotlib.
- **Export Functionality:** Export evaluations to a text file.
- **Configurable Options:** Toggle visibility of detailed analysis and score charts.

---

## Requirements

- Python 3.12 (or compatible)
- Tkinter (bundled with Python)
- [Matplotlib](https://matplotlib.org/)
- [PyInstaller](https://pyinstaller.org/) (for building executables)
- Gemini API client library (replace with your own API key)

---

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/advanced-interview-evaluation-tool.git
    cd advanced-interview-evaluation-tool
    ```

2. **(Optional) Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install the Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

   *Make sure to install any additional dependencies required by the Gemini API client.*

---

## Usage

1. **Run the Tool:**

    ```bash
    python main.py
    ```

2. **How It Works:**
   - Enter the candidate's name, interview question, and candidate's answer.
   - Click **Evaluate Answer** to generate an evaluation using the Gemini API.
   - The right pane displays a score card with a dynamic bar chart and detailed analysis.
   - Click **Generate Certificate** to view a minimal certificate-style report card.
   - Use **Export Evaluation** to save the evaluation details as a text file.

---

## Building the Executable

To build a standalone executable using PyInstaller or auto-py-to-exe, run a command similar to:

```bash
pyinstaller --noconfirm --onefile --windowed --exclude-module PyQt6 main.py
