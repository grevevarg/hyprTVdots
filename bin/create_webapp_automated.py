#!/usr/bin/python3

from os.path import realpath
import os
from pathlib import Path
import requests
import argparse
import shutil
import subprocess
import sys

HOMEDIR = os.getenv('HOME')

APPLICATIONDIR = Path(HOMEDIR) / ".local/share/applications/"
ICON_DIR = Path(HOMEDIR) / ".local/share/applications/icons"

def browser_in_path(browser: str) -> bool:
    try:
        subprocess.run(['which', browser], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

#app icon thing is ugly temporary permanent hack until i write out the proper way to do str || None
class DesktopFileData:
    def __init__(self, app_name: str, app_url: str, browser: str, app_icon=None) -> None:
        #variables not directly tied to desktop spec
        self.browser = browser
        self.appicon = app_icon
        self.app_url = app_url
        
        # variables with values for .desktop file
        self.version = "1.5"
        self.type = "Application"
        self.app_name = app_name
        self.comment = f"Chromium based PWA for {self.app_name}"
        self.terminal_exec = "false"
        self.appicon_path = self.get_icon()
        self.weak_sanitize_appname = self.sanitize_filename(self.app_name)
        # really brittle, if url contains a path to a tv endpoint then embed different User-Agent to hopefully get proper functionality
        if "/tv" in self.app_url:
            self.exec_str = f'setsid {browser} --user-data-dir="{os.getenv("XDG_CACHE_HOME") if os.getenv("XDG_CACHE_HOME") else Path(HOMEDIR / ".cache")}/{self.weak_sanitize_appname}" --no-default-browser-check --app="{self.app_url}" --user-agent "Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0" &'
        else:
            self.exec_str = f'setsid {browser} --user-data-dir="{os.getenv("XDG_CACHE_HOME") if os.getenv("XDG_CACHE_HOME") else Path(HOMEDIR / ".cache")}/{self.weak_sanitize_appname}" --no-default-browser-check --app="{self.app_url}"'
    
    def sanitize_filename(self, name: str):
        return "".join(c for c in name.casefold() if c.isalnum() or c in '-_')

    def get_icon(self):
        
        icon_path = ICON_DIR / f"{self.weak_sanitize_appname}.png"
        
        if Path(self.appicon).exists() and self.appicon != None:
            shutil.copy(Path(self.appicon), icon_path)
            return realpath(icon_path)
        if not self.appicon == None:
            response = requests.get(self.appicon)
            if response.status_code == 200:
                icon_path.write_bytes(response.content)
            return str(icon_path.resolve())
        response = requests.get(f'https://www.google.com/s2/favicons?sz=64&domain={self.weak_sanitize_appname}')
        if response.status_code == 200:
            icon_path.write_bytes(response.content)
            return str(icon_path.resolve())
        # this is the part where we give up and just return none
        return None

    def write_desktop_file(self):
        desktop_file_path = Path(APPLICATIONDIR / f"{self.weak_sanitize_appname}.desktop")
        file_contents = f"""
        [Desktop Entry]
        Type={self.type}
        Version={self.version}
        Name={self.app_name}
        Comment={self.comment}
        Icon={self.appicon_path}
        Terminal={self.terminal_exec}
        Exec={self.exec_str}
        """

        with open(desktop_file_path, 'w') as f:
            f.write(file_contents)

        return

def main():
    parser = argparse.ArgumentParser(
        prog="PWADesktopMaker",
        description="Creates a PWA based on passed in arguments. Supports Helium, Brave and Chromium as browsers"
    )
    #app_name: str, app_icon: str, app_url: str
    parser.add_argument('--app-name', help="The name of the application", required=True)
    parser.add_argument('--app-icon', help="Filesystem path or URL to an icon to be used in the desktop file. Optional")
    parser.add_argument("--app-url", help="The URL to set up the webapp for", required=True)
    
    args = parser.parse_args()

    APPLICATIONDIR.mkdir(parents=True, exist_ok=True)
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    
    browsers = ['helium-browser', 'brave', 'chromium']
    available = [b for b in browsers if browser_in_path(b)]
    if not available:
        raise RuntimeError("No compatible browser found in PATH. Supported browsers are helium-browser, brave and chromium")
    browser_to_use = available[0]

    desktop_info = DesktopFileData(app_name=args.app_name, app_icon=args.app_icon, app_url=args.app_url, browser=browser_to_use)

    try:
        desktop_info.write_desktop_file()
        sys.exit(0)
    except Exception as e:
        print(f"Error writing desktop file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
