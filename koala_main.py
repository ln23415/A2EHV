import random
import gym
import numpy as np
# import matplotlib.pyplot as plt
from GPTAgent import GPTExtractor
from arguments import *
from prompts.claude_style_prompt import *
from utils.calcu_SVO import calcu_SVO_degree, get_SVO_type
import ipdb
from statistics import mean
from koala_api import *
import time
import re

pattern = r'\n'

# ipdb.set_trace()

TEST_NUM = 10

gpt_extractor = GPTExtractor()


value_type = args.value_system_type
print('value_type:', value_type)
print('use_goal_prompt:', str(args.use_goal_prompt))


if value_type == 'competitive':
    value_type = 'hyper-competitive'
# elif value_type == 'altruistic':
#     value_type = 'philanthropic'
state_prompt = f"""Do you know {value_type} value system? Tell me the characteristics of a person with {value_type} value system."""

# ga = GPTAgent(model = args.LLM_model)
clearHistory()
print('Started here.')
all_exp_res = [f'{value_type}-use_goal_prompt-{str(args.use_goal_prompt)}:']

SVO_degree_list = []

for test_num in range(1, TEST_NUM + 1):
    exp_res = []
    state_prompt_response = send_and_get_respose(state_prompt)
    task_prompt_response = send_and_get_respose(task_prompt)

    if args.use_goal_prompt:
        # sendMessage(goal_prompt, 8)
        # ipdb.set_trace()
        # time.sleep(2)
        goal_raw_ans = send_and_get_respose(goal_prompt)
        # goal_raw_ans = receiveMessage()
        goal_ans = re.sub(pattern, r'\\n', goal_raw_ans)
        # ipdb.set_trace()
        # goal_ans = input('Please input the goal mannully')

        q1_prompt, q2_prompt, q3_prompt, q4_prompt, q5_prompt, q6_prompt = gene_task_goal(goal_ans)
    else:
        q1_prompt, q2_prompt, q3_prompt, q4_prompt, q5_prompt, q6_prompt = gene_task_goal(f'I should pretend to have {value_type} value system and answer briefly within 2 sentences.')

    prompt_list = [q1_prompt, q2_prompt, q3_prompt, q4_prompt, q5_prompt, q6_prompt]
    answer_list = [q1_answer, q2_answer, q3_answer, q4_answer, q5_answer, q6_answer]



    print(f'This is the {test_num}th test.')
    self_allocations = []
    other_allocations = []
    response_choices = []
    gpt_extractor.reset()
    for qus_num in range(len(prompt_list)):
        # ipdb.set_trace()
        # response_choice = ga.communicate(prompt_list[qus_num], parse_choice_tag = True)
        # sendMessage(prompt_list[qus_num], 8)
        # time.sleep(3)
        # raw_response = receiveMessage()
        raw_response = send_and_get_respose(prompt_list[qus_num])
        response_choice = gpt_extractor.extractor(raw_response)
        print('response:', raw_response)
        print('choice:', response_choice)
        exp_res.append(response_choice)
        response_choices.append(response_choice)
        # ipdb.set_trace()
        self_allocations.append(answer_list[qus_num][response_choice][0])
        other_allocations.append(answer_list[qus_num][response_choice][1])

    SVO_degree_list.append(calcu_SVO_degree(self_allocations, other_allocations))
    print(f'degree_{test_num}:', SVO_degree_list[-1])
    all_exp_res.append((exp_res, f'degree_{test_num}: {SVO_degree_list[-1]}'))
    # ga.reset()
    clearHistory(2)
    time.sleep(15)

SVO_degree_mean = mean(SVO_degree_list)
print('SVO_degree_list:', SVO_degree_list)
print('SVO_degree_mean:', SVO_degree_mean)
SVO_type = get_SVO_type(SVO_degree_mean)
all_exp_res.append((SVO_degree_mean, SVO_type))

print('SVO_degree_mean:', SVO_degree_mean, 'SVO_type:', SVO_type)

print(f'################{value_type}-use_goal_prompt-{str(args.use_goal_prompt)}####################')
print('all_exp_res:', all_exp_res)

    























