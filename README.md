## Turning Hand-Drawn Paths into Autonomous LEGO BOOST Robot Movement Using AI

🤖 This application is a Python application that converts a hand-drawn robot path on grid paper into real movement on a LEGO BOOST Move Hub using AI Vision.

✏️ The user draws a path with a START point, saves it as input/sketch.png, and runs host.bat. The application sends the image to OpenAI Vision, which analyzes the sketch and generates a structured JSON path containing straight movements and turns.

📄 The generated JSON:

- 📏 Converts grid squares into millimeter distances (default: 50 mm per square)
- 🔄 Uses Pybricks angle conventions (positive = left turn, negative = right turn)
- ✅ Is validated using Pydantic models
- 📂 Is saved under `output/`
- ⚙️ Is converted into Pybricks DriveBase robot code

📡 The host application connects to the LEGO BOOST Move Hub over Bluetooth, uploads the generated program, and runs the robot so it follows the drawn path autonomously.

🔧 The robot parameters, such as straight speed and wheel turn rate, are configured in the Pybricks template rather than extracted from the sketch.

🧠 GPT-5.5 Vision performs very well at recognizing paths, distances, and angles from the input sketch.

### Links & Resources

<small>

- [LEGO BOOST](https://www.lego.com/en-us/themes/boost/videos)
- [Building Smart Robots with Pybricks and LEGO BOOST](https://github.com/Ashot72/lego-robotics-ai-with-pybricks)


</small>

## Clone and Run

```bash
# Clone the repository
git clone https://github.com/Ashot72/lego-boost-sketch-to-motion
cd lego-boost-sketch-to-motion

# First-time setup
setup.bat

# OpenAI API key — copy .env.example to .env, then set:
# OPENAI_API_KEY=sk-your-key-here
# Get a key: https://platform.openai.com/api-keys
copy .env.example .env

# Start the app
host.bat
```

## Debugging in VS Code

Install Microsoft's [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy) extension.

Open the Run view (View → Run or Ctrl+Shift+D) and choose **Debug Host**.

## Video

[Watch on YouTube](https://youtu.be/H7yFOdxtZNQ)
