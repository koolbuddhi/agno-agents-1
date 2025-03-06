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
    instructions="Evaluate the transcript for clarity, coherence, and overall quality. Provide suggestions for improvement if necessary."
)

# Run the review process on cleaned transcripts
def review_transcripts():
    review_agent.print_response("Review all cleaned transcripts in folder 'cleaned_transcripts' and provide feedback.", stream=True)

if __name__ == "__main__":
    review_transcripts()
