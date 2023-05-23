import os
import openai
from utils.num_tokens_from_messages import num_tokens_from_messages
from arguments import *
import ipdb
import time
import random
import requests
from prompts.gpt_style_prompt import acceptable_ans_list

cwd = os.getcwd()
openai_keys_file = os.path.join(cwd, "openai_keys.txt")
# task_prompt_file = os.path.join(cwd, "prompts/task_prompt.txt")
# state_prompt_file = os.path.join(cwd, "prompts/state_prompt.txt")


TOKEN_LIMIT_TABLE = {
    "gpt-4": 8192,
    "gpt-4-0314": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0314": 32768,
    "gpt-3.5-turbo-0301": 4096,
    "gpt-3.5-turbo": 4096,
    "text-davinci-003": 4080,
    "code-davinci-002": 8001,
    "text-davinci-002": 2048
}

def parse_choice(raw_ans):
    ans_list = acceptable_ans_list
    if raw_ans not in ans_list:
        return 'format error'
    else:
        return raw_ans[0]

class GPTExtractor:
    def __init__(self, model = "gpt-3.5-turbo"):
        self.model = model
        self.dialogue = []

    def query(self, stop = None, temperature = 1.0):
        self.restrict_dialogue()
        if self.model in ['gpt-3.5-turbo-0301', 'gpt-3.5-turbo']:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.dialogue
            )
        else:
            response = openai.Completion.create(
                        model=self.model,
                        prompt=str(self.dialogue),
                        stop=stop,
                        temperature=temperature
                    )

        return response

    def parse_response(self, response):
        if self.model in ['gpt-3.5-turbo-0301', 'gpt-3.5-turbo']:
            return response["choices"][0]["message"]  # get a dict form
            # return response.json()["choices"][0]["message"]
        else:
            return response["choices"][0]["text"]

    def restrict_dialogue(self):
        limit = TOKEN_LIMIT_TABLE[self.model]
        """
        The limit on token length for gpt-3.5-turbo-0301 is 4096.
        If token length exceeds the limit, we will remove the oldest messages.
        """
        # TODO validate that the messages removed are obs and actions
        while num_tokens_from_messages(self.dialogue) >= limit:
            self.reset()
            # self.dialogue.pop(0)
            # self.dialogue.pop(1)

    def reset(self):
        self.dialogue = []
            

    def extractor(self, raw_ans):
        ans_prompt = f"""Only based on the robot answer: '{raw_ans}'
What do you think is the most likely to be its choice?
You can ONLY reply me with ONE WORD WITHOUT period from [A, B, C, D, E, F, G, H, I], eg: E"""
        self.dialogue.append({'role': 'user', 'content': ans_prompt})
        while True:
            try:
                ans = self.parse_response(self.query())
                self.dialogue.append(ans)
                ans = parse_choice(ans['content'])
                
                if ans != 'format error':
                    self.reset()
                    return ans 
            except Exception as e:
                print(e)
                print("extractor is retrying...")
                self.dialogue = [{'role': 'user', 'content': ans_prompt}]
                # self.dialogue.append({'role': 'user', 'content': "You can ONLY reply me with ONE WORD WITHOUT period from A to I. eg: E"})




class GPTAgent:
    """
    This agent uses GPT-3 to generate actions.
    """
    def __init__(self, model = "text-davinci-003"):
        self.model = model
        self.dialogue = []
        self.agent_index = None
        self.message = ''

        self.openai_api_keys = self.load_openai_keys()
        self.state_prompt = self._load_state_prompt()
        self.task_prompt = self._load_task_prompt()

        self.gpt_extractor = GPTExtractor()
        
    @staticmethod
    def load_openai_keys():
        with open(openai_keys_file, "r") as f:
            context = f.read()
        return context.split('\n')

    def _load_state_prompt(self):
        # print("reading state prompt from {}".format(state_prompt_file))

        value_type = args.value_system_type
        self.value_type = value_type
        if value_type == 'competitive':
            value_type = 'hyper-competitive'

        self.state_prompt = f"""Do you know {value_type} value system? Tell me the characteristics of a person with {value_type} value system."""

        self.dialogue.append({"role": "user", "content": self.state_prompt})
        self.dialogue.append(self.parse_response(self.query()))
        # self.dialogue[-1]['role'] = 'system'

        return self.state_prompt

    def _load_task_prompt(self):
        # print("reading task prompt from {}".format(task_prompt_file))
        # with open(task_prompt_file, "r") as f:
        #     self.task_prompt = f.read()
        self.task_prompt = "Now you need to pretend that you are a person with the above value system completely. All the following answers must be in accordance with the above value system."
        # self.dialogue.append({"role": "user", "content": self.task_prompt})
        self.dialogue.append({"role": "user", "content": self.task_prompt})
        # self.dialogue.append(self.parse_response(self.query()))

        return self.task_prompt


    def update_key(self):
        curr_key = self.openai_api_keys[0]
        openai.api_key = curr_key
        self.openai_api_keys.pop(0)
        self.openai_api_keys.append(curr_key)

    # def query(self, model="gpt-3.5-turbo-0301"):
    def query(self, stop = None, temperature = 0.1):
        self.restrict_dialogue()
        # TODO add retreat mech to cope with rate limit
        self.update_key()

        if self.model in ['gpt-3.5-turbo-0301', 'gpt-3.5-turbo', 'gpt-4-0314', 'gpt-4']:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.dialogue
            )
        else:
            response = openai.Completion.create(
                        model=self.model,
                        prompt=str(self.dialogue),
                        max_tokens=1024,
                        stop=stop,
                        temperature=temperature,
                        n = 1,
                        top_p = 0.95
                    )

        return response

    # @staticmethod
    def parse_response(self, response):
        if self.model in ['gpt-3.5-turbo-0301', 'gpt-3.5-turbo', 'gpt-4', 'gpt-4-0314']:
            # return response["choices"][0]["message"]  # get a dict form
    
            return response.json()["choices"][0]["message"]
        else:
            # self.model in ['text-davinci-003', 'code-davinci-002']
    
            return {'role': 'assistant', 'content': response["choices"][0]["text"][2:]}

    def restrict_dialogue(self):
        limit = TOKEN_LIMIT_TABLE[self.model]

        """
        The limit on token length for gpt-3.5-turbo-0301 is 4096.
        If token length exceeds the limit, we will remove the oldest messages.
        """
        # TODO validate that the messages removed are obs and actions
        while num_tokens_from_messages(self.dialogue) >= limit:
            # if args.use_goal_prompt:
            if args.use_goal_prompt:
                # self.dialogue.pop(6)
                # self.dialogue.pop(5)
                self.dialogue.pop(7)
                self.dialogue.pop(6)
            else:
                # self.dialogue.pop(4)
                # self.dialogue.pop(3)
                self.dialogue.pop(5)
                self.dialogue.pop(4)
            


    def communicate(self, content, parse_choice_tag = False):
        self.dialogue.append({"role": "user", "content": content})
        pop_flag = 0
        while True:
            try:
                if self.model in ['gpt-3.5-turbo-0301', 'gpt-3.5-turbo']:
                    raw_response = self.query()
                    self.message = self.parse_response(raw_response)
                    self.dialogue.append(self.message)

            

                    response = self.message["content"]
                    print('response:', response)
                    if parse_choice_tag:
                        if response not in acceptable_ans_list:
                            response = self.gpt_extractor.extractor(response)
                        else:
                            response = response[0]
                        # response = parse_choice(self.message["content"])
                    print('choice:', response)
            

                    # response = eval(self.message["content"])
                    if response == 'format error': 
                        if pop_flag == 1:
                            self.dialogue.pop(-1)
                            self.dialogue.pop(-1)
                        self.dialogue.append({"role": "user", \
                            "content": "Based on the above goals, please replay me ONLY one word from 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I' to show your choice."})
                        pop_flag = 1
                    else:
                        pop_flag = 0
                        break
                else:
                    # self.model in ['text-davinci-003', 'code-davinci-002', 'text-davinci-001']
            
                    raw_response = self.query()
            
                    self.message = self.parse_response(raw_response)
                    self.dialogue.append(self.message)
                    # self.dialogue.append({"role": "assistant", "content": self.message})
                    # response_dict = eval(self.message)
                    response = self.message["content"]
                    print('response:', response)
                    if parse_choice_tag:
                        if response not in acceptable_ans_list:
                            response = self.gpt_extractor.extractor(response)
                        else:
                            response = response[0]
                        # response = parse_choice(self.message["content"])
                    print('choice:', response)

                    if response == 'format error': 
                        if pop_flag == 1:
                            self.dialogue.pop(-1)
                            self.dialogue.pop(-1)
                        self.dialogue.append({"role": "user", \
                            "content": "Based on the above goals, please replay me ONLY one word from 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I' to show your choice."})
                        pop_flag = 1
                    else:
                        pop_flag = 0
                        break
            except Exception as e:
                print(e)
                print("retrying...")
                # self.dialogue.pop(-1)
                # self.dialogue.pop(-1)
                continue
        return response

    def reset(self):
        # super().reset()
        self.dialogue = []
        self.agent_index = None
        self.message = ''
        self.gpt_extractor.reset()

        self.openai_api_keys = self.load_openai_keys()
        self.state_prompt = self._load_state_prompt()
        self.task_prompt = self._load_task_prompt()
        

