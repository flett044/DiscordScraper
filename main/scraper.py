# Import statements
import requests
import json
import os

# Gets the location of the output txt file from scrapemessages()
def get_file_location():
    file_location = str(os.getcwd() + "\messages.txt")
    return file_location

# Write fetched messages to file
def write_to_file(filename, content):
    content_with_newline = content.replace(',', ',\n')
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(content_with_newline)
    file.close()

# Scrape tge discord messages
def get_messages(channelid, limit, token):
    headers = {
        'Authorization': token,
        'User-Agent': 'DiscordBot'
    }
    messages = []
    last_message_id = None

    while len(messages) < limit:
        # Construct the API URL with the appropriate limit and pagination parameters
        url = f'https://discord.com/api/v9/channels/{channelid}/messages?limit=100'
        if last_message_id:
            url += f'&before={last_message_id}'

        # Send the request
        message_request = requests.get(url, headers=headers)
        gotten_messages = json.loads(message_request.text)

        if not gotten_messages:
            break  # No more messages to retrieve, exit the loop

        # Extract the content from the messages
        messages += [c['content'] for c in gotten_messages]

        # Update the last message ID for the next iteration
        last_message_id = gotten_messages[-1]['id']

    message_string = '\n'.join(messages)
    write_to_file("messages.txt", message_string)


