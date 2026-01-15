![App Icon](images/patapata_clock.png)

# PataPata clock
[![License: CC BY-NC-ND 4.0](https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-nd/4.0/)   
[日本語版を見る](README.md) | [English Version](README_EN.md)


A **Python application** that combines a flip-style digital clock with a music player.

This application uses **pygame**.  
Therefore, installation of pygame is required beforehand.

---

## Features

- Digital clock with flip animation
- Window resizing support
- MP3 music playback function  
  (Play / Pause / Next / Previous)
- Easily change music by simply putting MP3 files into the `music` folder

---

## Requirements

- Python **3.9 or higher**
- pygame **2.6 or higher**

---

## Tested Environments

- Raspberry Pi 5  
- Mac mini (Apple Silicon / macOS Tahoe 26.1)

---

## Installation

### Windows

1. Install **Python 3** from the [Official Python Website](https://www.python.org/).  
   *Note: Please check **"Add Python to PATH"** during installation.*

2. Open Command Prompt and run the following command:
```bash
python -m pip install pygame
```
3. Navigate to the folder containing the files and run the application. (If located in the Downloads folder)
```bash
cd /d %USERPROFILE%\Downloads\PataPata_clock
python PataPata_clock.py
```
### mac
1. Install **Python 3** from the [Official Python Website](https://www.python.org/).  

2. Open Terminal and run the following commands (If located in the Downloads folder)
```bash
pip3 install pygame
cd ~/Downloads/PataPata_clock
python3 PataPata_clock.py
```

### Linux (Raspberry Pi)
1. Install **Python 3** from the [Official Python Website](https://www.python.org/).

2. Open Terminal and run the following commands
```bash
sudo apt update
sudo apt upgrade
sudo apt install -y python3-pygame
```

3. Navigate to the folder containing the files and run the application (If located on the Desktop)
```bash
cd ~/Desktop/PataPata_clock
python3 PataPata_clock.py
```
### Usage
1. Run the app using the commands above, and the window will appear.
2. You can control the music using the playback buttons at the bottom of the screen.
3. Please place the MP3 files you want to play in the music folder.

## Bug Reports
Please report any bugs in the comments section of the YouTube video.

## License
This work is licensed under a
Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
(CC BY-NC-ND 4.0) license.

© 2026 maronnulab

### Allowed
- Use or introduction on YouTube, etc.
- Personal use
- Modification of source code for personal use

### Prohibited
- Commercial use or sale
- Publication of modified versions
- Redistribution (whether original or modified)