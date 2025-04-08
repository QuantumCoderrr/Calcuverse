# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 19:30:17 2025
Updated by Jarvis 😎
"""

import tkinter as tk
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🧮 Scientific Calculator")
        self.geometry("420x600")
        self.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()
        self.history = []
        self.mode = tk.StringVar(value="Standard")
        self.degree_mode = tk.BooleanVar(value=True)
        self.dark_mode = tk.BooleanVar(value=True)

        self.configure(bg="#1e1e1e")  # Initial dark mode

        self.create_widgets()
        self.bind_keys()
        self.update_mode()

    def create_widgets(self):
        # Mode and theme toggle
        top_frame = tk.Frame(self, bg=self.bg_color())
        top_frame.pack(pady=10)

        tk.Radiobutton(top_frame, text="Standard", variable=self.mode, value="Standard", command=self.update_mode,
                       bg=self.bg_color(), fg=self.fg_color(), selectcolor=self.bg_color()).grid(row=0, column=0)
        tk.Radiobutton(top_frame, text="Scientific", variable=self.mode, value="Scientific", command=self.update_mode,
                       bg=self.bg_color(), fg=self.fg_color(), selectcolor=self.bg_color()).grid(row=0, column=1)
        tk.Checkbutton(top_frame, text="Dark Mode", variable=self.dark_mode, command=self.toggle_theme,
                       bg=self.bg_color(), fg=self.fg_color(), selectcolor=self.bg_color()).grid(row=0, column=2)

        # Display
        display_frame = tk.Frame(self, bg=self.bg_color())
        display_frame.pack()

        self.entry = tk.Entry(display_frame, textvariable=self.input_text, font=("Consolas", 22),
                              bd=10, relief="ridge", justify="right", bg=self.entry_bg(), fg=self.fg_color())
        self.entry.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=10)
        self.entry.bind("<Return>", self.calculate)
        self.entry.bind("<BackSpace>", self.backspace)

        # History display
        self.history_box = tk.Listbox(self, height=4, font=("Courier", 12), bg=self.bg_color(), fg="#8ef6e4")
        self.history_box.pack(pady=5, fill="x")

        self.create_buttons()

    def create_buttons(self):
        button_frame = tk.Frame(self, bg=self.bg_color())
        button_frame.pack()

        standard_buttons = [
            ("7", "8", "9", "/", "C"),
            ("4", "5", "6", "*", "←"),
            ("1", "2", "3", "-", "("),
            ("0", ".", "=", "+", ")"),
        ]

        scientific_buttons = [
            ("sin", "cos", "tan", "log", "√"),
            ("π", "e", "x²", "exp", "deg"),
        ]

        self.buttons = {}

        # Standard Buttons
        for r, row in enumerate(standard_buttons):
            for c, char in enumerate(row):
                btn = tk.Button(button_frame, text=char, font=("Arial", 14), width=5, height=2,
                                bg=self.button_bg(), fg=self.fg_color(), activebackground="#444",
                                command=lambda ch=char: self.on_button_click(ch))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[char] = btn

        # Scientific Buttons
        self.sci_frame = tk.Frame(button_frame, bg=self.bg_color())
        for r, row in enumerate(scientific_buttons):
            for c, char in enumerate(row):
                btn = tk.Button(self.sci_frame, text=char, font=("Arial", 14), width=5, height=2,
                                bg=self.button_bg(), fg=self.fg_color(), activebackground="#444",
                                command=lambda ch=char: self.on_button_click(ch))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[char] = btn

    def update_mode(self):
        if self.mode.get() == "Scientific":
            self.sci_frame.grid(row=5, column=0, columnspan=5)
        else:
            self.sci_frame.grid_forget()

    def toggle_theme(self):
        bg = self.bg_color()
        fg = self.fg_color()
        self.configure(bg=bg)
        for widget in self.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass
        self.create_widgets()

    def on_button_click(self, char):
        if char == "=":
            self.calculate()
        elif char == "C":
            self.expression = ""
        elif char == "←":
            self.expression = self.expression[:-1]
        elif char == "π":
            self.expression += str(math.pi)
        elif char == "e":
            self.expression += str(math.e)
        elif char == "x²":
            self.expression += "**2"
        elif char == "√":
            self.expression += "math.sqrt("
        elif char == "log":
            self.expression += "math.log10("
        elif char == "sin":
            self.expression += "math.sin(math.radians(" if self.degree_mode.get() else "math.sin("
        elif char == "cos":
            self.expression += "math.cos(math.radians(" if self.degree_mode.get() else "math.cos("
        elif char == "tan":
            self.expression += "math.tan(math.radians(" if self.degree_mode.get() else "math.tan("
        elif char == "exp":
            self.expression += "math.exp("
        elif char == "deg":
            self.degree_mode.set(not self.degree_mode.get())
        else:
            self.expression += char

        self.input_text.set(self.expression)

    def calculate(self, event=None):
        try:
            result = eval(self.expression, {"math": math})
            result = round(result, 6)
            self.history.append(f"{self.expression} = {result}")
            self.update_history()
            self.input_text.set(result)
            self.expression = str(result)
        except ZeroDivisionError:
            self.input_text.set("Zero Division Error")
            self.expression = ""
        except SyntaxError:
            self.input_text.set("Syntax Error")
            self.expression = ""
        except Exception as e:
            self.input_text.set("Unexpected Error")
            self.expression = ""

    def update_history(self):
        self.history_box.delete(0, tk.END)
        for item in reversed(self.history[-4:]):
            self.history_box.insert(tk.END, item)

    def backspace(self, event=None):
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)

    def bind_keys(self):
        self.bind("<Key>", self.handle_keypress)

    def handle_keypress(self, event):
        key = event.char
        if key in "0123456789+-*/().":
            self.on_button_click(key)
        elif key == "\r":
            self.calculate()
        elif key == "\b":
            self.backspace()

    def bg_color(self):
        return "#1e1e1e" if self.dark_mode.get() else "#f5f5f5"

    def fg_color(self):
        return "#ffffff" if self.dark_mode.get() else "#000000"

    def entry_bg(self):
        return "#3a3a3a" if self.dark_mode.get() else "#ffffff"

    def button_bg(self):
        return "#333" if self.dark_mode.get() else "#dcdcdc"

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
