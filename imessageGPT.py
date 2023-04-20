import openai
from imessage_reader import fetch_data
import os
from time import sleep
from datetime import datetime

sender_number_index = 0
message_index = 1
date_index = 2
message_type_index = 3
my_number_index = 4
who_sent_index = 5
from_me = 1
from_you = 0

new_messages = []
#summary_array = []
now = datetime.now()
last_message_date = int(now.strftime("%Y" + "%m" + "%d" + "%H" + "%M" + "%S"))

openai.api_key = "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"
model_engine = "text-davinci-003"

while True:
  fd = fetch_data.FetchData()
  messages = fd.get_messages()

  for message in messages:
    temp_date = (int((message[date_index])[0:4]) * 10000000000) + (int((message[date_index])[5:7]) * 100000000) + (int((message[date_index])[8:10]) * 1000000)
    temp_date = temp_date + (int((message[date_index])[11:13]) * 10000) + (int((message[date_index])[14:16]) * 100) + int((message[date_index])[17:19])
    if last_message_date < temp_date and from_you == message[who_sent_index]:
      new_messages.append(message)
      last_message_date = temp_date


  for message in new_messages:
    prompt = message[message_index]
    print(message[sender_number_index] + "\n" + message[message_type_index] + "\n" + 'Prompt: ' + prompt)
    
    #summary = [message[message_index]]
    #summary_array.append(summary)

    completion = openai.Completion.create(
      engine = model_engine,
      prompt = "Give a response to: " + prompt,
      max_tokens = 256,
      temperature = 0.5,
      top_p = 1,
      frequency_penalty = 0,
      presence_penalty = 0
    )
    response = completion.choices[0].text
    response = "\"" + response[2:] + "\""
    print("Response: " + response + "\n")
    
    if message[message_type_index] == "iMessage":
      os.system(
        "osascript sendiMessage.applescript {} {}".format(message[sender_number_index], response)
      )
    if message[message_type_index] == "SMS":
      os.system(
        "osascript sendSMS.applescript {} {}".format(message[sender_number_index], response)
      )

    new_messages.remove(message)
    sleep(1)