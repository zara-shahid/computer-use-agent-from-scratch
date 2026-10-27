# Computer Use Agent From Scratch

A step-by-step build of a computer use agent: an agent that looks at the screen, decides what to do, and controls the mouse and keyboard to complete tasks across real desktop applications. Built with free tools only: Groq vision models for reasoning, PyAutoGUI for control, and Tesseract for OCR.

This is Phase 7 of my AI agents learning journey, extending the browser-only agent from the previous phase to full OS-level control.

## What This Repo Covers


| Step | Folder | File | Topic |
|------|--------|------|-------|
| 1 | `01-pyautogui-basics` | `pyautogui_basics.py` | Mouse, keyboard, and screen control, fail-safe, fast screenshots with mss |
| 2 | `02-screenshot-agent-loop` | `screenshot_agent_loop.ipynb` | Screenshot to vision model to action loop, calculator mini-project |
| 3 | `03-grounding-accuracy` | `grounding_accuracy.ipynb` | Click-accuracy benchmark for the vision model |
| 4 | `04-structured-actions` | `structured_actions.ipynb` | Pydantic action schema with function calling and retry logic |
| 5 | `05-multi-app-tasks` | `multi_app_tasks.ipynb` | Window switching, OCR fallback, cross-app task |

## The Core Loop

```
screenshot (mss) -> vision model (Groq) -> structured action (Pydantic) -> execute (PyAutoGUI) -> repeat
```

The loop ends when the model returns a `done` action or a hard step limit is reached.

## Step Summaries

**Step 1: PyAutoGUI Basics**
Screen size and mouse position, mouse functions (move, click, double click, drag, scroll), keyboard functions (write, press, hotkey, hold), and the fail-safe that aborts the script when the mouse is moved to a screen corner. Uses `mss` for screenshots because it is faster than PyAutoGUI's built-in capture. Written as a plain script rather than a notebook.

**Step 2: Screenshot-Based Agent Loop**
Captures the screen, base64-encodes it, and sends it with a task prompt to a Groq vision model. The model's response is parsed into a next action and executed with PyAutoGUI. Includes a hard step limit. Mini-project: completing a calculation in a calculator app using only the screenshot-to-action loop.

**Step 3: Grounding Accuracy Benchmark**
A small benchmark following the ScreenSpot methodology: a prediction counts as correct only if the predicted click point falls inside the ground-truth bounding box of the target. Results are split by target type (text-labeled vs icon-like) and size, with a written section on observed failure modes, and a comparison against the DOM vs vision findings from the browser agent phase.

**Step 4: Structured Action Schema**
Replaces free-text action parsing with a Pydantic schema using `Literal` types (click, type, scroll, wait, done) and Groq function calling, plus retry logic for malformed tool calls. Wired into the Step 2 loop.

**Step 5: Multi-App Task Completion**
Window focus handling with `pygetwindow` so the agent can switch between applications, and an OCR fallback with `pytesseract` for apps with no accessible text layer. Mini-project: copying data from a text file into a spreadsheet app.

## Tech Stack

- Python
- Groq API (vision-capable models)
- PyAutoGUI
- mss
- Pydantic
- pygetwindow
- pytesseract with Tesseract OCR
- Jupyter

## Setup

```bash
git clone https://github.com/zara-shahid/computer-use-agent-from-scratch.git
cd computer-use-agent-from-scratch
pip install pyautogui mss pydantic groq pygetwindow pytesseract pillow jupyter
```

Create a `.env` file in the repo root:

```
GROQ_API_KEY=your_key_here
```

**Tesseract (Step 5 only):** install the Tesseract engine separately, since `pytesseract` is only a wrapper. On Windows, use the UB-Mannheim installer and set the binary path explicitly in your code:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Notes

- **Vision model availability changes.** Groq updates its multimodal lineup often and deprecates models (for example, `llama-4-scout` was deprecated in July 2026). Check the current list at https://console.groq.com/docs/vision before running.
- **Keep the fail-safe on.** PyAutoGUI's fail-safe is the emergency stop for an agent that controls your real mouse and keyboard. Move the cursor to a screen corner to abort.
- **Run on a clean desktop.** The agent acts on whatever is on screen, so close sensitive windows before running any loop.
- **Open vision models are less precise than frontier computer-use models** at pixel-level grounding. Step 3 measures this rather than assuming it.

## Resources

- PyAutoGUI docs: https://pyautogui.readthedocs.io/
- python-mss docs: https://python-mss.readthedocs.io/
- Groq vision docs: https://console.groq.com/docs/vision
- Groq tool use docs: https://console.groq.com/docs/tool-use
- ScreenSpot benchmark methodology: https://arxiv.org/pdf/2601.22491
- PyGetWindow: https://github.com/asweigart/PyGetWindow
- pytesseract: https://pypi.org/project/pytesseract/
