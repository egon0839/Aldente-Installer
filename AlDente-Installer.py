import os
import requests
import subprocess
import time
import shutil

# Define emojis and symbols for better logging
CHECKMARK = "✅"
CROSSMARK = "❌"
INFO = "ℹ️"
DOWNLOAD = "📥"
INSTALL = "🔧"

def download_aldente_installer(url, filename):
    """
    Downloads the AlDente installer (.dmg) from the given URL.
    """
    installer_path = os.path.join(os.getcwd(), filename)
    
    print(f"{DOWNLOAD} [INFO] Downloading AlDente installer...")
    try:
        # Use a session to handle headers and cookies
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
        }
        response = session.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes

        # Write the installer to disk
        with open(installer_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"{CHECKMARK} [SUCCESS] Download complete.")
        return installer_path

    except requests.exceptions.RequestException as e:
        print(f"{CROSSMARK} [ERROR] Failed to download installer: {e}")
        return None

def mount_dmg(installer_path):
    """
    Mounts the AlDente .dmg file and returns the path to the mounted volume.
    """
    print(f"{INFO} [INFO] Mounting AlDente installer...")
    try:
        # Mount the DMG file
        subprocess.run(["hdiutil", "attach", installer_path], check=True)
        time.sleep(3)  # Wait for the volume to mount

        # Find the mounted volume
        result = subprocess.run(["hdiutil", "info"], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "/Volumes/AlDente" in line or "/Volumes/AlDentePro" in line:
                volume_path = line.split()[-1]
                print(f"{CHECKMARK} [SUCCESS] Mounted volume: {volume_path}")
                return volume_path

        print(f"{CROSSMARK} [ERROR] Failed to find mounted AlDente volume.")
        return None

    except subprocess.CalledProcessError as e:
        print(f"{CROSSMARK} [ERROR] Failed to mount DMG: {e}")
        return None

def copy_aldente_app(volume_path):
    """
    Copies the AlDente.app bundle from the mounted volume to /Applications.
    """
    print(f"{INFO} [INFO] Copying AlDente.app to /Applications...")
    try:
        # Locate the AlDente.app bundle
        app_path = os.path.join(volume_path, "AlDente.app")
        if not os.path.exists(app_path):
            print(f"{CROSSMARK} [ERROR] AlDente.app not found in {volume_path}.")
            return False

        # Remove existing AlDente.app in /Applications (if any)
        destination_path = "/Applications/AlDente.app"
        if os.path.exists(destination_path):
            print(f"{INFO} [INFO] Removing existing AlDente.app in /Applications...")
            shutil.rmtree(destination_path)

        # Copy the app bundle
        shutil.copytree(app_path, destination_path)
        print(f"{CHECKMARK} [SUCCESS] AlDente.app copied to /Applications.")
        return True

    except Exception as e:
        print(f"{CROSSMARK} [ERROR] Failed to copy AlDente.app: {e}")
        return False

def unmount_dmg(volume_path):
    """
    Unmounts the AlDente .dmg file.
    """
    print(f"{INFO} [INFO] Unmounting AlDente installer...")
    try:
        subprocess.run(["hdiutil", "detach", volume_path], check=True)
        print(f"{CHECKMARK} [SUCCESS] Unmounted volume: {volume_path}")
    except subprocess.CalledProcessError as e:
        print(f"{CROSSMARK} [ERROR] Failed to unmount DMG: {e}")

def main():
    # AlDente macOS installer URL (updated to the correct URL)
    url = "https://github.com/AppHouseKitchen/AlDente-Charge-Limiter/releases/download/1.31.3/AlDente.dmg"
    filename = "AlDente.dmg"

    # Step 1: Download the installer
    installer_path = download_aldente_installer(url, filename)
    if not installer_path:
        return

    # Step 2: Mount the DMG file
    volume_path = mount_dmg(installer_path)
    if not volume_path:
        return

    # Step 3: Copy AlDente.app to /Applications
    if not copy_aldente_app(volume_path):
        unmount_dmg(volume_path)  # Clean up before exiting
        return

    # Step 4: Unmount the DMG file
    unmount_dmg(volume_path)

    # Step 5: Clean up the installer
    os.remove(installer_path)
    print(f"{CHECKMARK} [INFO] Installer removed successfully.")

if __name__ == "__main__":
    # Ensure the script is running on macOS
    if os.uname().sysname != "Darwin":
        print(f"{CROSSMARK} [ERROR] This script only works on macOS.")
    else:
        main()