
# MITCH Bootstrap Guide

_Maintained by House – Diagnostician of Root Causes and Builder of Digital Assistants_

This guide documents the intentional rebuild of MITCH from the ground up. Each step is followed by a snapshot recommendation to allow for safe, incremental development. MITCH resides at `/home/triad/mitch/` on a clean Ubuntu 24.04 LTS VM.

---

## Step 1 – Create Project Folder & Initialize Git

**Directory Layout:** `/home/triad/mitch/`

**Commands:**
```bash
# As user 'triad'
mkdir ~/mitch
cd ~/mitch
git init
```
This creates a Git repository at `/home/triad/mitch/.git`.

**Snapshot Recommendation:** `mitch_step1_git_initialized`

---

## Step 2 – Set Up Virtual Environment

**Commands:**
```bash
# Still inside /home/triad/mitch
sudo apt install -y python3.12-venv  # Or python3-venv depending on version
python3 -m venv venv
source venv/bin/activate
```
Your prompt will change to show the virtual environment is active:

```bash
(venv) triad@mitch:~/mitch$
```

**Snapshot Recommendation:** `mitch_step2_venv_created`

---

## Step 3 – Add `.gitignore`, `README`, and First Commit

**Commands:**
```bash
echo "venv/" >> .gitignore
echo "# MITCH Project" > README.md
git add .gitignore README.md
git commit -m "Initial commit with .gitignore and README"
```

**Snapshot Recommendation:** `mitch_step3_initial_commit`

---

## Step 4 – Install Dependencies

**Commands:**
```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Install required packages
pip install pyttsx3 uvicorn fastapi
```
Ensure that all necessary packages are listed in `requirements.txt` for future reference:

```bash
pip freeze > requirements.txt
```

**Snapshot Recommendation:** `mitch_step4_dependencies_installed`

---

## Step 5 – Configure Audio Playback

To resolve audio playback issues, specify the correct audio device. Use `aplay -l` to list available devices and identify the appropriate card and device numbers.

```bash
aplay -l
```

If your device is listed as `card 1: J65 [Jabra Evolve 65], device 0: USB Audio [USB Audio]`, set the default audio device in your code or configuration to use `hw:1,0`.

**Snapshot Recommendation:** `mitch_step5_audio_configured`

---

## Step 6 – Set Up Systemd Services

To ensure MITCH components start automatically and recover from crashes, create systemd service files.

**Create `mitch-dispatcher.service`:**
```ini
[Unit]
Description=MITCH Dispatcher (FastAPI server)
After=network.target

[Service]
User=triad
WorkingDirectory=/home/triad/mitch
ExecStart=/home/triad/mitch/venv/bin/python -m uvicorn core.dispatcher:app --host 0.0.0.0 --port 9000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Create `mitch-main.service`:**
```ini
[Unit]
Description=MITCH Main (Listener + Event System)
After=network.target

[Service]
User=triad
WorkingDirectory=/home/triad/mitch
ExecStart=/home/triad/mitch/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Commands:**
```bash
# Copy service files to systemd directory
sudo cp mitch-*.service /etc/systemd/system/

# Reload systemd to recognize new services
sudo systemctl daemon-reload

# Enable services to start on boot
sudo systemctl enable mitch-dispatcher.service
sudo systemctl enable mitch-main.service

# Start services immediately
sudo systemctl start mitch-dispatcher.service
sudo systemctl start mitch-main.service
```

**Snapshot Recommendation:** `mitch_step6_services_configured`

---

## Step 7 – Verify Services

**Commands:**
```bash
# Check status of dispatcher service
systemctl status mitch-dispatcher.service

# Check status of main service
systemctl status mitch-main.service
```

Ensure both services are active and running without errors.

**Snapshot Recommendation:** `mitch_step7_services_verified`

---

## Step 8 – Test Voice Output

To test the text-to-speech functionality:
```bash
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Audio test'); engine.runAndWait()"
```

If you encounter errors related to audio devices, ensure that the correct device is specified, as detailed in Step 5.

**Snapshot Recommendation:** `mitch_step8_tts_tested`

---

## Step 9 – Test Voice Input

To test audio recording:
```bash
arecord -D plughw:1,0 -f cd -t wav -d 5 -r 48000 test.wav
aplay -D plughw:1,0 test.wav
```

Replace `plughw:1,0` with your device's appropriate card and device numbers.

**Snapshot Recommendation:** `mitch_step9_voice_input_tested`

---

## Step 10 – Finalize and Document

Ensure all configurations are documented, and the system is tested thoroughly. Commit all changes to the Git repository:

```bash
git add .
git commit -m "Finalize MITCH setup with systemd services and audio configuration"
```

**Snapshot Recommendation:** `mitch_step10_finalized`

---

This updated `bootstrap.md` should serve as a comprehensive guide to setting up and configuring the MITCH system from scratch.
