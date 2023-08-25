import json
import openai

# Load dummy data from JSON file
with open('dummy_data.json', 'r') as f:
    dummy_data = json.load(f)

# Set your OpenAI API key
openai.api_key = MY_KEY

# Define a function to process user prompts
def process_prompt(prompt):
    # Extract the shortened link from the prompt
    #shortened_link = prompt.split(':')[0].strip()

    parts = prompt.split(':', 1)

    # Extract the link and query
    if len(parts) == 2:
        shortened_link = parts[0].strip()
        query = parts[1].strip()
    else:
        # Handle invalid prompt format
        return "Invalid prompt format. Please use 'link : query' format."

    # Get the click count from dummy data
    if shortened_link in dummy_data:
        click_count = dummy_data[shortened_link]["clicks"]
        country_dist = dummy_data[shortened_link]["country_distribution"]
        browser_dist = dummy_data[shortened_link]["browser_distribution"]
        long_link = dummy_data[shortened_link]["long_link"]
        response_prompt = f"shortened link is {shortened_link} , country dist is {country_dist} , browser dist is {browser_dist} , long link is {long_link} , click count is {click_count}: please answer the question {query} from given data"
        return response_prompt
    else:
        return "Link not found in dummy data."

# User interaction loop
while True:
    user_input = input("Enter a prompt: ")
    if user_input.lower() == 'exit':
        break

    chatgpt_prompt = process_prompt(user_input)

    # Call the ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides analytics."},
            {"role": "user", "content": chatgpt_prompt}
        ]
    )

    print("ChatGPT response:", response.choices[0].message["content"])
