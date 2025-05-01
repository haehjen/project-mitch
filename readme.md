# MITCH 1.0 - Event Horizon

## ?? Overview
MITCH is an event-driven modular assistant system with voice recognition, AI integration, and homelab control features. It’s designed to be extensible, hands-free, and resilient. Version 1.0 introduces a unified architecture, full voice-to-action workflow, and Proxmox VM control.

---

## ?? Features

### Core System
- Event-driven architecture using a central `EventBus`
- Modular separation of Listener, TTS, Interpreter, Dispatcher
- Systemd-managed user services for auto-start and fault tolerance

### Voice and Audio
- Microphone input using `speech_recognition`
- TTS using `pyttsx3` (British voice preferred)
- Custom `.asoundrc` for headset support (e.g. Jabra)

### AI Integration
- `triad.py` module powered by GPT-4o for tool invocation
- Supports GPT vision tools: Describe Room, Object Detection
- Uses Imgur API for temporary image hosting

### VM Control
- Integration with Proxmox API
- Can restart VMs, check VM status by voice
- JSONL logs of node/VM status to `/home/triad/mitch/data`

### Secrets & Security
- `.env` file (`mitchskeys.env`) for storing secrets securely
- `.gitignore` excludes all secrets, cache, logs, venv

---

## ?? Install Guide (Updated Bootstrap)

### Prerequisites
```bash
sudo apt install python3-venv python3-pyaudio portaudio19-dev ffmpeg
```

### Clone and Setup
```bash
git clone https://github.com/haehjen/project-mitch.git
cd project-mitch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Setup `mitchskeys.env`
Create a `.env` file named `mitchskeys.env` in the root:
```env
OPENAI_API_KEY=sk-...
PROXMOX_PASS=your_password_here
```
Ensure it’s listed in `.gitignore`:
```bash
echo 'mitchskeys.env' >> .gitignore
```

### Create systemd **user** services
Enable user lingering so services run at login:
```bash
sudo loginctl enable-linger triad
```

Create service files:

#### `~/.config/systemd/user/mitch-main.service`
```ini
[Unit]
Description=MITCH Main (Listener + Event System)
After=default.target

[Service]
ExecStart=/home/triad/mitch/venv/bin/python /home/triad/mitch/main.py
WorkingDirectory=/home/triad/mitch
Restart=always
User=triad

[Install]
WantedBy=default.target
```

#### `~/.config/systemd/user/mitch-dispatcher.service`
```ini
[Unit]
Description=MITCH Dispatcher (FastAPI server)
After=default.target

[Service]
ExecStart=/home/triad/mitch/venv/bin/python -m uvicorn core.dispatcher:app --host 0.0.0.0 --port 9000
WorkingDirectory=/home/triad/mitch
Restart=always
User=triad

[Install]
WantedBy=default.target
```

Then run:
```bash
systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user enable mitch-main.service mitch-dispatcher.service
systemctl --user start mitch-main.service mitch-dispatcher.service
```

Use `journalctl --user -u mitch-main.service -f` to monitor logs.

---

## ?? Notes for 1.1
- Add personality/memory persistence layer
- More resilient audio handling (fallback devices)
- Configurable VM descriptions and metadata
- Web-based dashboard?

---

MITCH 1.0 is alive. Let's go bigger.

