import os
import sys
import subprocess
from pathlib import Path

from art import LOGO

ROOT = Path(__file__).parent

MENU = """
Select a build to run:
  [1] Original  — course solution (requests + BeautifulSoup + Selenium)
  [2] Advanced  — refactored build (undetected-chromedriver, config, classes)
  [q] Quit
"""

clear = True
while True:
    if clear:
        os.system("cls" if os.name == "nt" else "clear")
        print(LOGO)
    clear = True

    print(MENU)
    choice = input("Your choice: ").strip().lower()

    if choice == "1":
        path = ROOT / "original" / "main.py"
        subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
        input("\nPress Enter to return to menu...")
    elif choice == "2":
        path = ROOT / "advanced" / "main.py"
        subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
        input("\nPress Enter to return to menu...")
    elif choice == "q":
        break
    else:
        print("Invalid choice. Try again.")
        clear = False
