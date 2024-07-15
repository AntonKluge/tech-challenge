
# Installation Requirements

This page covers all the steps to install the required software for backend, frontend and production.

## Docker

Docker is used to containerize the code for production which makes it easier to install and to deploy it.

#### For MacOS

1. **Download Docker Desktop:**
   Visit the [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop) page and download the installer.

2. **Install Docker Desktop:**
    - Open the downloaded `.dmg` file.
    - Drag the Docker icon to the Applications folder.
    - Open Docker from the Applications folder.

3. **Verify Installation:**
   Open a terminal and run:

   ```bash
   docker --version
   docker-compose --version
   ```

#### For Linux (Debian/Ubuntu)

1. **Update Existing Packages:**
   ```bash
   sudo apt update
   sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
   ```

2. **Add Docker’s Official GPG Key:**
   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

3. **Set Up the Stable Repository:**
   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

4. **Install Docker Engine:**
   ```bash
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io
   ```

5. **Verify Installation:**
   ```bash
   sudo systemctl status docker
   docker --version
   docker-compose --version
   ```

6. **Optional: Manage Docker as a Non-Root User:**
   ```bash
   sudo groupadd docker
   sudo usermod -aG docker $USER
   newgrp docker
   ```

   Log out and log back in for the changes to take effect.

Now you should have Docker installed and ready to use on your system.

## Python

The backend is written in Python. If you want to develop the application further, it needs to be installed on your 
device. You need Python 3.12 or later.

**For MacOS:**

```bash
brew install python
```

**For Linux (Debian/Ubuntu):**

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

Verify the installation:

```bash
python3 --version
pip3 --version
```

## ChromeDriver

ChromeDriver is required for browser automation, and you will need it installed when running the code locally.
Install ChromeDriver using the following commands:

**For MacOS:**

```bash
brew install chromedriver
```

**For Linux (Debian/Ubuntu):**

```bash
sudo apt-get install -y chromium-chromedriver
```

Verify the installation:

```bash
chromedriver --version
```

## Poetry

Poetry is a dependency management tool for Python. Install Poetry with the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add Poetry to your PATH by updating your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then, apply the changes:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

Verify the installation:

```bash
poetry --version
```
