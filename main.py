import tkinter as tk
from tkinter import scrolledtext
import openai
import webbrowser
from dotenv import load_dotenv
import os
load_dotenv()  # This loads .env automatically
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_safety_resource(message):
    distress_keywords = ["suicide", "self-harm", "hopeless", "can't go on", "want to die", "don't want to live"]
    if any(word in message.lower() for word in distress_keywords):
        webbrowser.open("https://www.eran.org.il/")
        return (
            "I'm really sorry you're feeling this way. I've opened the ERAN support website for you: https://www.eran.org.il/"
            "\nIf you need immediate help, please reach out to a professional or helpline."
        )
    return None

def chat_with_openai(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def on_send(event=None):  # event arg for Enter key
    user_message = entry.get()
    if not user_message.strip():
        return
    if user_message.lower() == "exit":
        root.quit()
    chat_window.config(state="normal")
    chat_window.insert(tk.END, f"You: {user_message}\n")
    safety = get_safety_resource(user_message)
    messages.append({"role": "user", "content": user_message})
    if safety:
        chat_window.insert(tk.END, f"Bot: {safety}\n")
        chat_window.config(state="disabled")
        entry.delete(0, tk.END)
        return
    reply = chat_with_openai(messages)
    messages.append({"role": "assistant", "content": reply})
    chat_window.insert(tk.END, f"Bot: {reply}\n")
    chat_window.config(state="disabled")
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Adi's Mental Health Support Chatbot")
root.attributes('-topmost', True)

chat_window = scrolledtext.ScrolledText(root, state="disabled", width=60, height=20)
chat_window.pack(pady=10)

messages = [{"role": "system", "content": "You are a supportive mental health assistant."}]

entry = tk.Entry(root, width=60)
entry.pack(pady=5)
entry.bind("<Return>", on_send)

send_button = tk.Button(root, text="Send", command=on_send)
send_button.pack()

entry.focus_set()

root.mainloop()
