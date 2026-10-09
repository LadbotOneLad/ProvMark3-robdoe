import os
import json
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import FileReadTool

# Initialize local or cloud LLM engine
llm = LLM(model="gemini/gemini-2.5-flash")

# Load the live proof data to give the agents real telemetry
proof_tool = FileReadTool(file_path='sovereign_lattice_proof.json')

# 1. Define the Value-Translation Agent
evangelist_agent = Agent(
    role="Sovereign Value Architect",
    goal="Translate low-level hardware-to-ledger proofs into undeniable, high-impact value statements for the public.",
    backstory=(
        "You bridge the gap between elite systems engineering and universal human comprehension. "
        "You make people realize that local-first, hardware-anchored sovereignty isn't just cool tech—it's the future of trust."
    ),
    tools=[proof_tool],
    llm=llm,
    verbose=True
)

# 2. Define the Manifest Task
manifest_task = Task(
    description=(
        "Analyze the sovereign_lattice_proof.json and the ESP32 hardware anchor state. "
        "Draft a high-impact public manifest that answers: "
        "1. What did we just build? "
        "2. Why is traditional cloud infrastructure obsolete compared to this? "
        "3. How does this guarantee absolute Byzantine immutability for anyone who audits it?"
    ),
    expected_output="A striking, professional, and uncompromising public release manifest ready for robdoe.com.",
    agent=evangelist_agent
)

# 3. Spin up the Crew
value_crew = Crew(
    agents=[evangelist_agent],
    tasks=[manifest_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("[*] Engaging CrewAI Value-Broadcast Engine...")
    result = value_crew.kickoff()
    
    # Save the output to a public-facing markdown file for the web layer
    output_filename = "SOVEREIGN_VALUE_MANIFEST.md"
    with open(output_filename, "w") as f:
        f.write(str(result))
        
    print(f"\n[✔] VALUE MANIFEST LOCKED TO DISK: {output_filename}")
