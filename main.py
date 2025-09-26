# main.py (FINAL, CORRECTED, CREWAI VERSION)
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from langchain_openai import ChatOpenAI # Nayi, zaroori import

# --- API Keys aur Model Configuration ---
    
# Apni API keys ko environment variables se load karein
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY") # Hum OpenRouter ki key istemal kar rahe hain

# CrewAI ko batayein ke hum OpenRouter istemal kar rahe hain
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct:free",
    base_url="https://openrouter.ai/api/v1"
)

# --- Hamari AI Team (The Crew) ---

# Agent 1: The Researcher
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation=False,
  tools=[SerperDevTool(), ScrapeWebsiteTool(), WebsiteSearchTool()],
  llm=llm # Har agent ko batayein ke kaun sa model istemal karna hai
)

# Agent 2: The Writer
writer = Agent(
  role='Professional Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
  verbose=True,
  allow_delegation=True,
  llm=llm # Har agent ko batayein ke kaun sa model istemal karna hai
)

# --- Hamare Tasks (Kaam) ---

# Task 1: Research ka kaam
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify the top 3 most significant trends, their potential impacts on the industry,
  and provide relevant links to support your findings.""",
  expected_output="A full analysis report with citations.",
  agent=researcher
)

# Task 2: Likhne ka kaam
task2 = Task(
  description="""Using the insights provided by the research analyst, develop an engaging blog
  post that highlights the most significant AI advancements.
  Your post should be informative yet accessible, catering to a tech-savvy audience.
  Make it sound cool, avoid complex words unless you explain them.""",
  expected_output="A full blog post of at least 4 paragraphs.",
  agent=writer
)

# --- Factory ko Start Karna ---

# Crew ko assemble karein
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  process=Process.sequential
)

# Kaam shuru karein!
result = crew.kickoff()

print("######################")
print("## FINAL RESULT ##")
print("######################")
print(result)
