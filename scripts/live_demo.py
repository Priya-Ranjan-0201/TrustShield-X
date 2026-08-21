"""
TruthShield X — Live Autonomous Browser Demo & Interaction Harness
"""

import time
import sys
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def launch_demo():
    print("=" * 80, flush=True)
    print("TRUTHSHIELD X — LAUNCHING LIVE DEMO ON YOUR SCREEN...", flush=True)
    print("=" * 80, flush=True)

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception:
        driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 15)

    try:
        # Step 1: Open Login
        print("\n[1/5] Loading login portal (http://localhost:5180/login)...", flush=True)
        driver.get("http://localhost:5180/login")
        time.sleep(1.5)

        # Step 2: Authenticate Admin
        print("[2/5] Authenticating as SecOps Administrator...", flush=True)
        email_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_el.clear()
        email_el.send_keys("admin@truthshield.com")

        pass_el = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        pass_el.clear()
        pass_el.send_keys("AdminPassword123!")

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2.5)

        # Step 3: Test Scan
        print("\n[3/5] Navigating to Unified Threat Scanner (/scan)...", flush=True)
        driver.get("http://localhost:5180/scan")
        time.sleep(1.5)

        url_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form input")))
        url_input.clear()
        url_input.send_keys("http://nios-ac.in")
        driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(3.5)

        # Step 4: Threat Intelligence Fabric
        print("\n[4/5] Navigating to Threat Intelligence Fabric (/threat-intelligence-center)...", flush=True)
        driver.get("http://localhost:5180/threat-intelligence-center")
        time.sleep(2.5)

        # Step 5: Early Warning & Hunting
        print("\n[5/5] Navigating to Early Warning & Hunting (/threat-intelligence-command)...", flush=True)
        driver.get("http://localhost:5180/threat-intelligence-command")
        time.sleep(2.5)

        driver.get("http://localhost:5180/dashboard")
        print("\n" + "=" * 80, flush=True)
        print("DEMO COMPLETE — BROWSER READY FOR INTERACTIVE USE!", flush=True)
        print("=" * 80, flush=True)
        time.sleep(60)

    except Exception as exc:
        print(f"Demo info: {exc}", flush=True)


if __name__ == "__main__":
    launch_demo()
