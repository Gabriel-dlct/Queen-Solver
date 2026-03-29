import tkinter as tk
import subprocess

def launch():
    subprocess.Popen(["python", "src/main.py"])

root = tk.Tk()
root.title("Queens Solver")

btn = tk.Button(root, text="Lancer le solver", command=launch, width=20, height=2)
btn.pack(padx=20, pady=20)

root.mainloop()