from helper_classes import Website
from helper_classes import Model
from helper_classes import Prompt
import argparse


def main():

    parser = argparse.ArgumentParser(description='Summarize website content using OpenAI')
    parser.add_argument('--model', type=str, required=True, help='LLM to call.')
    parser.add_argument('--url', type=str, required=True, help='Website to summarize.')

    args = parser.parse_args()

    website = Website(url=args.url)

    prompt = Prompt(website=website)

    summary = Model().summarize(model=args.model, prompt=prompt.create_prompts())

    print(summary)

if __name__ == '__main__':
    main()