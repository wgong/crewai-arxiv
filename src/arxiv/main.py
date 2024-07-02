#!/usr/bin/env python
from arxiv.crew import ArxivCrew
import os

def run():
    if False:
        api_key = os.getenv("OPENAI_API_KEY")
        llm_model = os.getenv("OPENAI_MODEL_NAME")
        print(f"llm_model: {llm_model}")
        print(f"api_key: {api_key[:5]}***{api_key[-2:]}")
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'self-service analytics'
    }
    ArxivCrew().crew().kickoff(inputs=inputs)