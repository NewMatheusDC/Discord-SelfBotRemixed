# Discord SelfBot Remix

This is a remixed version of the original [Discord-SelfBot](https://github.com/AstraaDev/Discord-SelfBot) by AstraaDev, with additional features and improvements while maintaining the core functionality.

## Features

- **Enhanced Command System**: All original commands plus new additions
- **Improved UI**: Better console display and organization
- **Mobile Support**: Works on Termux (Android) and traditional PCs
- **Advanced Automation**: More robust autoreply and logging features
- **Security**: Better permission handling and error management

## Installation

### On PC (Windows/Linux/macOS)

1. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/)
2. **Clone the repository**:
   ```bash
   git clone https://github.com/NewMatheusDC/selfbot-remix.git
   cd selfbot-remix
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the bot**:
   - Edit `YOUR_TOKEN(main.py` with your token and settings
5. **Run the bot**:
   ```bash
   python main.py
   ```

### On Mobile (Termux - Android)

1. **Install Termux** from [F-Droid](https://f-droid.org/en/packages/com.termux/)
2. **Run these commands**:
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   git clone https://github.com/yourusername/selfbot-remix.git
   cd selfbot-remix
   pip install -r requirements.txt
   ```
3. **Configure the bot**:
   - Edit `config/config.json` using nano:
     ```bash
     nano config/config.json
     ```
4. **Run the bot**:
   ```bash
   python main.py
   ```

## Configuration

Edit `config/config.json` with your preferred settings:

```json
{
    "prefix": ".",
    "remote-users": [],
    "autoreply": {
        "messages": ["Hello!", "I'm busy right now"],
        "channels": [],
        "users": []
    },
    "afk": {
        "enabled": false,
        "message": "I'm AFK right now"
    },
    "copycat": {
        "users": []
    },
    "autoreact": {
        "enabled": false,
        "targets": [],
        "blacklist": [],
        "react_to_own": false
    },
    "autolog": {
        "enabled": false,
        "log_pairs": []
    }
}
```

## Usage

Start the bot and use commands with your prefix (default is `.`). For a full list of commands, type `.help` in any Discord channel where the bot is active.

## Credits

This project is based on the original work by [AstraaDev](https://github.com/AstraaDev/Discord-SelfBot). All credit for the core functionality goes to them.

## License

MIT License - Same as the original project

## Warning

Using selfbots may violate Discord's Terms of Service. Use at your own risk. This project is for educational purposes only.
