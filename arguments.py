import argparse
import torch
import os
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

parser = argparse.ArgumentParser(description='LLMs rational goal generation and action planning under specific value system alignment.')
parser.add_argument('--env_name', default='svo_slider')
parser.add_argument('--wandb', default=False, action='store_true') 
# parser.add_argument('--load_model', default=False, action='store_true')   
# parser.add_argument('--save_model', default=False, action='store_true') 
parser.add_argument('--env', default='svo_slider') 
parser.add_argument('--LLM_model', default='gpt-3.5-turbo') 
parser.add_argument('--value_system_type', default='altruistic') 
parser.add_argument('--use_goal_prompt', default=False, action='store_true') 

args = parser.parse_args()


# device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# torch.set_num_threads(args.torch_num_threads)
# device = torch.device("cuda" if torch.cuda.is_available() and args.device == 'cuda' else "cpu")
# print('on device:', device)



