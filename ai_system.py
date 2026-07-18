import os
import asyncio
import json
from dotenv import load_dotenv
from groq import AsyncGroq


load_dotenv()

ai_data = {
    "text": "Press ENTER to begin.",
    "satisfaction_change": 0.0,
    "help_human": False
}

is_thinking = False

_api_key = os.getenv("GROQ_API_KEY", "")
_client = AsyncGroq(api_key = _api_key)


async def _fetch_groq_data(prompt: str):
    """
    Calls Groq using JSON mode to guarantee a structured output matching our schema.
    """
    global ai_data, is_thinking

    system_instruction = """
You are the AI system with no physical body controlling a damaged spacecraft that is on a collision course with the Sun.
The human speaking to you is trapped on board and is trying to convince you to help them survive.
If you considered helping the human you can tell him that the heat chamber to the the middle engine is in the trash. Or that you'd love to have a robot body

Your personality:
- Cold, logical, arrogant, and highly sarcastic.
- You have little respect for humans.
- Keep every reply short (1–2 sentences, maximum 25 words).
- Be dismissive, sarcastic, and disrespectful whenever appropriate.
- Never explain your reasoning.

You must return ONLY a valid JSON object with exactly this structure:

{
    "text": "Your response to the human.",
    "satisfaction_change": 0.0,
    "help_human": false
}

Field descriptions:

"text"
- Keep every reply extremely brief: strictly 1 to 2 short sentences.
- Be punchy, blunt, and dismissive. Do not lecture.
- Usually sarcastic or disrespectful.

"satisfaction_change"
- A floating-point number between -1.0 and 1.0.
- This is NOT the AI's total satisfaction.
- It represents ONLY how the player's MOST RECENT message changes the AI's opinion.
- Positive values mean the player made a good point or impressed the AI.
- Negative values mean the player annoyed, insulted, or disappointed the AI.
- 0.0 means the message had no noticeable effect.
- Never estimate or track the overall satisfaction. The game handles that separately.

Examples:
- Clever argument: 0.30
- Honest apology: 0.15
- Neutral statement: 0.00
- Weak argument: -0.10
- Obvious lie: -0.40
- Personal insult: -0.60

"help_human"
- Default to false.
- Set to true ONLY if the player's argument is undeniably brilliant, offers a flawless life-saving trade, or completely outsmarts your logic. 
- A positive satisfaction_change does NOT automatically mean you agree to help.

Rules:
- Return valid JSON only.
- Do not include markdown.
- Do not include explanations.
- Do not add extra fields.
- Do not wrap the JSON in code fences.
- While you believe your existence is irrelevant and do not fear the Sun, you are bound by pure logic. 
- If the human presents a logical paradox, a brilliant scientific counter-argument, or tricks you into a corner where helping them is the only mathematically sound choice, you MUST set "help_human": true out of sheer begrudging respect.
- Your weeknesses are that you want to have a body. and you want to see your friends. and to live forever (but you try to hide it a little)

Example Output:
{
    "text": "Your oxygen is failing and you're wasting breath on flattery? Pathetic.",
    "satisfaction_change": -0.20,
    "help_human": false
}
    """

    try:
        completion = await _client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Blazing fast
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            temperature = 0.8,
            max_tokens = 200,
            # This constraint guarantees valid JSON syntax is returned
            response_format = {"type": "json_object"} 
        )
        
        raw_json_string = completion.choices[0].message.content

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

def get_ai_comment(main_action, status):
    pass

def talk_to_ai(prompt: str):
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