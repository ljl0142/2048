import tkinter as tk
import tkinter.messagebox

def fail_popup(score):
    tk.messagebox.showinfo(title='Game Over',message='You fail.\n Your score is '+str(score))


def success_popup(score):
    tk.messagebox.showinfo(title='2048',message='Congratulations! You have got 2048 in this game.\n Your score is '+str(score))
