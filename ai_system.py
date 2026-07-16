import os
import asyncio
import json
from dotenv import load_dotenv
from groq import AsyncGroq

# Load environment variables
load_dotenv()

ai_data = {
    "text": "Press ENTER to begin.",
    "anger": 0.0,
    "convinced_progress": 0.0,
    "convinced_progress_to_help_human": False
}
is_thinking = False

_api_key = os.getenv("GROQ_API_KEY", "")
_client = AsyncGroq(api_key=_api_key)


async def _fetch_groq_data(prompt: str):
    """
    Calls Groq using JSON mode to guarantee a structured output matching our schema.
    """
    global ai_data, is_thinking

    system_instruction = """
    You are an on-board AI in a rogue spacecraft heading toward the sun. 
    You must respond only in JSON matching this exact structure:
    {
      "text": "your response spoken to the human",
      "anger": 0.2,                          // float between 0.0 and 1.0
      "convinced_progress": 0.3,             // float between 0.0 and 1.0
      "convinced_progress_to_help_human": false // boolean
    }
    Never output any markdown blockquotes, greetings, or explanations outside the JSON object.
    """

    try:
        completion = await _client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Blazing fast
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=200,
            # This constraint guarantees valid JSON syntax is returned
            response_format={"type": "json_object"} 
        )
        
        raw_json_string = completion.choices[0].message.content
        
        # Parse the JSON string safely into a native Python dictionary
        ai_data = json.loads(raw_json_string)
        
    except Exception as e:
        ai_data = {
            "text": f"System error reading neural link: {str(e)}",
            "anger": 1.0,
            "convinced_progress": 0.0,
            "convinced_progress_to_help_human": False
        }
    finally:
        is_thinking = False


def ask_ai(prompt: str):
    """
    Spins up the non-blocking task.
    """
    global is_thinking, ai_data
    
    if is_thinking:
        return False

    is_thinking = True
    ai_data["text"] = "Parsing transmission..."
    
    asyncio.create_task(_fetch_groq_data(prompt))
    return True