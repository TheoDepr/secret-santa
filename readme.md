# 🎅 Secret Santa Pair Generator

A festive web application built with Streamlit that helps organize Secret Santa gift exchanges by generating random pairs while respecting pairing constraints.

## 🎄 Features

- Simple and intuitive interface
- Add multiple participants
- Set pairing constraints (prevent specific pairs from being matched)
- Generates random pairs while ensuring:
  - No one gets themselves
  - All constraints are respected
  - Creates a complete circle of gift-giving
- Festive UI with Christmas themed styling

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository

2. Install required packages:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install streamlit numpy
    ```

3. Run the application:
    ```bash
    streamlit run app.py
    ```

