#!/usr/bin/env python3
import sys
import subprocess

def setup_and_run_crew():
    print("================================================================")
    print("          CREWAI LOCAL OLLAMA INTEGRATION ENGINE                ")
    print("================================================================")
    
    # 1. Ensure crewai and litellm are available
    try:
        import crewai
        print(f"[+] Found CrewAI version: {crewai.__version__}")
    except ImportError:
        print("[*] Installing crewai with litellm support...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai[litellm]"])

    from crewai import Agent, Task, Crew, LLM

    # 2. Configure CrewAI to target local Ollama instance running gemma4:12b
    local_llm = LLM(
        model="ollama/gemma4:12b",
        base_url="http://127.0.0.1:11434"
    )

    print("[*] Initializing local role-playing agents...")
    
    # Define specialized agents
    system_analyst = Agent(
        role='System Performance Specialist',
        goal='Analyze local compute nodes and optimize workloads efficiently.',
        backstory='An expert in embedded hardware constraints, Linux resource allocation, and lightweight process control.',
        verbose=True,
        llm=local_llm,
        memory=True
    )

    code_auditor = Agent(
        role='Code & Security Auditor',
        goal='Review system execution blocks for stability and performance bottlenecks.',
        backstory='A meticulous kernel code inspector focused on secure, low-latency execution loops.',
        verbose=True,
        llm=local_llm,
        memory=True
    )

    # Define concrete operational tasks
    task1 = Task(
        description='Evaluate current memory and CPU overhead metrics and formulate a 3-step mitigation strategy.',
        expected_output='A concise, itemized list of optimizations for low-resource environments.',
        agent=system_analyst
    )

    task2 = Task(
        description='Review the optimization strategy from task1 and draft a compact shell execution snippet.',
        expected_output='Valid executable commands enclosed in a markdown block.',
        agent=code_auditor
    )

    # Assemble the multi-agent crew
    local_crew = Crew(
        agents=[system_analyst, code_auditor],
        tasks=[task1, task2],
        verbose=True
    )

    print("[*] Launching multi-agent execution cycle locally via Ollama...")
    try:
        result = local_crew.kickoff()
        print("\n================================================================")
        print("                  CREW EXECUTION FINAL RESULT                   ")
        print("================================================================")
        print(result)
        print("================================================================")
    except Exception as e:
        print(f"[!] Crew execution failed: {e}")
        print("[!] Ensure Ollama is running on port 11434 with 'gemma4:12b' loaded.")

if __name__ == "__main__":
    setup_and_run_crew()
