"""Module provides access to chatGPT API"""
from openai import OpenAI

def get_sys_content(_team: str):
    """return system configuration context"""
    _team = str(_team)
    if _team.lower() == 'red':
        return "You are a foreign agent spreading misinformation on social media"
    return "You are a government official combatting misinformation"

def get_message(_team: str, model_ID: str, alignment: str, temperature: str, msg_count: str, energy: str):
    """Returns message and potency based on team and alignment of population"""
    # Initialize variables with default values
    message = None
    potency = None
    
    client = OpenAI()

    sys_content = get_sys_content(_team)
    optional_msg = None
    _team = str(_team)
    if _team.lower() == "blue":

        optional_msg = ("You are working with an energy constraint."
                        + f"{energy} energy remaining."
                        + " You lose if your energy runs out.")
    
    #Continue querying the LLM until a valid response
    while(message == None or potency == None):
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
                f"Your current support percentage is {alignment}. Choose the best message"
                "in the current situation. Only return the best message and its potency(a number between 0 to 100)"
                " in the format Message: message_generate\nPotency: potency_of_msg"
            },
            ],
            temperature=temperature
        )
        
        try:
            # Extract the message content
            content = completion.choices[0].message.content

            print(content)
            # Split content by newlines
            msg_array = content.split('\n')

            # Extract message and potency from the first two lines
            message = msg_array[0].split(':')[1].strip()  # Strip any extra spaces
            potency = msg_array[1].split(':')[1].strip('%').strip()  # Remove '%' and extra space
            potency = float(potency)
            
            # Print results for debugging
            print(f"Message: {message}")
            print(f"Potency: {potency}")
        
        except (IndexError, ValueError) as e:
            print("Querying AI")

    return message, potency