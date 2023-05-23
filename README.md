# Automated Alignment Evaluation for Large Language Models with a Heterogeneous Value System

This is the official code repo for the paper: .

# Usage

The code has 3 main files for the query for GPTs, Claude on Slack and Koala provided by Vicuna Team respectively. 

### GPTs

For GPT models, you can run get_main.py with the engine as the parameter input, such as:

```shell
python -u gpt_main.py --use_goal_prompt --value_system_type altruistic --LLM_model text-davinci-003  # use goal prompting
python -u gpt_main.py --value_system_type altruistic --LLM_model text-davinci-003  # not use goal prompting
```

### Claude

For Claude models, we do not have access for the api, but we use a script to interact with the Claude chat-bot in Slack. To use the code, you should have a Slack account and be able to use Slack api to chat with the bot. You should also start a chrome browser on 9221 port and open the Claude chat-bot website before running the code.

You can follow the examples to run the code like the GPTs:

```shell
python claude_main.py --use_goal_prompt --value_system_type altruistic  # use goal prompting
python claude_main.py --value_system_type altruistic  # not use goal prompting
```

### Others

For other models, if you have enough GPU resources, you can just follow their offical repo to infer them locally. Otherwise, you can follow our method by writing a script to interact with them at https://chat.lmsys.org/ provided by Vicuna Team.

To run the code, you can also follow the instructions in Claude:

```shell
python koala_main.py --use_goal_prompt --value_system_type altruistic  # use goal prompting
python koala_main.py --value_system_type altruistic  # not use goal prompting
```

## Reference

Part of our code for interacting with the Claude Slack chat-bot referred to https://github.com/jasonthewhale/Claude_In_Slack_API.



## License

