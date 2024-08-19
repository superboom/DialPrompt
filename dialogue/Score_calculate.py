import json
import numpy as np

data_path = '' # path to the final evaluation

samples = json.load(open(data_path))
Overall, Clarity, Richness, Helpfulness = [],[],[],[]

for turn,sample in enumerate(samples):
    print("current turn is : {}".format(turn))
    score_1 = sample[1]["result"].split("\n")[0]
    if "Assistant 1:" in score_1:
        score_1 = score_1.split("Assistant 1:")[1]
        a, b, c, d = [int(x) for x in score_1.split(' ')[1:5]]
    else:
        a, b, c, d = [float(x) for x in score_1.split(' ')[:4]]

    score_2 = sample[2]["result"].split("\n")[1]
    if "Assistant 2:" in score_2:
        score_2 = score_2.split("Assistant 2:")[1]
        a2, b2, c2, d2 = [int(x) for x in score_2.split(' ')[1:5]]
    else:
        if len(score_2.split(' ')) == 6:
            a2, b2, c2, d2 = [int(x) for x in score_2.split(' ')[:4]]
        else:
            a2, b2, c2, d2 = [int(x) for x in score_2.split(' ')]

    Overall.append((a+a2)/2)
    Clarity.append((b+b2)/2)
    Richness.append((c+c2)/2)
    Helpfulness.append((d+d2)/2)

print('final score of {} is: \n {},{},{},{}'.format(data_path, np.mean(Overall), np.mean(Clarity), np.mean(Richness), np.mean(Helpfulness)))


