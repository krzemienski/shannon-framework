#!/usr/bin/env python3
"""Test Dashboard Event Reception with Playwright.

This script:
1. Starts the Shannon server
2. Starts the dashboard dev server
3. Opens dashboard in Playwright browser
4. Runs 'shannon do "create test.py"' with --dashboard flag
5. Verifies events are received in the dashboard
"""

import asyncio
import subprocess
import time
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# Configuration
SERVER_PORT = 8000
DASHBOARD_PORT = 5173
SERVER_URL = f"http://localhost:{SERVER_PORT}"
DASHBOARD_URL = f"http://localhost:{DASHBOARD_PORT}"
TEST_TIMEOUT = 30000  # 30 seconds

async def start_server():
    """Start the Shannon server."""
    print("Starting Shannon server...")
    server_process = subprocess.Popen(
        ["poetry", "run", "python", "run_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for server to be ready
    await asyncio.sleep(3)

    # Check if server is running
    try:
        import requests
        response = requests.get(f"{SERVER_URL}/health", timeout=2)
        if response.status_code == 200:
            print(f"✓ Server started successfully on {SERVER_URL}")
            return server_process
    except Exception as e:
        print(f"✗ Server health check failed: {e}")
        server_process.terminate()
        raise

    return server_process

async def start_dashboard():
    """Start the dashboard dev server."""
    print("Starting dashboard dev server...")
    dashboard_dir = Path(__file__).parent / "dashboard"

    dashboard_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=dashboard_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for dashboard to be ready
    await asyncio.sleep(5)

    print(f"✓ Dashboard started on {DASHBOARD_URL}")
    return dashboard_process

async def run_shannon_command():
    """Run shannon do command with --dashboard flag."""
    print("\nRunning: shannon do 'create test.py' --dashboard")

    command_process = subprocess.Popen(
        ["poetry", "run", "shannon", "do", "create test.py", "--dashboard"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return command_process

async def test_dashboard_events():
    """Test dashboard event reception using Playwright."""
    server_process = None
    dashboard_process = None
    command_process = None

    try:
        # Start server and dashboard
        server_process = await start_server()
        dashboard_process = await start_dashboard()

        # Launch Playwright
        async with async_playwright() as p:
            print("\nLaunching Playwright browser...")
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to dashboard
            print(f"Navigating to {DASHBOARD_URL}...")
            await page.goto(DASHBOARD_URL)
            await page.wait_for_load_state("networkidle")

            # Wait for React app to mount
            await asyncio.sleep(2)

            # Take initial screenshot
            await page.screenshot(path="dashboard_before_command.png")
            print("✓ Dashboard loaded - screenshot saved: dashboard_before_command.png")

            # Get initial event count
            initial_count_element = await page.query_selector('[data-testid="event-count"]')
            if initial_count_element:
                initial_count_text = await initial_count_element.text_content()
                print(f"Initial event count: {initial_count_text}")
            else:
                print("Warning: Could not find event count element")
                initial_count_text = "0"

            # Start the shannon command
            command_process = await run_shannon_command()

            # Wait for events to arrive and count to update
            print("\nWaiting for events to arrive...")
            max_wait = 20  # 20 seconds
            wait_interval = 1
            events_received = False

            for i in range(max_wait):
                await asyncio.sleep(wait_interval)

                # Check event count
                count_element = await page.query_selector('[data-testid="event-count"]')
                if count_element:
                    count_text = await count_element.text_content()
                    print(f"Event count at {i+1}s: {count_text}")

                    # Check if count increased
                    if count_text != initial_count_text and count_text != "0":
                        events_received = True
                        print(f"✓ Events received! Count changed from {initial_count_text} to {count_text}")
                        break
                else:
                    print(f"No event count element found at {i+1}s")

            # Take final screenshot
            await page.screenshot(path="dashboard_after_command.png")
            print("✓ Final screenshot saved: dashboard_after_command.png")

            # Get event list
            event_items = await page.query_selector_all('[data-testid="event-item"]')
            print(f"\nEvent items found: {len(event_items)}")

            if event_items:
                print("\nEvent types received:")
                for i, item in enumerate(event_items[:5]):  # Show first 5
                    event_text = await item.text_content()
                    print(f"  {i+1}. {event_text[:100]}")

            # Final result
            print("\n" + "="*60)
            if events_received:
                print("✓ TEST PASSED: Dashboard successfully received events!")
                print(f"  Initial count: {initial_count_text}")
                print(f"  Final count: {count_text}")
                print(f"  Events visible: {len(event_items)}")
                result = 0
            else:
                print("✗ TEST FAILED: Dashboard did not receive events")
                print(f"  Count remained: {initial_count_text}")
                result = 1

            print("="*60)

            # Keep browser open for inspection
            print("\nBrowser will remain open for 10 seconds for inspection...")
            await asyncio.sleep(10)

            await browser.close()
            return result

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Cleanup
        print("\nCleaning up processes...")
        if command_process:
            command_process.terminate()
            try:
                command_process.wait(timeout=5)
            except:
                command_process.kill()

        if dashboard_process:
            dashboard_process.terminate()
            try:
                dashboard_process.wait(timeout=5)
            except:
                dashboard_process.kill()

        if server_process:
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except:
                server_process.kill()

        print("✓ Cleanup complete")

if __name__ == "__main__":
    print("="*60)
    print("Shannon Dashboard Event Reception Test")
    print("="*60)

    result = asyncio.run(test_dashboard_events())
    sys.exit(result)
