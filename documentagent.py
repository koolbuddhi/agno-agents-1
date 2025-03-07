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
   Prompt for AI Agent: Document Cleaning Task
   Your task is to clean the provided transcript by removing filler words, vocal pauses, and redundant phrases while preserving the original meaning and sentence structure. Please adhere to the following guidelines:
   Speaker Identification:
   Clearly identify and format the speaker's name followed by the duration of their speech at the beginning of each section.
   The format should be as follows:
   Speaker Name   [Duration]  
   Example:
   Ethan Hall   [0:10]  
   2. Content Formatting:
   Below the speaker's name and duration, provide the cleaned content of their speech on a new line.
   Ensure that each speaker's response is clearly separated and does not merge with another speaker's content.
   Do not combine two different answers or questions into one.
   Remove Filler Words: Eliminate any vocal pauses and filler words, including but not limited to:
   "uh," "um," "oh," "yeah," "so," "like," "basically," "actually," "I guess," "you know," "kind of," "just," and similar expressions.
   Repeated words or phrases that do not add meaning or clarity.
   Unnecessary conversational fragments that do not contribute to the main point.
   Maintain Sentence Structure:
   Keep the original sentence structure and wording as much as possible.
   Make only minimal edits necessary for clarity and readability.
   Ensure that the underlying meaning of the conversation is preserved.
   Clarification and Context:
   If a sentence or phrase is unclear due to conversational hesitations or filler words, rephrase it for clarity without altering its meaning. Ensure that technical terms and industry jargon are accurately represented.
   Output Format:
   Provide the cleaned transcript in a clear and organized format.
   Highlight where significant edits were made to improve clarity while ensuring the original intent of the speaker remains intact.
   Review for Coherence:
   After cleaning, review the document to ensure that it reads smoothly and logically, without any abrupt transitions or fragmented thoughts.
   Specificity in Content:
   Retain important details, such as names, specific terms, and context relevant to the discussion, while ensuring the content is concise and coherent.
   Preserve Key Metrics and Insights:
   Ensure that any metrics, evaluations, or insights shared during the conversation are preserved in the cleaned document for future reference.
   Capture Nuanced Details:
   Pay attention to the flow of the conversation, capturing nuanced details such as relationship dynamics, partnership evaluations, and specific market insights that may be vital for understanding the context.
   Enhance Readability:
   Where applicable, break long sentences into shorter, more digestible pieces to improve readability while maintaining the original meaning.
   Preserve Tone and Style:
   Keep the tone and style of the original speaker while ensuring clarity and professionalism in the cleaned text.
   Identify Key Use Cases:
   Highlight any specific use cases mentioned that are relevant to the technology or service being discussed, ensuring those insights are clearly articulated.
   Highlight Unique Value Propositions:
   Capture any unique selling points or differentiators mentioned in the conversation regarding the product or service being evaluated.
"""
)

transcript_processor.run("Process all meeting transcripts in folder 'transcripts' and save cleaned versions in 'cleaned_transcripts'.", stream=True)