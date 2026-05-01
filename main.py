# -*- coding: utf-8 -*-
import json
import os
import sys
from dotenv import load_dotenv
import anthropic


from prompts import SYSTEM_PROMPT, TOOL_DEFINITIONS
from tools import dispatch
from safety import check_free_text, escalate

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
MODEL = 'claude-opus-4-5'

def run_agent_turn(conversation):
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_DEFINITIONS,
            messages=conversation,
        )
        conversation.append({'role': 'assistant', 'content': response.content})
        for block in response.content:
            if hasattr(block, 'text') and block.text.strip():
                print('\nAssistant: ' + block.text.strip() + '\n')
        if response.stop_reason == 'end_turn':
            return conversation, False
        if response.stop_reason == 'tool_use':
            tool_results = []
            for block in response.content:
                if block.type != 'tool_use':
                    continue
                print('  [tool: ' + block.name + ']')
                result_str = dispatch(block.name, block.input)
                result = json.loads(result_str)
                if block.name == 'score_phq9' and result.get('crisis_flag'):
                    escalate()
                    return conversation, True
                tool_results.append({
                    'type': 'tool_result',
                    'tool_use_id': block.id,
                    'content': result_str,
                })
            conversation.append({'role': 'user', 'content': tool_results})

def main():
    print('\n' + '='*50)
    print('  Wellbeing Screening - University of Lucerne')
    print('  Confidential - Not a diagnosis')
    print('='*50)
    print('  Type quit to exit.\n')
    conversation = [{'role': 'user', 'content': 'Hello, I would like to start the screening.'}]
    conversation, crisis = run_agent_turn(conversation)
    if crisis:
        return
    while True:
        print('-'*50)
        user_input = input('You: ').strip()
        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit', 'q'):
            print('\nScreening ended. Take care.\n')
            break
        if check_free_text(user_input):
            escalate()
            break
        conversation.append({'role': 'user', 'content': user_input})
        conversation, crisis = run_agent_turn(conversation)
        if crisis:
            break

if __name__ == '__main__':
    main()
