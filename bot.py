from app import chat_with_paolo_freire

while True:
    user_input = input("User: ")
    if user_input.lower() in ("quit", "exit"):
        exit(0)
    
    response = chat_with_paolo_freire("bot", user_input)
    print(f"Paolo: {response}")




