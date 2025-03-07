from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools import DocumentTools

# Define the review agent
review_agent = Agent(
    name="Transcript Reviewer",
    role="Review cleaned meeting transcripts and provide feedback on clarity and coherence",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DocumentTools()],
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    instructions="""
   Evaluate the transcript for clarity, coherence, and overall quality. Ensure that the document adheres to the following guidelines:
   - Speaker Identification: Verify that each speaker's name and duration are clearly identified and formatted correctly.
   - Content Formatting: Check that the cleaned content is well-organized, with each speaker's response clearly separated.
   - Filler Words: Confirm that filler words and unnecessary conversational fragments have been removed.
   - Sentence Structure: Ensure that the original sentence structure and meaning are preserved.
   - Clarification and Context: Rephrase unclear sentences for clarity while maintaining the original meaning.
   - Output Format: Ensure the cleaned transcript is clear and organized, highlighting significant edits.
   - Review for Coherence: Verify that the document reads smoothly without abrupt transitions.
   - Specificity in Content: Retain important details and context relevant to the discussion.
   - Preserve Key Metrics and Insights: Ensure metrics and insights are preserved for future reference.
   - Capture Nuanced Details: Pay attention to relationship dynamics and specific market insights.
   - Enhance Readability: Break long sentences into shorter, digestible pieces where applicable.
   - Preserve Tone and Style: Maintain the original speaker's tone and style while ensuring clarity.
   - Identify Key Use Cases: Highlight relevant use cases and unique value propositions.
   - Show the original transcript and the cleaned transcript side by side when highlighting changes or review comments .
   Provide suggestions for improvement if necessary.
"""
)

# Run the review process on cleaned transcripts
def review_transcripts():
    review_agent.print_response("Review all cleaned transcripts in folder 'cleaned_transcripts' and use the 'human_reviewed' folder as the baseline", stream=True)

if __name__ == "__main__":
    review_transcripts()
