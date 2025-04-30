
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
