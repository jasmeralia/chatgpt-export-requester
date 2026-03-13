import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("CLAUDE_BASE_URL", "https://claude.ai")
PROFILE_PATH = os.environ.get("PROFILE_PATH", "/app/claude-profile")
SCREENSHOT_DIR = Path(os.environ.get("SCREENSHOT_DIR", "/app/screenshots"))
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            PROFILE_PATH,
            headless=False,
            viewport={"width": 1600, "height": 1200},
        )
        page = context.new_page()
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.screenshot(path=str(SCREENSHOT_DIR / "claude-bootstrap-opened.png"), full_page=True)

        print("")
        print("Bootstrap mode is running.")
        print("Log into Claude in the opened browser window if needed.")
        print("Once you can access the app normally, close the browser window.")
        print("The persisted profile will remain in /app/claude-profile.")
        print("")

        page.wait_for_timeout(60000 * 30)
        context.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
