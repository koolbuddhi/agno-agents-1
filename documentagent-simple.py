from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools import DocumentTools

transcript_processor = Agent(
    name="Transcript Processor",
    role="Read folder of meeting transcripts in docx format and clean them without changing meaning",
    model= OpenAIChat(id="gpt-4o"),
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