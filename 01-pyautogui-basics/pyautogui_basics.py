"""
Step: 1
Topic: PyAutoGUI basics (mouse, keyboard, fail-safe) + mss for fast screenshots
Resources: PyAutoGUI docs (pyautogui.readthedocs.io), mss docs (python-mss.readthedocs.io)
Summary: Core PyAutoGUI mouse/keyboard control plus a faster screenshot method needed for the Step 2 agent loop.
"""

import time
import pyautogui
import mss
import mss.tools


# ---------------------------------------------------------------------------
# SECTION 1: General functions - screen size and cursor position
# ---------------------------------------------------------------------------
def section_1_general_functions():
    width, height = pyautogui.size()
    print(f"Screen size: {width}x{height}")

    # position() reads the cursor's current XY, useful for logging what the
    # agent "sees" as its own state before it acts
    x, y = pyautogui.position()
    print(f"Current cursor position: ({x}, {y})")


# ---------------------------------------------------------------------------
# SECTION 2: Mouse functions
# ---------------------------------------------------------------------------
def section_2_mouse_functions():
    # XY origin (0, 0) is the TOP-LEFT of the screen, not bottom-left like
    # normal math coordinates. X grows right, Y grows down. Every coordinate
    # the agent produces later has to be interpreted with this in mind.

    # moveTo() takes absolute coordinates, duration is in seconds and makes
    # the move visible/debuggable instead of an instant jump
    pyautogui.moveTo(200, 200, duration=0.5)

    # click() clicks at the current position if no coordinates are given
    pyautogui.click()

    # doubleClick() is its own function rather than click(clicks=2), because
    # the OS treats double-click timing differently from two separate clicks
    pyautogui.doubleClick(400, 300)

    # drag() moves the mouse while holding the button down, duration controls
    # drag speed, button defaults to 'left'
    pyautogui.moveTo(300, 300, duration=0.3)
    pyautogui.drag(100, 0, duration=0.5, button="left")

    # scroll() takes positive (up) or negative (down) "clicks", the exact
    # pixel amount per click is OS-dependent so treat it as relative, not exact
    pyautogui.scroll(-5)


# ---------------------------------------------------------------------------
# SECTION 3: Keyboard functions
# ---------------------------------------------------------------------------
def section_3_keyboard_functions():
    # write() types a literal string, interval adds a delay per character so
    # the target app has time to register each keystroke
    pyautogui.write("hello from step 1", interval=0.05)

    # press() sends a single keypress (down + up), used for non-character keys
    pyautogui.press("enter")

    # hotkey() presses multiple keys in sequence then releases them in
    # reverse order, matching how real key combos are held
    pyautogui.hotkey("ctrl", "a")

    # hold() is a context manager, the key stays down for the whole block,
    # useful for held-modifier actions instead of manual keyDown/keyUp pairs
    with pyautogui.hold("shift"):
        pyautogui.press("home")


# ---------------------------------------------------------------------------
# SECTION 4: Fail-safe mechanism
# ---------------------------------------------------------------------------
def section_4_failsafe_demo():
    # FAILSAFE is on by default. Slamming the mouse to any screen corner
    # (0,0 / top-right / bottom-left / bottom-right) raises
    # pyautogui.FailSafeException and halts the script immediately.
    print(f"FAILSAFE is currently: {pyautogui.FAILSAFE}")

    # Never set this to False. An agent-driven script has no other kill
    # switch once it starts moving the mouse and typing on its own, this
    # corner-throw is the only manual override you have mid-run.
    # pyautogui.FAILSAFE = False   # left commented on purpose, do not enable

    try:
        print("Move your mouse to a screen corner within 3 seconds to test the fail-safe...")
        time.sleep(3)
        pyautogui.moveTo(500, 500, duration=1)
    except pyautogui.FailSafeException:
        print("Fail-safe triggered, script stopped as expected")


# ---------------------------------------------------------------------------
# SECTION 5: Fast screenshots with mss
# ---------------------------------------------------------------------------
def section_5_mss_screenshot():
    # pyautogui.screenshot() works but is slow because it goes through PIL
    # on every call. mss grabs frames directly from the OS, which matters
    # once Step 2 is screenshotting every loop iteration.
    with mss.mss() as sct:
        # monitors[0] is "all monitors combined", monitors[1] is the primary
        # display, use [1] unless you actually want a multi-monitor capture
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        output_path = "screenshot.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)
        print(f"Screenshot saved to {output_path}")


# ---------------------------------------------------------------------------
# Run sections individually by commenting out the ones you don't want to test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    section_1_general_functions()
    # section_2_mouse_functions()
    # section_3_keyboard_functions()
    # section_4_failsafe_demo()
    # section_5_mss_screenshot()
