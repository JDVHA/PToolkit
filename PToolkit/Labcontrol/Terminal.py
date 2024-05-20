import tkinter as tk

class TkTerminal(tk.LabelFrame):
    def __init__(self, root, text):
        super().__init__(root, text=text)
        self.msgkey = ""
        self.Build()

    def Build(self):
        scrollbar = tk.Scrollbar(self)
        self.terminal = tk.Text(self, wrap="word", yscrollcommand=scrollbar.set)
        self.terminal.tag_config("ERROR", foreground="red")
        scrollbar.config(command=self.terminal.yview)
        
        self.terminal.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.terminal.config(state=tk.DISABLED)

    def Setlink(self, key):
        self.msgkey = key

    def Terminal_msg(self, msg, error=False):
        self.terminal.config(state=tk.NORMAL)
        if error:
            self.terminal.insert(tk.END, f"ERROR: {msg}\n", "ERROR")
        else:
            self.terminal.insert(tk.END, f"{msg}\n")
        self.terminal.config(state=tk.DISABLED)