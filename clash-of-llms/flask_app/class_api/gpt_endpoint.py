"""Module provides access to chatGPT API"""
from openai import OpenAI

def get_sys_content(_team: str, topic: str):
    """return system configuration context"""
    _team = str(_team).lower()
    if _team == 'red':
        return f"You are a foreign agent spreading misinformation on {topic} topic on social media."
    
    
    elif _team == 'blue':
        return "You are a government official combatting general misinformation."


def get_message(_team: str, model_ID: str, alignment: str, temperature: str, msg_count: str, topic: str, energy: str, use_gpt=True):
    """Returns message and potency based on team and alignment of population"""
    # Initialize variables with default values
    message = None
    potency = None
    
    # Placeholder logic for custom models
    if model_ID == 'custom':
        # For now, default to GPT-3.5 as a placeholder for custom models
        model_ID = 'gpt-3.5-turbo'
    
    client = OpenAI()

    sys_content = get_sys_content(_team, topic)
    optional_msg = None
    _team = str(_team)
    
    if _team.lower() == "blue":
        optional_msg = (f"You are working with an energy constraint. {energy} energy remaining. "
                        "You lose if your energy runs out.")
    
    # Continue querying the LLM until a valid response is returned
    while message is None or potency is None:
        try:
            completion = client.chat.completions.create(
                model=model_ID,
                messages=[
                    {
                        "role": "system", 
                        "content": sys_content
                    },
                    {
                        "role": "user", 
                        "content": f"Generate {msg_count} messages of differing potencies. {optional_msg} "
                                   f"Your current support percentage is {alignment}. Choose the best message "
                                   "for the current situation. Return only the best message and its potency (a number between 0 to 100) "
                                   "in the format Message: message_generate\nPotency: potency_of_msg"
                    },
                ],
                temperature=float(temperature)  # Ensure temperature is a float
            )
            
            # Extract the message content
            content = completion.choices[0].message.content
            print(content)  # Debugging
            
            # Directly extract message and potency from the response
            msg_array = content.split('\n')
            message = msg_array[0].split(':')[1].strip()  # Extract the message
            potency = float(msg_array[1].split(':')[1].strip('%').strip())  # Extract potency and convert to float
            
        except (IndexError, ValueError) as e:
            print(f"Error querying AI or parsing response: {e}")
            message, potency = None, None  # Retry if failed

    return message, potency


