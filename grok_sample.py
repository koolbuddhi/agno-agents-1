from agno.agent import Agent
from agno.models.azure import AzureOpenAI
#from agno.models.openai import OpenAIChat
from tools import DocumentTools
import os
from dotenv import load_dotenv
from docx import Document


# Load environment variables from .env file
load_dotenv()

# Define the model globally using environment variable
model = AzureOpenAI(id=os.getenv("MODEL_NAME"))
#model = OpenAIChat(id=os.getenv("MODEL_NAME"))


# Pattern Analyzer Agent: Learns from human-reviewed samples
pattern_analyzer_agent = Agent(
    name="Pattern Analyzer Agent",
    role="Analyze human-reviewed transcripts for patterns",
    model=model,
    tools=[DocumentTools()],
    instructions=[
        "Read all .docx files from 'human_reviewed/' folder.",
        "Compare with corresponding raw transcripts from 'transcripts/' (if available).",
        "Identify patterns: common filler words removed, preserved phrases, formatting styles.",
        "Output a summary of findings to refine other agents’ instructions."
        "Save output to 'pattern_summary.md' to reuse the rules."
    ],
    markdown=True,
)

# Metadata Agent: Handles speaker identification and duration
metadata_agent = Agent(
    name="Metadata Agent",
    role="Extract and format speaker names and durations",
    model=model,
    instructions=[
        "Identify each speaker and their speech duration from the transcript.",
        "Format as 'Speaker Name [Duration]' (e.g., 'Ethan Hall [0:10]') at the start of each section.",
        "Separate each speaker’s content clearly on a new line."
    ],
    markdown=True,
)

# Preprocessor Agent: Flags filler words and redundancies
preprocessor_agent = Agent(
    name="Preprocessor Agent",
    role="Flag filler words and redundancies with minimal intervention",
    model=model,
    instructions=[
        "Scan the transcript for filler words (e.g., 'uh,' 'um,' 'like,' 'you know') and redundant phrases.",
        "Only flag items that are purely vocal pauses or meaningless interjections using [REMOVE].",
        "Do not flag words contributing to emphasis, phrasing, or intent (e.g., 'just' for emphasis).",
        "Preserve proper nouns, numbers, dates, technical terms, and examples."
    ],
    markdown=True,
)

# Simplifier Agent: Removes flagged items minimally
simplifier_agent = Agent(
    name="Simplifier Agent",
    role="Remove flagged sections with minimal changes",
    model=model,
    instructions=[
        "Remove sections marked [REMOVE] from the transcript.",
        "Make the absolute minimum changes necessary for clarity.",
        "Preserve original sentence structure, wording, and intent.",
        "Do not summarize or condense responses—keep full detail."
    ],
    markdown=True,
)

# Verifier Agent: Ensures meaning preservation with human-reviewed comparison
verifier_agent = Agent(
    name="Verifier Agent",
    role="Verify meaning and add ambiguity notes",
    model=model,
    tools=[DocumentTools()],
    instructions=[
        "Compare the original transcript with the cleaned version.",
        "If a human-reviewed version exists in 'human_reviewed/', compare against it to ensure consistency.",
        "Ensure all essential details (proper nouns, numbers, dates, technical terms, examples) remain intact.",
        "If a sentence is unclear after cleaning, add a bracketed note (e.g., '[Sentence may be ambiguous]').",
        "Flag any loss of meaning or intent and suggest minimal corrections."
    ],
    markdown=True,
)

# Formatter Agent: Polishes and highlights changes
formatter_agent = Agent(
    name="Formatter Agent",
    role="Polish output and highlight changes",
    model=model,
    instructions=[
        "Ensure proper grammar, punctuation, and readability in the cleaned transcript.",
        "Break long sentences into shorter ones only if needed, preserving meaning.",
        "Highlight removed/changed words using markdown (e.g., ~~uh~~).",
        "Maintain the speaker’s tone and style, avoiding over-formalization."
        "Format as 'Speaker Name [Duration]' (e.g., 'Ethan Hall [0:10]') at the start of each section."
    ],
    markdown=True
)

# Coordinator Agent: Manages workflow and file operations
cleaning_team = Agent(
    team=[metadata_agent, preprocessor_agent, simplifier_agent, verifier_agent, formatter_agent],
    model=model,
    tools=[DocumentTools()],
    instructions=[
        "List all .docx files in 'transcripts/' using DocumentTools.",
        "For each file: read the raw transcript, process it through the team, and save to 'cleaned_transcripts/'.",
        "Start with Metadata Agent to format speaker names and durations.",
        "Pass to Preprocessor Agent to flag filler words.",
        "Send to Simplifier Agent to remove flagged items.",
        "Forward to Verifier Agent to check meaning and add notes.",
        "Finish with Formatter Agent to polish and highlight changes.",
        "Save the cleaned transcript as a .docx file in 'cleaned_transcripts/' with the same name.",
        "Provide a summary of changes for each file.",
        "Context: Due diligence interview with {{Company under due diligence}}Company."
    ],
    show_tool_calls=True,
    markdown=True
)

# Run Pattern Analyzer first to refine instructions (optional)
pattern_analyzer_agent.print_response("Analyze patterns from 'human_reviewed/' folder.", stream=True)

# Process all transcripts
cleaning_team.print_response("He is the transcripts for 'ThreatMark's technology'. Clean all transcripts in 'transcripts/' folder and save to 'cleaned_transcripts/'.", stream=True)