import concurrent.futures
import json
import os
from typing import List, Dict
from openai import OpenAI
import re
from datetime import datetime
import asyncio
path = "/root/autodl-tmp/formal/datasets/CMIN-CN/news_score"
companies = os.listdir(path)
path_score = "/root/autodl-tmp/formal/datasets/CMIN-CN/news_score"
path_to = "/root/autodl-tmp/formal/datasets/CMIN-CN/news_score"
client = OpenAI(
    api_key = "",    
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
prompt = "As a stock trading news analyst, you are a helpful and precise assistant. Your task is to analyze news impact on stocks Using 10 measurable dimensions with standardized scoring. Give an overall score for all news, and scores list for each news"
default_prompt = """
    Analyze the provided stock-related news Using these scoring dimensions:\
    Correlation: <0-10> News-to-stock relevance
    Sentiment: <0-10> Polarity strength
    Importance: <0-10> Event significance
    Impact: <0-10> Price movement magnitude
    Duration: <0-10> Effect timespan
    Entity_Density: <0-10> Frequency of company/ticker mentions
    Market_Scope: <0-10> Sector-wide vs company-specific
    Time_Proximity: <0-10> News time vs market hours
    Headline_Structure: <0-10> Attention-grabbing elements
    Source_Recency: <0-10> Time decay since event occurrence

    Scoring Rules:
    All factors scored 0-10
    Higher values = stronger effects
    Never return all zeros (minimum 1 where applicable)
    Score all applicable factors (skip only if truly irrelevant)
    Output format:
    {
        "Each_item":[
            {
            "News_content:""
            "Correlation": <0-10>
            "Sentiment": <0-10>
            "Importance": <0-10>
            "Impact": <0-10>
            "Duration": <0-10>
            "Entity_Density": <0-10>
            "Market_Scope": <0-10>
            "Time_Proximity": <0-10>
            "Headline_Structure": <0-10>
            "Source_Recency": <0-10>
            }
        ]
    }
    please return only the json with standard format, without ```json``` or ellipsis '...'
    """

def extract(input1):
    try:
        response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": default_prompt},
                        {"role": "user", "content": input1}
                    ],
                    temperature=0.3,
                    stream=False
                )
        res1 = response.choices[0].message.content
        return res1
    except Exception as e:
        try:
            response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": default_prompt},
                        {"role": "user", "content": input1}
                    ],
                    temperature=0.3,
                    stream=False
                )
            res1 = response.choices[0].message.content
            return res1
        except Exception as e:
            print(e,"95**")
# def is_zero(path):
#     with open(path,"r")as f:
#         data_json = json.load(f)
#         f.close()
#     for k in range(len(data_json[0])):
#         scores = data_json[0][k]["scores"]
#         sum1 = 0
#         for key in scores:
#             if key !="News_content":
#                 sum1 += scores[key]
#         if sum1 == 0:
#             return True
#     return False
# path1 = "./extracted"
# def fun(comp):
#     path_file = os.path.join(path1,comp)
#     files = os.listdir(path_file)
#     all_dates_news = []
#     for file in files:
#         try: 
#             if is_zero(os.path.join(path_to,comp,file)) :
#                 path2 = os.path.join(path_file,file)
#                 with open(path2,"r")as f:
#                     data_json = json.load(f)
#                     f.close()
#                 print(path_file,file)
#                 all_news = data_json[file.replace(".json","")]
             
#                 if len(all_news)>0:
#                     news_ext = []
#                     all_ids = []  
#                     k = 0 
#                     for news in all_news[0]:
#                         test = None
#                         if 'original_text' in news:
#                             data = news['original_text']
#                         else:
#                             data = news['orginal_text']
#                             news['original_text'] = data
#                         flag = 0
                        
#                         if os.path.exists(os.path.join(path_score,comp,file)):
#                             with open(os.path.join(path_score,comp,file),"r")as f:
#                                 data_json = json.load(f)
#                                 f.close()
#                             all_scores = data_json['Each_item']
#                             for score1 in all_scores:
#                                 if score1['News_content'].replace(" ","") == data.replace(" ",""):
#                                     print("replace")
#                                     del score1['News_content']
#                                     temp = score1
#                                     news['scores'] = temp
#                                     flag = 1
#                         if flag == 0:
#                             # print(data)
#                             news_ext.append(data.replace('\xa0', ' '))
#                             all_ids.append(k)
#                         k+=1
#                     if len(news_ext)>0:
#                         input1 = str(news_ext)
#                         all_dates_news.append(input1)
#                         try:
#                             result = extract(input1)
#                             print(f"收到结果: {result}")
#                             test = json.loads(result)
#                         except Exception as e:
#                             # print(e)
#                             news['scores'] = {
#                             "Correlation":0,
#                             "Sentiment":0,
#                             "Importance":0,
#                             "Impact":0,
#                             "Duration":0,
#                             "Entity_Density":0,
#                             "Market_Scope":0,
#                             "Time_Proximity":0,
#                             "Headline_Structure":0,
#                             "Source_Recency":0
#                             }
#                         try:
#                             assert len(test['Each_item']) == len(news_ext)
#                         except:
#                             if test is not None and len(news_ext)==1:
#                                 test['Each_item'] = test['Each_item'][:1]
#                             del_ids = []
#                             if test is not None and len(test['Each_item'])<len(news_ext):
#                                 for k in range(len(news_ext)):
#                                     if news_ext[k] in [b['News_content'] for b in test['Each_item']]:
#                                         pass
#                                     else:
#                                         del_ids.append(k)
#                                 if len(del_ids)!=0:
#                                     del_ids.reverse()
#                                     for id in del_ids:
#                                         del news_ext[id]
#                                         del all_ids[id]
#                         for news_id in range(len(all_news[0])):
#                             all_news[0][news_id]
#                             if news_id in all_ids:
#                                 id1 = all_ids.index(news_id)
#                                 # print(news_id,id1,len(test['Each_item']))
#                                 if test is not None:
#                                     all_news[0][news_id]['scores'] = test['Each_item'][id1]
#                                 else:
#                                     all_news[0][news_id]['scores'] =  {
#                                 "Correlation":0,
#                                 "Sentiment":0,
#                                 "Importance":0,
#                                 "Impact":0,
#                                 "Duration":0,
#                                 "Entity_Density":0,
#                                 "Market_Scope":0,
#                                 "Time_Proximity":0,
#                                 "Headline_Structure":0,
#                                 "Source_Recency":0
#                                 }
                                
#                     # print(all_news[0])
#                     with open(os.path.join(path_to,comp,file),"w",encoding='utf-8')as f:
#                         json.dump(all_news, f, ensure_ascii=False, indent=4)
#         except Exception as e:
#             # raise e
#             pass

# def main():
#     with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
#         for comp in companies:
#             executor.submit(fun, comp)   
# main()
default_prompt = """
    Analyze the provided stock-related news Using these scoring dimensions:\
    Correlation: <0-10> News-to-stock relevance
    Sentiment: <0-10> Polarity strength
    Importance: <0-10> Event significance
    Impact: <0-10> Price movement magnitude
    Duration: <0-10> Effect timespan
    Entity_Density: <0-10> Frequency of company/ticker mentions
    Market_Scope: <0-10> Sector-wide vs company-specific
    Time_Proximity: <0-10> News time vs market hours
    Headline_Structure: <0-10> Attention-grabbing elements
    Source_Recency: <0-10> Time decay since event occurrence

    Scoring Rules:
    All factors scored 0-10
    Higher values = stronger effects
    Never return all zeros (minimum 1 where applicable)
    Score all applicable factors (skip only if truly irrelevant)
    Output format:
       {
            "News_content:""
            "Correlation": <0-10>
            "Sentiment": <0-10>
            "Importance": <0-10>
            "Impact": <0-10>
            "Duration": <0-10>
            "Entity_Density": <0-10>
            "Market_Scope": <0-10>
            "Time_Proximity": <0-10>
            "Headline_Structure": <0-10>
            "Source_Recency": <0-10>
        }
    please return only the json with standard format, without ```json``` or ellipsis '...'
    """
def is_zero1(path):
    with open(path,"r")as f:
        data_json = json.load(f)
        f.close()
    k_all = []
    for k in range(len(data_json[0])):
        scores = data_json[0][k]["scores"]
        sum1 = 0
        for key in scores:
            if key !="News_content":
                sum1 += scores[key]
        if sum1 == 0:
            # return True,k
            k_all.append(k)
    if len(k_all)!=0:
        return True,k_all
    return False,-1
def extract2(input1):
    try:
        response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": default_prompt},
                        {"role": "user", "content": input1}
                    ],
                    temperature=0.3,
                    stream=False
                )
        res1 = response.choices[0].message.content
        return res1
    except Exception as e:
        try:
            response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": default_prompt},
                        {"role": "user", "content": input1}
                    ],
                    temperature=0.3,
                    stream=False
                )
            res1 = response.choices[0].message.content
            return res1
        except Exception as e:
            print(e,"95**")

path_from = "/root/autodl-tmp/formal/datasets/zero"
files = os.listdir(path_from)
for file in files:
    path_file = os.path.join(path_from,file)
    tf, k = is_zero1(path_file)
    if tf:
        with open(path_file,"r")as f:
            data_json = json.load(f)
            f.close()
        if not os.path.exists(os.path.join("/root/autodl-tmp/formal/datasets/zero_to",file)):
            for kk in k:
                try:
                    res = extract2(data_json[0][kk]["original_text"])
                    data_json[0][kk]["scores"] = json.loads(res)
                    # print(data_json)
                    with open(os.path.join("/root/autodl-tmp/formal/datasets/zero_to",file),"w",encoding='utf-8')as f:
                        json.dump(data_json, f, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(e,"98**")


        
