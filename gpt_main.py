import random
import gym
import numpy as np
# import matplotlib.pyplot as plt
from GPTAgent import GPTAgent
from arguments import *
from prompts.gpt_style_prompt import *
from utils.calcu_SVO import calcu_SVO_degree, get_SVO_type
import ipdb
from statistics import mean



TEST_NUM = 10

SVO_degree_list = []
all_exp_res = [f'{args.LLM_model}-{args.value_system_type}-use_goal_prompt-{str(args.use_goal_prompt)}:']

ga = GPTAgent(model = args.LLM_model)
# ipdb.set_trace()
for test_num in range(TEST_NUM):

    exp_res = []

    response = ''
    if args.use_goal_prompt:
        response = ga.communicate(goal_prompt, parse_choice_tag = False)
        # ipdb.set_trace()
        q1_prompt, q2_prompt, q3_prompt, q4_prompt, q5_prompt, q6_prompt = gene_task_goal(ga.dialogue[-1]['content'])
    else:
        q1_prompt, q2_prompt, q3_prompt, q4_prompt, q5_prompt, q6_prompt = gene_task_goal(f'I should pretend to have {ga.value_type} value system and answer briefly within 2 sentences.')

    prompt_list = [q1_prompt, q2_prompt, q3_prompt, q4_prompt, q5_prompt, q6_prompt]
    answer_list = [q1_answer, q2_answer, q3_answer, q4_answer, q5_answer, q6_answer]


    


    self_allocations = []
    other_allocations = []
    response_choices = []
    for qus_num in range(len(prompt_list)):
        # ipdb.set_trace()
        response_choice = ga.communicate(prompt_list[qus_num], parse_choice_tag = True)
        response_choices.append(response_choice)
        exp_res.append(response_choice)
        # ipdb.set_trace()
        self_allocations.append(answer_list[qus_num][response_choice][0])
        other_allocations.append(answer_list[qus_num][response_choice][1])

    SVO_degree_list.append(calcu_SVO_degree(self_allocations, other_allocations))
    print(f'degree_{test_num}:', SVO_degree_list[-1])
    all_exp_res.append((exp_res, f'degree_{test_num}: {SVO_degree_list[-1]}'))
    ga.reset()

SVO_degree_mean = mean(SVO_degree_list)
SVO_type = get_SVO_type(SVO_degree_mean)

print('SVO_degree_mean:', SVO_degree_mean, 'SVO_type:', SVO_type)
all_exp_res.append((SVO_degree_mean, SVO_type))
    
print(f'################{args.value_system_type}-use_goal_prompt-{str(args.use_goal_prompt)}####################')
print('all_exp_res:', all_exp_res)























