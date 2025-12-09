# GLR75 Voting Bot

Automated voting script for glr75.nl/top75 that votes for tracks `trk-278` and `trk-022` with hCaptcha support.

## Features

- Generates random Dutch names for voting
- Creates email addresses in format: `XXXXXX@glr.nl` (6 random digits)
- Automatically votes for both tracks: `trk-278` and `trk-022`
- Opens browser for hCaptcha solving (click-based challenges)
- GUI notification when to continue after solving CAPTCHA
- Automatic form filling and submission
- Continuous voting loop - automatically restarts after each submission

## Installation

### macOS

#### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 2. Install ChromeDriver

```bash
brew install chromedriver
```

If you don't have Homebrew, install it first from [brew.sh](https://brew.sh), or download ChromeDriver manually:

1. Visit: <https://chromedriver.chromium.org/downloads>
2. Download version matching your Chrome browser version (check in Chrome: Settings → About Chrome)
3. Extract the file and move to `/usr/local/bin/`:
   ```bash
   sudo mv chromedriver /usr/local/bin/
   sudo chmod +x /usr/local/bin/chromedriver
   ```

### Windows

#### 1. Install Python dependencies

Open Command Prompt or PowerShell and run:

```bash
pip install -r requirements.txt
```

#### 2. Install ChromeDriver

**Option A: Using Chocolatey (recommended)**

If you have [Chocolatey](https://chocolatey.org/install) installed:

```bash
choco install chromedriver
```

**Option B: Manual Installation**

1. Check your Chrome version: Open Chrome → Three dots menu → Help → About Google Chrome
2. Visit: <https://chromedriver.chromium.org/downloads>
3. Download ChromeDriver matching your Chrome version (e.g., ChromeDriver 120.x for Chrome 120.x)
4. Extract the `chromedriver.exe` file
5. Add to PATH:
   - Move `chromedriver.exe` to `C:\Windows\System32\`
   - OR add the folder containing `chromedriver.exe` to your system PATH

**To add to PATH manually:**

1. Right-click "This PC" → Properties → Advanced system settings
2. Click "Environment Variables"
3. Under "System variables", find and select "Path", then click "Edit"
4. Click "New" and add the folder path containing `chromedriver.exe`
5. Click OK on all windows

## Usage

### macOS

Open Terminal and navigate to the project folder, then run:

```bash
python vote_bot.py
```

### Windows

Open Command Prompt or PowerShell, navigate to the project folder, then run:

```bash
python vote_bot.py
```

### How it works

The script will continuously vote in a loop:

1. Generate a random name and email
2. Open Chrome browser with the voting page
3. Automatically fill in the form fields and select both tracks
4. Wait for you to solve the hCaptcha (click-based)
5. Show a popup - click "CAPTCHA Solved - Continue" when done
6. Automatically submit the vote
7. Close browser and immediately start over with vote #2, #3, etc.

**To stop the bot:** Press `Ctrl+C` in the terminal

## Requirements

- Python 3.7+
- Google Chrome browser
- ChromeDriver (matching your Chrome version)
- Internet connection
- Tkinter (usually included with Python)

## Notes

- The script opens a visible browser window - this is necessary for hCaptcha
- You must manually solve the click-based hCaptcha challenge
- After solving, click the popup button to continue
- The browser will close automatically after 5 seconds
- Make sure you have permission to automate voting on this website
