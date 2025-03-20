# Aldente-Installer
# AlDente Installer for macOS

A Python script to automate the download and installation of **AlDente**, a macOS app for managing battery charging limits. This script downloads the `.dmg` file from the official GitHub release, mounts it, copies the `AlDente.app` bundle to `/Applications`, and cleans up afterward.

---

## Features

- **Automated Installation**: Downloads and installs AlDente with a single command.
- **macOS Only**: Designed specifically for macOS.
- **Error Handling**: Provides detailed error messages for troubleshooting.
- **Cleanup**: Removes the downloaded `.dmg` file after installation.

---

## Prerequisites

- **Python 3.x**: Ensure Python 3 is installed on your system.
- **`requests` Library**: Required for downloading the `.dmg` file.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/aldente-installer.git
   cd aldente-installer
