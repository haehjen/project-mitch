
# MITCH Bootstrap Guide

Maintained by House – Diagnostician of Root Causes and Builder of Digital Assistants

This guide documents the intentional rebuild of MITCH from the ground up. Each step is followed by a snapshot recommendation to allow for safe, incremental development. MITCH lives at /home/triad/mitch/ on a clean Ubuntu 24.04 LTS VM.

---

## Step 1 – Create Project Folder & Initialize Git

Directory Layout:
/home/triad/mitch/

Commands:
# As user 'triad'
mkdir ~/mitch
cd ~/mitch
git init

This creates a Git repository at /home/triad/mitch/.git

Snapshot Recommendation:
mitch_step1_git_initialized

---

## Step 2 – Set Up Virtual Environment

Commands:
# Still inside /home/triad/mitch
sudo apt install -y python3.12-venv     # Or python3-venv depending on version
python3 -m venv venv
source venv/bin/activate

Your prompt will change to show the venv is active: (venv) triad@mitch:~/mitch$

Notes:
- Never commit the venv/ folder to Git.
- We’ll track dependencies later with requirements.txt.

Snapshot Recommendation:
mitch_step2_venv_created

---

## Step 3 – Add .gitignore, README, and First Commit

This step creates Git metadata, prepares project documentation, and excludes unnecessary files from version control.

Files Created:
- .gitignore – Prevents tracking of venv, logs, compiled files, and env vars
- README.md – Starts project description

Commands:
# Inside /home/triad/mitch

# Create .gitignore
echo "venv/
__pycache__/
*.pyc
*.log
.env" > .gitignore

# Create README
echo "# MITCH

Self-hosted AI assistant managed by House, rebuilt with intention, precision, and proper documentation.
" > README.md

# Configure Git identity (one-time setup)
git config --global user.name "House"
git config --global user.email "haehjen@gmail.com"

# Stage and commit files
git add .
git commit -m "Step 3: Added .gitignore and README"

Snapshot Recommendation:
mitch_step3_commit_complete

---

## Step 4 – Link Local Repo to GitHub

The local Git repository is pushed to GitHub to allow remote versioning, collaboration, and integration with Echo.

Remote Repo:
https://github.com/haehjen/project-mitch.git

Commands to run (inside /home/triad/mitch):

1. Add the remote repo:
git remote add origin https://github.com/haehjen/project-mitch.git

2. Rename the branch to match GitHub default:
git branch -M main

3. Push to GitHub:
git push -u origin main

When prompted:
- Username: haehjen
- Password: paste your GitHub Personal Access Token (PAT)

Snapshot Recommendation:
mitch_step4_pushed_to_github


---

## Step 5 – Install Core Python Dependencies

This step installs the essential packages for MITCH’s audio, HTTP, and service functionality inside the virtual environment. These are tracked with requirements.txt.

Required system dependencies (to allow building pyaudio):

sudo apt update
sudo apt install -y portaudio19-dev python3-dev build-essential

Python package install (inside the venv):

source ~/mitch/venv/bin/activate
pip install pyaudio pyttsx3 requests fastapi uvicorn python-dotenv

Freeze versions to file:

pip freeze > requirements.txt

Commit to Git:

git add requirements.txt
git commit -m "Step 5: Installed dependencies and locked versions"
git push

Snapshot Recommendation:
mitch_step5_requirements_installed


---

## Step 6 – Create Project Folder Structure

This step defines the base folder layout for MITCH’s architecture.

Recommended structure:
/home/triad/mitch/
├── core/            # System logic: dispatcher, recognizer, etc.
├── modules/         # Optional features: TTS, weather, emotion, etc.
├── data/            # Configs, logs, models, assets
├── tests/           # Unit/integration tests
├── bootstrap.md     # Build and deployment log
├── requirements.txt
└── README.md

Commands to create:

cd ~/mitch
mkdir core modules data tests
touch core/__init__.py
touch modules/__init__.py
touch data/.keep
touch tests/__init__.py

Snapshot Recommendation:
mitch_step6_project_structure_created




---

## Step 7 – USB Audio Passthrough and I/O Verification

This step enables and validates both audio output and microphone input via the Jabra Evolve 65 USB headset.

### Host-Level Setup

1. Shut down the MITCH VM in Proxmox.
2. In the Proxmox UI:
   - Go to Hardware → Add → USB Device
   - Select the Jabra Evolve 65
   - Enable "Use USB3" if available
3. Boot the VM.

### Inside the VM

1. Confirm the device is visible:
   lsusb

2. Install ALSA tools:
   sudo apt update
   sudo apt install -y alsa-utils

3. Verify kernel modules:
   lsmod | grep snd_usb_audio

4. Check card detection:
   cat /proc/asound/cards

5. Create ALSA config:
   nano ~/.asoundrc

Paste this:

pcm.jabra {
    type hw
    card 0
    device 0
}

ctl.jabra {
    type hw
    card 0
}

pcm.!default jabra
ctl.!default jabra

6. Add user to audio group:
   sudo usermod -aG audio triad

7. Log out or reboot.

8. Test speaker output:
   speaker-test -c2 -t wav

9. Test microphone input:
   arecord -D plughw:0,0 -f cd -d 5 test.wav
   aplay test.wav

Snapshot Recommendation:
mitch_step7_audio_io_verified


---

## Step 8 – USB Webcam Passthrough and Detection

This step adds basic vision to MITCH by passing through a webcam device to the VM.

### Host-Level Setup

1. Shut down the MITCH VM in Proxmox.
2. In the Proxmox UI:
   - Go to Hardware → Add → USB Device
   - Select your USB webcam
   - Enable "Use USB3" if available
3. Boot the VM.

### Inside the VM

1. SSH into the VM:
   cd ~/mitch

2. Confirm the webcam is detected:
   lsusb
   v4l2-ctl --list-devices (after installing v4l-utils)

Next: capture a test frame or stream.

Snapshot Recommendation:
mitch_step8_webcam_attached
