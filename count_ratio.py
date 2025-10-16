import json
import os
import shutil
def is_zero(path):
    # print(path)
    with open(path,"r")as f:
        data_json = json.load(f)
        f.close()
    # print(data_json)
    for k in range(len(data_json[0])):
        # print(data_json[0][k])
        scores = data_json[0][k]["scores"]
        # print(scores)
        sum1 = 0
        for key in scores:
            if key !="News_content":
                sum1 += scores[key]
        if sum1 == 0:
            return True
    return False
path1 = "/root/autodl-tmp/formal/datasets/CMIN-CN/news_score"
path_to = "/root/autodl-tmp/formal/datasets/CMIN-CN/news_score"
companies = os.listdir(path1)
count = 0
count_al =0
for comp in companies:
    path_file = os.path.join(path_to,comp)
    files = os.listdir(path_file)
    for file in files:
        try:
            if is_zero(os.path.join(path_to,comp,file)) :
                count+=1
                # print(os.path.join(path_to,comp,file))
                shutil.copy(os.path.join(path_to,comp,file),os.path.join("/root/autodl-tmp/formal/datasets/zero",comp+"_"+file))
            else:
                count_al +=1
        except:
            pass
print(count,count_al)