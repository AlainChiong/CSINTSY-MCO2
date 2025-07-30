import tkinter as tk
from tkinter import font as tkfont
from family_logic import handle_statement, handle_question

def start_app():
    def process_input():
        user_input = entry.get()
        if user_input.strip() == "":
            return
        if user_input.endswith("?"):
            response = handle_question(user_input)
        else:
            response = handle_statement(user_input)
        output_text.insert(tk.END, f"You: {user_input}\n", "user")
        output_text.insert(tk.END, f"Bot: {response}\n\n", "bot")
        entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Family Chatbot")
    root.geometry("600x500")
    root.configure(bg="#f7f7f7")

    user_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
    bot_font = tkfont.Font(family="Helvetica", size=12)
    entry_font = tkfont.Font(family="Helvetica", size=12)

    frame = tk.Frame(root, bg="#f7f7f7")
    frame.pack(pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    output_text = tk.Text(frame, height=20, width=70, yscrollcommand=scrollbar.set, wrap=tk.WORD, bg="white", padx=10, pady=10)
    output_text.pack()

    output_text.tag_configure("user", foreground="#007acc", font=user_font)
    output_text.tag_configure("bot", foreground="#333333", font=bot_font)

    scrollbar.config(command=output_text.yview)

    output_text.insert(tk.END, "Welcome to the Family Chatbot!\n")

    entry = tk.Entry(root, width=60, font=entry_font)
    entry.pack(pady=5)

    submit_button = tk.Button(root, text="Send", command=process_input, bg="#007acc", fg="white", font=("Helvetica", 12), padx=10, pady=5)
    submit_button.pack()

    root.mainloop()
