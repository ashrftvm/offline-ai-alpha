
# Offline AI Assistant
This guide will help you set up the prerequisites for running the Offline AI Assistant in your laptop or devices.

## Prerequisites
- Ensure you have Python (3.13+) installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- Make sure you have `pip` (Python's package installer) installed. It usually comes bundled with Python.

## Step 1: Install `venv` Module
Install python3-venv module if you haven't already.

In Ubuntu/Debian-based systems, run:
```bash
sudo apt-get install python3-venv
```

In MacOS, `venv` is included with the Python installation.
In Windows, `venv` is included with the Python installation.

## Step 2: Create a Virtual Environment
1. Open a terminal or command prompt.
2. Navigate to the directory where you want to create your project.
3. Run the following command to create a virtual environment:
   ```bash
   python3.13 -m venv gemma-assistant
   ```
   Replace `gemma-assistant` with your desired environment name.
4. This will create a directory named `gemma-assistant` (or your chosen name) containing the virtual environment.

## Step 4: Activate the Virtual Environment
- On Windows:
  ```bash
  gemma-assistant\Scripts\activate
  ```
- On macOS and Linux:
  ```bash
  source gemma-assistant/bin/activate
  ```
Once activated, your terminal prompt will change to indicate that you are now working inside the virtual environment.

## Step 5: Install Packages
You can now install packages using `pip` without affecting your global Python installation. For example:
```bash
pip install -r requirements.txt
```

then run the following command to get the ui.
```bash
python3.13 assistant.py
```