# Import statements - Written by Fleet
import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
import json
import os


title_font = "terminal 15 underline bold"
normal_font = "terminal 10"

# Main GUI
root = tk.Tk()
root.title("Discord Scraper")
root.geometry("270x300")
root.resizable(0, 0)

# Style options
style = ttk.Style("vapor")

# Title Label
title = ttk.Label(root, text="Discord Scraper", font=title_font)
title.place(x=55, y=5)

# Convert entry to string var
channel_id = ttk.StringVar()
message_limit = ttk.StringVar()
discord_token = ttk.StringVar()

# Token Label and token input box
token_text = ttk.Label(root, text="Token", font=normal_font)
token_text.place(x=9, y=34)
token_input = ttk.Entry(root, textvariable=discord_token, width=40, show='*')
token_input.place(x=9, y=50)

# Channel Label and channel_id input box
channel_text = ttk.Label(root, text="Channel ID", font=normal_font)
channel_text.place(x=9, y=79)
channel_input = ttk.Entry(root, textvariable=channel_id, width=40)
channel_input.place(x=9, y=95)

# Limit aka how many messages to get
limit_text = ttk.Label(root, text="Message Limit", font=normal_font)
limit_text.place(x=9, y=126)
limit_input = ttk.Entry(root, textvariable=message_limit, width=40)
limit_input.place(x=9, y=142)

# Output Box
output_box = ttk.Text(root, height = 1, width = 40)
output_box.place(x=9, y=208)

# Write output in output box
def set_output(Output):
    output_box.delete(1.0, "end")
    output_box.insert(END, Output)

# Reads discord token from token inout
def read_discord_token():
    discord_token = token_input.get()
    return discord_token

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

# Scrapes discord messages
def scrape_messages():
    set_output("Scraping Messages...")
    try:
        get_messages(read_channel_id(), read_message_limit(), read_discord_token())
        set_output("Done")
        set_output(get_file_location())
    # Catch if nothing is entered in token/channelid/limit box
    except TypeError as e:
        set_output("Wrong Token/Channel ID/Message Limit")
    # Catch all other exceptions and print to output
    except Exception as e:
        set_output(e)

# Reads channel id from channel input box
def read_channel_id():
    channel_id = channel_input.get()
    return channel_id

# Reads message limit from limit input box
def read_message_limit():
    message_limit = int(limit_input.get())
    return message_limit

# Exits the program
def main_exit():
    sys.exit()

# Start button
scrape_Messages_Button = ttk.Button(root, text="Scrape Messages", command=scrape_messages)
scrape_Messages_Button.place(x=9, y=240)

# Exit button
exit_Button = ttk.Button(root, text="Exit", command=main_exit)
exit_Button.place(x=220, y=240)

root.mainloop()
