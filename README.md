## Vibe Todo – Tkinter Desktop App

A small, modern-styled todo list built with Python and Tkinter.

### Features
- **Add tasks** with a quick input bar and Enter key.
- **Delete tasks** with the Delete key or button.
- **Mark tasks completed** (toggle) with the button or **Ctrl+Enter**.
- **Persistent storage** in a local `tasks.json` file.

### Requirements
- **Python 3.8+**
- Tkinter (usually bundled with standard Python on Windows/macOS/Linux).

You can optionally install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Run the app

```bash
python main.py
```
## Dockerization

### Build the image
```bash
docker build -t smart-task-manager .

### Run the container
```bash
docker run -it --rm -e DISPLAY=$DISPLAY smart-task-manager