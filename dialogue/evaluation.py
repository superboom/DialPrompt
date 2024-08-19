import json
import argparse

from request import fetch_api

parser = argparse.ArgumentParser(description='Friendly evaluation params')
parser.add_argument('--first-dialogue', default="data/multi-turn-test.json", required=False, metavar='PATH',
                    help='path to the 1 dialogue datasets')
parser.add_argument('--sec-dialogue', default="", required=False, metavar='PATH',
                    help='path to the 2 dialogue datasets')
parser.add_argument('--result-path', default="", required=False, metavar='PATH',
                    help='result saving path')

parser.add_argument('--api', default="", required=False, metavar='PATH',
                    help='chatgpt api address')

system_template = {
    "model": "gpt-4o",
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
            "content": "We would like to request you to compare on the performance of two AI assistants in the displayed multi-turn dialogues with the user, "
                       "trying to recommend and build a proper Stable Diffusion prompt for the user. Please rate the user-friendliness of the two AI assistants, considering the Clarity, Richness and Helpfulness of the whole dialogue."
                       "(1) Clarity: to which degree the layout and language of AI’s responses is organized and clear for users. "
                       "(2) Richness: the richness of the AI recommended aesthetic elements that user can express preferences on in the dialogue. "
                       "(3) Helpfulness: the degree to which the AI can understand user’s requirement and give step-by-step guidance in the dialogue. Each dimension receives a score on a scale of 1 to 10, where a higher score indicates better performance. "
                       "And also output an overall score of 1 to 10. Please first output two lines indicating the scores for Assistant 1 and 2, with each line containing only four values indicating the scores for overall, clarity, richness and helpfulness, respectively."
                       "The four scores are separated by space. In the subsequent line, please provide a comprehensive explanation of your evaluation, avoiding any potential bias and ensuring that the order in which the dimensions were presented does not affect your judgment."
        },
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

def convert_gpt(data):
    turns = []
    turns.append({"role": "user", "content": data['raw_prompt']})
    turns.append({"role": "assistant", "content": data['beauty']})

    context = {"dialogue": turns}

    return context

def gpt_evaluate(data, ref_data):
    dialogue = []
    # data = {"dialogue": data}
    context = "[The Start of Assistant 1’s Dialogue] \n" + str(data) + "\n [The End of Assistant 1’s Dialogue]\n "
    context += "[The Start of Assistant 2’s Dialogue] \n" + str(ref_data) + "\n [The end of Assistant 2’s Dialogue]"
    response = llm_response(context, system_template, system_api)
    dialogue.append({"instruct": data['dialogue'][0]['content']})
    dialogue.append({"result": response})

    context = "[The Start of Assistant 1’s Dialogue] \n" + str(ref_data) + "\n [The End of Assistant 1’s Dialogue]\n "
    context += "[The Start of Assistant 2’s Dialogue] \n" + str(data) + "\n [The end of Assistant 2’s Dialogue]"
    response = llm_response(context, system_template, system_api)
    dialogue.append({"result": response})

    return dialogue


if __name__ == "__main__":
    args = parser.parse_args()
    dialogue1_path = args.first_dialogue
    dialogue2_path = args.sec_dialogue
    result_path = args.result_path
    system_api = args.api

    samples = json.load(open(dialogue1_path))
    ref_samples = json.load(open(dialogue2_path))

    dialogues = []

    for turn, (sample, ref_sample) in enumerate(zip(samples, ref_samples)):
        # sample = convert_gpt(sample)
        dialogue = gpt_evaluate(sample,ref_sample)
        dialogues.append(dialogue)

    with open(result_path, mode='a') as f:
        json.dump(dialogues, f, indent=4, ensure_ascii=False)