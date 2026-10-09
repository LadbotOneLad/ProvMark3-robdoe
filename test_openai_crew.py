#!/usr/bin/env python3
import sys
import subprocess
import os

def run_openai_crew():
    print("================================================================")
    print("          CREWAI + OPENAI API INTEGRATION ENGINE                ")
    print("================================================================")
    
    # 1. Ensure crewai and openai are installed (using lightweight pip install with no cargo build needed)
    try:
        import crewai
        print(f"[+] Found CrewAI version: {crewai.__version__}")
    except ImportError:
        print("[*] Installing crewai...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai"])

    # 2. Check for OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[!] OPENAI_API_KEY environment variable not detected.")
        api_key = input("Enter your OpenAI API Key: ").strip()
        os.environ["OPENAI_API_KEY"] = api_key

    from crewai import Agent, Task, Crew, LLM

    # Use standard OpenAI model via CrewAI LLM wrapper
    openai_llm = LLM(model="gpt-4o-mini")

    print("[*] Initializing agents with OpenAI backend...")
    
    architect = Agent(
        role='System Architect',
        goal='Design efficient resource mapping and directory structures for mobile compute nodes.',
        backstory='An expert in systems engineering, storage optimization, and cross-platform architecture.',
        verbose=True,
        llm=openai_llm
    )

    task = Task(
        description='Formulate a 3-step checklist to verify that storage, dependencies, and execution environments are correctly synchronized on external storage.',
        expected_output='A clear, bulleted action plan for system verification.',
        agent=architect
    )

    crew = Crew(
        agents=[architect],
        tasks=[task],
        verbose=True
    )

    print("[*] Executing CrewAI workflow using OpenAI...")
    try:
        result = crew.kickoff()
        print("\n================================================================")
        print("                  CREW EXECUTION RESULT                         ")
        print("================================================================")
        print(result)
        print("================================================================")
    except Exception as e:
        print(f"[!] Execution failed: {e}")

if __name__ == "__main__":
    run_openai_crew()
