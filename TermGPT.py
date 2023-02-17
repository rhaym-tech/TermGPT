#!/usr/bin/env python3

import os
import sys
import time
import argparse
from revChatGPT.V1 import Chatbot
from dotenv import load_dotenv

load_dotenv()

def ask_prompt():
    prompt = input("Please enter a prompt: ")
    print("Hmm, let me think", end="")
    while True:
        for i in range(5):
            time.sleep(1)
            print(".", end="", flush=True)
        print("\033[K", end="")
        response = ""
        for data in chatbot.ask(prompt):
            response = data["message"]
        if response != "":
            print("\033[32m", end="")
            print("\r" + response + "\033[0m")
            break

    return input("Do you want to ask another prompt? (y/n)").lower() == 'y'

def setup_login():
    email = input("Please enter your OpenAI email address: ")
    password = input("Please enter your OpenAI password: ")

    with open(".env", "w") as f:
        f.write(f"#OpenAI account email:\n")
        f.write(f'OPENAI_EMAIL = "{email}"\n\n')
        f.write(f"#OpenAI account password:\n")
        f.write(f'OPENAI_PASSWORD = "{password}"\n\n')
        f.write(f"# TermGPT version\n")
        f.write(f'VERSION = "TermGPT Beta v1.0.0"\n')

    print("Login information saved successfuly.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TermGPT')
    parser.add_argument('-a', '--ask', action='store_true', help='Ask for a prompt and get a response')
    parser.add_argument('-l', '--login', action='store_true', help='Set up OpenAI login credentials')
    parser.add_argument('-v', '--version', action='version', version= os.getenv("VERSION"))
    args = parser.parse_args()

    if args.login:
        setup_login()
        sys.exit()

    email = os.getenv("OPENAI_EMAIL")
    password = os.getenv("OPENAI_PASSWORD")
    chatbot = Chatbot(config={
      "email": email,
      "password": password
    })

    if args.ask:
        while True:
            if not ask_prompt():
                break
    else:
        parser.print_help()
