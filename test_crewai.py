from crewai import Agent, Task, Crew, Process, LLM

llm = LLM(model="robdoe-local")

agent = Agent(
    name="RobdoeNode",
    role="Operator",
    goal="Identity-driven execution",
    llm=llm
)

task = Task("Run GENESIS vector", agent=agent)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process("sequential")
)

print(crew.kickoff())
