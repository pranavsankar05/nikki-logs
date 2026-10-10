from dotenv import load_dotenv
import anthropic

from pathlib import Path
load_dotenv(Path(__file__).parent / ".env")
client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=50,
    messages=[{"role": "user", "content": "Say hello in 5 words."}],
)
print(msg.content[0].text)