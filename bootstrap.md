
# MITCH Bootstrap Guide

**Maintained by House – Diagnostician of Root Causes and Builder of Digital Assistants**

This guide documents the intentional rebuild of MITCH from the ground up. Each step is followed by a snapshot recommendation to allow for safe, incremental development. MITCH lives at `/home/triad/mitch/` on a clean Ubuntu 24.04 LTS VM.

---

## ✅ Step 1 – Create Project Folder & Initialize Git

### 📁 Directory Layout
```
/home/triad/mitch/
```

### 🧪 Commands
```bash
# As user 'triad'
mkdir ~/mitch
cd ~/mitch
git init
```

> This creates a Git repository at `/home/triad/mitch/.git`

### 📸 Snapshot Recommendation:
> `mitch_step1_git_initialized`

---

## ✅ Step 2 – Set Up Virtual Environment

### 🧪 Commands
```bash
# Still inside /home/triad/mitch
sudo apt install -y python3.12-venv     # Or python3-venv depending on version
python3 -m venv venv
source venv/bin/activate
```

> Your prompt will change to show the venv is active: `(venv) triad@mitch:~/mitch$`

### 🧼 Notes
- Never commit the `venv/` folder to Git.
- We’ll track dependencies later with `requirements.txt`.

### 📸 Snapshot Recommendation:
> `mitch_step2_venv_created`

---

## ✅ Step 3 – Add .gitignore, README, and First Commit

This step creates Git metadata, prepares project documentation, and excludes unnecessary files from version control.

### 📄 Files Created
- `.gitignore` – Prevents tracking of venv, logs, compiled files, and env vars
- `README.md` – Starts project description

### ✏️ Commands
```bash
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
```

### 📸 Snapshot Recommendation:
> `mitch_step3_commit_complete`
