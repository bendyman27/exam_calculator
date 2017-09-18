#!/usr/bin/env python3

"""
A simple GUI to calculate weighted exam results.
"""

from tkinter import *
from tkinter import messagebox

LARGE_FONT = ("verdana", 12)
MEDIUM_FONT = ("verdana", 10)

class Exam_calculator(Tk):
     
    def __init__(self):
        Tk.__init__(self)
        self.title("Exam Calculator")
        
        container = Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.pack(side=TOP, fill="both", expand=True)
        
        frame = StartPage(container)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)       
        
class StartPage(Frame):
        
    def __init__(self, parent):
        self.container = parent
        Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        for i in range(2,11):
            self.grid_rowconfigure(i, weight=1)
        

        main_label = Label(self, text="Please enter exam details...", font=LARGE_FONT)
        main_label.grid(row=0, column=0, columnspan=3, pady=10)

        Label(self, text="Section:", font=MEDIUM_FONT).grid(
            row=1, column=0, pady=10)
        Label(self, text="Marks:", font=MEDIUM_FONT).grid(
            row=1, column=1, pady=10)
        Label(self, text="Weight:", font=MEDIUM_FONT).grid(
            row=1, column=2, pady=10)
        
        self.sections = []
        self.marks = []
        self.weights = []
        for i in range(8):        
            self.sections.append(Entry(self, font=MEDIUM_FONT))
            self.sections[i].grid(row=i+2, column=0, padx=10, pady=5, sticky=EW)
            self.marks.append(Entry(self, font=MEDIUM_FONT, width=5, justify=CENTER))
            self.marks[i].grid(row=i+2, column=1, padx=10, pady=5)
            self.marks[i].insert(0, "0")
            self.weights.append(Entry(self, font=MEDIUM_FONT, width=5, justify=CENTER))
            self.weights[i].grid(row=i+2, column=2, padx=10, pady=5)
            self.weights[i].insert(0, "0")
        
        self.sections[0].focus_set()
        
        go_button = Button(self, text="Go...", font=LARGE_FONT, command=self.go)
        go_button.grid(row=10, column=2, padx=10, pady=10)
        go_button.bind('<Return>', self.go)
     
    def go(self, *args):
        section = []
        mark = []
        weight = []
        try:
            for i in range(8):
                section.append(self.sections[i].get())
                mark.append(int(self.marks[i].get()))
                weight.append(int(self.weights[i].get()))
        except:
            messagebox.showwarning("Error",
                "A problem reading input.\n" +
                "Please use whole numbers\nonly for Marks and Weight")
            return
        
        #check data and proceed to new page if OK
        proceed = True
        
        # Trim lists
        for i in range(7, -1,-1):
            if section[i] == '':
                section = section[:i]
            if mark[i] == 0:
                mark = mark[:i]
            if weight[i] == 0:
                weight = weight[:i]
        
        # Check lengths
        if len(section) != len(mark) or len(mark) != len(weight):
            messagebox.showwarning("Error", "Please check your input.")
            proceed = False
        
        # Check weights sum to 100
        if proceed:
            total = 0
            for w in weight:
                total += w
            if total != 100:
                proceed = messagebox.askyesno("Confirm",
                        "Weights don't total 100%, Proceed anyway?")
        
        if proceed:
            frame = CalcPage(self.container, section, mark, weight)
            frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
            self.grid_forget()
            self.destroy()
        
class CalcPage(Frame):
    
    def __init__(self, parent, section, mark, weight):
        Frame.__init__(self, parent)
        self.container = parent
        self.number_of_sections = len(section)
        self.mark = mark
        self.weight = weight
        
        # Configure grid
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        for i in range(self.number_of_sections):
            self.grid_rowconfigure(i+1, weight=1)        
        
        # Main label
        Label(self, text="Calculate results...", font=LARGE_FONT).grid(
            row=0, column=0, padx=10, pady=10)
        
        # Back button
        backB = Button(self, text="New Exam", font=MEDIUM_FONT,
                       command=self.back, takefocus=0)
        backB.grid(row=0, column=1, pady=10, padx=10)
        
        # Label and input box loop
        self.results = []
        for i in range(self.number_of_sections):
            Label(self, text=section[i] + " (" + str(self.mark[i]) + ")",
                  font=MEDIUM_FONT).grid(row=i+1, column=0, pady=10, sticky=E)
            self.results.append(Entry(self, font=MEDIUM_FONT, width=5, justify=CENTER))
            self.results[i].grid(row=i+1, column=1, pady=10)
            
        if self.number_of_sections > 0:
            self.results[0].focus_set()
        
        # Result box (read only)
        self.final_mark = StringVar()
        result_box = Entry(self, font=LARGE_FONT, textvariable=self.final_mark,
                           state="readonly", width=5, justify=CENTER, takefocus=0)
        result_box.grid(row=9, column=1, pady=10)
        
        # Calc button
        calcB = Button(self, text="Calculate", font=MEDIUM_FONT, command=self.calc)
        calcB.grid(row=9, column=0, sticky=E)
        calcB.bind('<Return>', self.calc)
                
    def calc(self, *args):
        result = []
        try:
            for i in range(self.number_of_sections):
                result.append(float(self.results[i].get()))
        except:
            messagebox.showwarning("Error", "Numerical input only please.")
            return
        # Do maths
        x = 0
        for i in range(self.number_of_sections):
            x += (result[i] / self.mark[i]) * self.weight[i]
        x = int(x)
        x = float(x) / 10        
        # Update result
        self.final_mark.set(str(x))
        
    def back(self):
        frame = StartPage(self.container)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        self.grid_forget()
        self.destroy()   

def main():
     app = Exam_calculator()
     app.mainloop()
     
if __name__ == '__main__':
     main()
