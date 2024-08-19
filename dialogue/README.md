# README
To evaluate the user-friendly degree for a batch of multi-turn samples, we adopt gpt4-o as judgement tool with a fair and objective prompt which included in `evaluation.py`.

## Usage
Prepare a ChatGPT API and template, here is the template demo:
```bash
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
```
Then run the following script
```bash
python evaluation.py --first-dialogue --sec-dialogue --result-path --api
```

2. Score calculation
```bash
python setup.py develop
```
