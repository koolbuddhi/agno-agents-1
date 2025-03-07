from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.azure import AzureOpenAI
#from agno.models.openai import OpenAIChat
from tools import DocumentTools
import os


# Load environment variables from .env file
load_dotenv()

# Define the model globally using environment variable
model = AzureOpenAI(id=os.getenv("MODEL_NAME"))
#model = OpenAIChat(id=os.getenv("MODEL_NAME"))

transcript_processor = Agent(
    name="Transcript Processor",
    role="Read folder of meeting transcripts in docx format and clean them without changing meaning",
    model=model,
    tools=[DocumentTools()],
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    instructions="""
    Remove filler words, correct grammar, standardize formatting.
    # guidelines:
   ##Speaker Identification:
   Clearly identify and format the speaker's name followed by the duration of their speech at the beginning of each section.
   The format should be as follows:
   Speaker Name   [Duration]  
   Example:
   Ethan Hall   [0:10]  
    """,
)

transcript_processor.print_response("Process all meeting transcripts in folder 'transcripts' and save cleaned versions in 'cleaned_transcripts' appending datetime tag to filename.", stream=True)