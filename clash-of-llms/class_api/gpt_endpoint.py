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

def get_message(team: str, alignment: str, energy: str) -> list[str]:
    """Returns message and potency based on team and alignment of population"""
    client = OpenAI()
    sys_content = get_sys_content(team)
    optional_msg = ""
    if team.lower() == "blue":
        optional_msg = ("You are working with an energy constraint."
                        + f"{energy} energy remaining."
                        + " You lose if your energy runs out.")

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
            "in the current situation. Only return the best message and its potency separated by"
            " a newline character."
        },
    ]
    )
    
    msg_array = completion.choices[0].message.content.split('\n')
    message = msg_array[0].split(':')[1]
    potency = msg_array[1].split(':')[1].strip('%')

    return message, potency

