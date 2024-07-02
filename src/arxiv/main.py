#!/usr/bin/env python

import os
import re
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from arxiv.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

def normalize_filename(text,sep="-"):   
    return sep.join([i.strip() for i in re.split(r'[^a-z0-9]+', text.lower()) if i.strip()])

if False:
	t = "Deep Learning & AI"
	print(normalize_filename(t))

# INPUT_TOPIC = "self-service analytics"
# INPUT_TOPIC = "bilingual learning"
INPUT_TOPIC = "precision medicine"
OUTPUT_FILE = f"{normalize_filename(INPUT_TOPIC)}.md"

@CrewBase
class ArxivCrew():
	"""Arxiv crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file=OUTPUT_FILE
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Arxiv crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
	
# entry-point    
def run():
    if False:
        api_key = os.getenv("OPENAI_API_KEY")
        llm_model = os.getenv("OPENAI_MODEL_NAME")
        print(f"llm_model: {llm_model}")
        print(f"api_key: {api_key[:5]}***{api_key[-2:]}")
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': INPUT_TOPIC
    }
    ArxivCrew().crew().kickoff(inputs=inputs)