import os

print(">>> CrewAI Operator Module Installer")
root = os.getcwd()

module_dir = os.path.join(root, "crewai")
module_file = os.path.join(module_dir, "__init__.py")

print(f">>> Target directory: {module_dir}")
print(f">>> Target file: {module_file}")

os.makedirs(module_dir, exist_ok=True)

content = """
# ====================================================
#  CrewAI Operator Edition (Termux-Compatible)
#  Custom module for Robdoe identity-driven mesh
# ====================================================

import subprocess
import os

class Agent:
    def __init__(self, name="agent", role=None, goal=None, backstory=None, llm=None):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = llm

    def run(self, input_text):
        return f"[{self.name}] processed: {input_text}"

class Task:
    def __init__(self, description, agent=None, expected_output=None):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output

    def execute(self):
        if self.agent:
            return self.agent.run(self.description)
        return f"Task executed: {self.description}"

class Crew:
    def __init__(self, agents=None, tasks=None, process=None):
        self.agents = agents or []
        self.tasks = tasks or []
        self.process = process

    def kickoff(self):
        results = []
        for task in self.tasks:
            results.append(task.execute())
        return results

class Process:
    def __init__(self, name="sequential"):
        self.name = name

class LLM:
    def __init__(self, model="local", temperature=0.2):
        self.model = model
        self.temperature = temperature

    def generate(self, prompt):
        return f"[LLM:{self.model}] → {prompt}"

class OperatorAgent(Agent):
    def run(self, input_text):
        text = input_text.upper()

        if "GENESIS" in text:
            return subprocess.getoutput("python genesis.py")

        if "ATOM" in text:
            return subprocess.getoutput("python atom.py")

        if "TRUTH" in text:
            return subprocess.getoutput("python truth.py")

        if "WEATHER" in text or "SWARM" in text:
            return subprocess.getoutput("python weather.py")

        if "ESP" in text or "NODE" in text:
            return subprocess.getoutput("python esp32_check.py")

        if text.startswith("CMD:"):
            cmd = input_text.split("CMD:", 1)[1].strip()
            return subprocess.getoutput(cmd)

        return f"[{self.name}] processed: {input_text}"

def run_cmd(cmd):
    try:
        return subprocess.getoutput(cmd)
    except Exception as e:
        return f"Command error: {e}"

def esp32_ping(port="/dev/ttyUSB0", baud=115200):
    try:
        import serial
        ser = serial.Serial(port, baud, timeout=1)
        ser.write(b'ping\\n')
        reply = ser.readline().decode().strip()
        return f"ESP32 replied: {reply}"
    except Exception as e:
        return f"ESP32 error: {e}"
"""

with open(module_file, "w") as f:
    f.write(content)

print(">>> CrewAI Operator Module Installed Successfully")
