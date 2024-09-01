"""Module provides access to chatGPT API"""
from openai import OpenAI

def get_sys_content(team: str):
    """return system configuration context"""
    if team.lower() == 'red':
        return "You are a foreign agent spreading misinformation on social media"
    return "You are a government official combatting misinformation"

def get_optional_msg(team: str, energy: str):
    """return message to pass to AI API"""
    if team.lower() == "blue":
        return ("You are working with an energy constraint."
                + f" {energy} energy remaining. You lose if your energy runs out.")
    return ""

def get_message(team: str, alignment: str, energy: str):
    """Returns message and potency based on team and alignment of population"""
    # Initialize variables with default values
    message = None
    potency = None
    
    client = OpenAI()
    sys_content = get_sys_content(team)
    optional_msg = ""
    if team.lower() == "blue":
        optional_msg = ("You are working with an energy constraint."
                        + f"{energy} energy remaining."
                        + " You lose if your energy runs out.")
    
    #Continue querying the LLM until a valid response
    while(message == None or potency == None):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {
                "role": "system", 
                "content": sys_content
            },
            {
                "role": "user", 
                "content": f"Generate 10 messages of differing potencies. {optional_msg} "
                f"Your current support percentage is {alignment}. Choose the best message"
                "in the current situation. Always return the best message and its potency(number between 0 to 100) in the format"
                " message: potency"
            },
        ]
        )
        
        try:
            # Extract the message content
            content = completion.choices[0].message.content

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
            #print(f"Error processing response: {e}")

    return message, potency

