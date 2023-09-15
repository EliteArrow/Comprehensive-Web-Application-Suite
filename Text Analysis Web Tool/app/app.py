import openai
openai.api_key = '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'
messages = [ {"role": "system", "content":
			"You are a intelligent assistant."} ]
while True:
	message = input("""User : """)
	if message:
		messages.append(
			{"role": "user", "content": message},
		)
		chat = openai.ChatCompletion.create(
			model="gpt-3.5-turbo", messages=messages
		)
	reply = chat.choices[0].message.content
	print(f"System: {reply}")
	messages.append({"role": "assistant", "content": reply})
