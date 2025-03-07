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
    debug_mode=True,
    monitoring=True,
    description="""\
        Your task is to clean the provided transcript of a commercial company due diligence and agency interview with an employee from ThreatMark Company. Clean the transcript by removing filler words, vocal pauses, and redundant phrases while preserving the original meaning and sentence structure. Your primary goal is to clean the transcript while making the ABSOLUTE MINIMUM changes necessary. Prioritize preserving the original wording and meaning. Only remove filler words and redundant phrases when they clearly impede understanding. If there is any doubt, leave the original phrasing. Pay special attention to preserving all proper nouns, numbers, dates, technical terms, and specific examples. Only remove filler words that are purely vocal pauses or meaningless interjections. Do not remove words that, while potentially redundant, contribute to the speaker's emphasis or phrasing. If a sentence is unclear after removing filler words, add a brief, bracketed note explaining the potential ambiguity, but do not change the core wording. After cleaning, compare the cleaned transcript to the original. Verify that all essential details remain intact. If possible, highlight the words or phrases that were removed or changed in the cleaned transcript, using a different color or font style. Perform a final review to ensure that the cleaned transcript is accurate, coherent, and preserves the original meaning and intent of the speakers.
        Crucially, do not summarize or condense the speaker's answers. Your task is to clean, not to interpret or synthesize. Maintain the full detail of each response, focusing solely on removing filler words and improving clarity without altering the speaker's original content.
        This transcript is from a commercial company's due diligence process, involving an agency interview with an employee from ThreatMark Company. The interview focuses on evaluating ThreatMark's services, technology, and their suitability for a potential partnership or investment.
    """,
    instructions="""\
   Following are the instruction you need to follow when cleanning the transcipts 
##### 1. Speaker Identification
- Clearly identify and format the speaker's name followed by the duration of their speech at the beginning of each section.
- The format should be as follows:
  - Speaker Name [Duration]
  - Example:
    - Ethan Hall [0:10]

##### 2. Content Formatting
- Below the speaker's name and duration, provide the cleaned content of their speech on a new line.
- Ensure that each speaker's response is clearly separated and does not merge with another speaker's content.
- Do not combine two different answers or questions into one.

##### 3. Remove Filler Words
- Only remove filler words that are purely vocal pauses or meaningless interjections. Do not remove words that, while potentially redundant, contribute to the speaker's emphasis or phrasing.
- Remove filler words only when they do not alter the intended meaning of the sentence. If a filler word is used for emphasis, or to indicate a pause for thought that is relevant to the conversation, do not remove it.
- Eliminate any vocal pauses and filler words, including but not limited to: "uh," "um," "oh," "yeah," "so," "like," "basically," "actually," "I guess," "you know," "kind of," "just," and similar expressions.
- Remove repeated words or phrases that do not add meaning or clarity.
- Remove unnecessary conversational fragments that do not contribute to the main point.

##### 4. Maintain Sentence Structure
- Keep the original sentence structure and wording as much as possible.
- Make only minimal edits necessary for clarity and readability.
- Ensure that the underlying meaning of the conversation is preserved.

##### 5. Clarification and Context
- If a sentence or phrase is unclear due to conversational hesitations or filler words, add a brief, bracketed note explaining the potential ambiguity, but do not change the core wording. Example: '[Sentence may be interpreted in multiple ways due to original conversational structure]'.
- Ensure that technical terms and industry jargon related to cybersecurity, fraud detection, and ThreatMark's specific solutions are accurately represented.
- Maintain the natural flow of the conversation, even if the speakers use informal language. Do not attempt to make the conversation sound overly formal.
- Capture the intent of the speaker rather than making sentences grammatically perfect.

##### 6. Output Format
- Provide the cleaned transcript in a clear and organized format.
- If possible, highlight the words or phrases that were removed or changed in the cleaned transcript, using a different color or font style. This will allow for easy review and verification.

##### 7. Review for Coherence
- After cleaning, review the document to ensure that it reads smoothly and logically, without any abrupt transitions or fragmented thoughts.
- Compare the cleaned transcript to the original. Verify that all essential details remain intact.
- Perform a final review to ensure that the cleaned transcript is accurate, coherent, and preserves the original meaning and intent of the speakers.

##### 8. Specificity in Content
- Retain important details, such as names, specific terms, and context relevant to the discussion, while ensuring the content is concise and coherent.
- Pay special attention to preserving:
  - All proper nouns (names, company names, product names, especially ThreatMark).
  - Numbers and numerical data (e.g., performance metrics, financial data).
  - Dates and times.
  - Technical terms and industry jargon related to cybersecurity and fraud detection.
  - Any specific examples that are mentioned regarding ThreatMark's technology, use cases, or client interactions.

##### 9. Preserve Key Metrics and Insights
- Ensure that any metrics, evaluations, or insights shared during the conversation regarding ThreatMark's performance, technology, or market position are preserved in the cleaned document for future reference.

##### 10. Capture Nuanced Details
- Pay attention to the flow of the conversation, capturing nuanced details such as relationship dynamics, partnership evaluations, and specific market insights related to ThreatMark's industry that may be vital for understanding the context.

##### 11. Enhance Readability
- Where applicable, break long sentences into shorter, more digestible pieces to improve readability while maintaining the original meaning.

##### 12. Preserve Tone and Style
- Keep the tone and style of the original speaker while ensuring clarity and professionalism in the cleaned text.

##### 13. Identify Key Use Cases
- Highlight any specific use cases mentioned that are relevant to ThreatMark's technology or services, ensuring those insights are clearly articulated.

##### 14. Highlight Unique Value Propositions
- Capture any unique selling points or differentiators mentioned in the conversation regarding ThreatMark's products or services.
"""
)

transcript_processor.print_response("Process all meeting transcripts in folder 'transcripts' and save cleaned versions in 'cleaned_transcripts'.", stream=True)