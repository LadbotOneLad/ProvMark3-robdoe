import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import DirectoryReadTool, FileReadTool

# Initialize your local or preferred LLM engine
llm = LLM(model="gemini/gemini-2.5-flash") # Or your local bridge endpoint

# 1. Define tools that point safely to the repository and treasure chest
# Read-only access ensures the treasure chest is protected
safe_dir_tool = DirectoryReadTool(directory='./')
proof_file_tool = FileReadTool(file_path='sovereign_lattice_proof.json')

# 2. Define Specialized Sovereign Agents
auditor_agent = Agent(
    role="Sovereign Lattice Auditor",
    goal="Independently verify Merkle root integrity and hardware anchor states against local proofs.",
    backstory=(
        "You are an uncompromising zero-trust cryptographic auditor. "
        "You trust no string, only raw mathematical verification and ledger consistency."
    ),
    tools=[proof_file_tool],
    llm=llm,
    verbose=True
)

guardian_agent = Agent(
    role="Repository State Guardian",
    goal="Monitor workspace hygiene, ensure git submodules and critical assets remain pristine, and report anomalies.",
    backstory=(
        "You protect the core root authority and the sacred treasure chest folders. "
        "You ensure zero accidental state corruption or unauthorized mutations occur."
    ),
    tools=[safe_dir_tool],
    llm=llm,
    verbose=True
)

# 3. Define the Tasks
audit_task = Task(
    description=(
        "Inspect the current sovereign_lattice_proof.json file. "
        "Verify that the Merkle root calculation matches the structural leaf nodes."
    ),
    expected_output="A definitive cryptographic integrity report confirming Byzantine immutability.",
    agent=auditor_agent
)

integrity_task = Task(
    description=(
        "Scan the repository file tree structure. Confirm that the core treasure chest "
        "and critical directories are intact, untouched, and properly accounted for."
    ),
    expected_output="A clean workspace status manifest verifying zero unauthorized modifications.",
    agent=guardian_agent
)

# 4. Assemble the Autonomous Crew
sovereign_crew = Crew(
    agents=[auditor_agent, guardian_agent],
    tasks=[audit_task, integrity_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("[*] Initializing Sovereign Crew Orchestration...")
    result = sovereign_crew.kickoff()
    print("\n[✔] CREW EXECUTION COMPLETE:")
    print(result)
