import json

from request import fetch_api

# Hypothetical function to get a response from Model A
user_api = ""  #"http://10.155.106.208:22120/chat"
system_api = ""

user_template = {
    "model": "gpt-4o-mini",
    "temperature": 0.5,
    "top_p": 1,
    "n": 1,
    "stream": False,
    "stop": None,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "logit_bias": {},
    "messages": [
        {
            "role": "system",
            "content": "Assume you are an user who dialogue with a system which aims to enrich prompt for text to image generation, make suitable selection according to the option it provided, or ask it to combine all options based on your situation. your answer must be concise! "
                       "e.g. system: To create a more captivating image, would you like the portrait to be realistic or stylized? your anser: Realistic, please. Or you can answer: A mix of both is ok"
        },
        {
            "role": "user",
            "content": ""
        }
    ]
}

system_template = {
    "model": "promptModi",
    "temperature": 0.5,
    "top_p": 1,
    "n": 1,
    "stream": False,
    "stop": None,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "logit_bias": {},
    "messages": [
        {
            "role": "user",
            "content": ""
        }
    ]
}

def llm_response(prompt, template, model_api):
    # Replace this with actual API call to Model A
    result = fetch_api(prompt, template, model_api)
    return result

def single_turn(data):
    dialogue = []
    turns = data['dialogue']

    context = turns[0]['content']
    response = llm_response(context, system_template, system_api)
    dialogue.append({"role": "user", "content": context})
    dialogue.append({"role": "assistant", "content": response})

        # Pause for readability (optional)
        # time.sleep(1)

    return {"dialogue": dialogue}

def single_turn_dialogue(data):
    dialogue = []
    context = data['raw_prompt']

    turns_num = 12

    for turn in range(turns_num+1):
        if turn == 0:
            #instrution

            response = llm_response(context, system_template, system_api)
            dialogue.append({"user": context})
            dialogue.append({"system": response})
        elif turn % 2 == 1:
            # user's turn
            response = llm_response(context, user_template, user_api)
            # print(f"user: {response}")
            if turn == 11:
                # user's turn
                response += " Then, summarize the prompt for me."
            dialogue.append({"user": response})
        else:
            # system's turn
            response = llm_response(context, system_template, system_api)
            # print(f"system: {response}")
            dialogue.append({"system": response})

        # Add the response to the context
        context += f" {response}"

        # Pause for readability (optional)
        # time.sleep(1)

    return dialogue


def multi_turn_dialogue(data):
    dialogue = []
    turns = data['dialogue']

    context = turns[0]['content']

    turns_num = 22

    for turn in range(turns_num+1):
        if turn == 0:
            #instrution
            response = llm_response(context, system_template, system_api)
            dialogue.append({"role": "user", "content": context})
            dialogue.append({"role": "assistant", "content": response})

        elif turn % 2 == 1:
            # user's turn
            response = llm_response(context, user_template, user_api)
            # print(f"user: {response}")
            if turn == 21:
                # user's turn
                response += " Then, summarize the prompt for me."
            dialogue.append({"role": "user", "content": response})

        else:
            # system's turn
            response = llm_response(context, system_template, system_api)
            # print(f"system: {response}")
            dialogue.append({"role": "assistant", "content": response})

        # Add the response to the context
        context += f" {response}"

    return {"dialogue": dialogue}

data_path = 'dialogue/data/pe_200.json'
result_path = 'pe_200-result.json'

samples = json.load(open(data_path))

dialogues = []

for turn,sample in enumerate(samples):
    print("current turn is: {}".format(turn))
    dialogue = single_turn_dialogue(sample) #multi_turn_dialogue(sample) # #single_turn(sample)
    dialogues.append(dialogue)

with open(result_path, mode='a') as f:
    json.dump(dialogues, f, indent=4, ensure_ascii=False)

