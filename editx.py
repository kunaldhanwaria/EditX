import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import mimetypes

class TextEditor:
    file_name = "Untitled.txt"   # Default file name
    file_content = ""          # Content in a new file
    file_saved_status = False         # File is saved or not

    def __init__(self, master):
        self.master = master
        # Menu Bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Sub Menu (File Menu)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)

        file_menu_command_names = ["New", "Open...", "Save", "Save As...;", "Exit"]
        file_menu_commands = [self.new_file, self.open_file, self.save_file, self.save_as, self.master.quit]

        self.add_menu_command(self.file_menu, "File", file_menu_command_names, file_menu_commands)

        # Sub Menu (Edit Menu)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        space = " " * 18
        edit_menu_command_names = [ f"Undo{space}Ctrl+Z", f"Redo {space}Ctrl+Y;", f"Cut  {space} Ctrl+X",
            f"Copy{space}Ctrl+C", f"Paste{space}Ctrl+V;", f"Select All{space[0:-7]}Ctrl+A", "Clear All"]
        edit_menu_commands = [self.undo, self.redo, self.cut_text, self.copy_text, self.paste_text,
            self.select_all_text, self.clear_all_text]

        self.add_menu_command(self.edit_menu, "Edit", edit_menu_command_names, edit_menu_commands)

        # Sub Menu (Help Menu)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.add_menu_command(self.help_menu, "Help", ["About"], [self.about_msg])

        # Frame 
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill="both", expand=True)

        # Define Scroll Bars + Text Area
        self.v_scroll_bar = tk.Scrollbar(self.main_frame)
        self.h_scroll_bar = tk.Scrollbar(self.main_frame, orient="horizontal")

        self.text_area = tk.Text(self.main_frame, font=("ansifixed", 14), height=10, width=50,
            yscrollcommand=self.v_scroll_bar.set, xscrollcommand=self.h_scroll_bar.set)
        
        # Config and Pack Text Area + Scroll Bars
        self.v_scroll_bar.config(command=self.text_area.yview)
        self.v_scroll_bar.pack(side=tk.RIGHT, fill="y")

        self.text_area.config(selectbackground="Grey", selectforeground="White", undo=True, wrap="none")
        self.text_area.pack(padx=5, pady=5, fill="both", expand=True)

        self.h_scroll_bar.config(command=self.text_area.xview)
        self.h_scroll_bar.pack(side=tk.BOTTOM, fill="x")

        # Status Bar
        self.status_bar = tk.Label(self.master, text=self.file_name, bg="#bfc9c9", fg="Black")
        self.status_bar.pack(fill="x")

    # Function to add Sub Menu
    def add_menu_command(self, sub_menu, label, command_names, command_functions):
        self.menu_bar.add_cascade(label=label, menu=sub_menu)
        for name, function in zip(command_names, command_functions):
            if name.find(";") != -1:
                sub_menu.add_command(label=name[:-1], command=function)
                sub_menu.add_separator()
            else:
                sub_menu.add_command(label=name, command=function)

    # Function to detect changes in a file and save those changes
    def detect_and_save(self):
        if self.text_area.get(1.0, tk.END).strip() != self.file_content.strip():
            response = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save these changes?")
            if response:
                self.save_file()
            elif response == None:
                self.file_saved_status = False
            else:
                self.file_saved_status = True
        else:
            self.file_saved_status = True
        return self.file_saved_status 

    # Saved Prompt
    def saved_successfully_window(self):
        file = self.file_name.split("/")[-1]
        messagebox.showinfo("Saved", f"{file} has successfully saved")

    # Define Functions for Menu Bar Commands
    # 1. File Sub Menu Commands
    def new_file(self):
        if self.detect_and_save():
            self.text_area.delete(1.0, tk.END)
            self.file_content = self.text_area.get(1.0, tk.END)
            self.file_name = "Untitled.txt"
            self.status_bar.configure(text=self.file_name)
        
    def open_file(self):
        try:
            if self.detect_and_save():
                self.file_name = askopenfilename(initialdir=".", title="Select a File",
                                                 filetypes=(("Text Documents", "*.txt"),
                                                 ("All Files", "*.*")))
                # Check the type of selected file (text or binary)
                file_type = mimetypes.guess_type(self.file_name)
                if not file_type[0].find("text"):
                    with open(self.file_name, "r") as text_file:
                        self.text_area.delete(1.0, tk.END)
                        self.file_content = text_file.read()
                        self.text_area.insert(1.0, self.file_content)
                        self.status_bar.configure(text=self.file_name.split("/")[-1])
                else:
                    messagebox.showerror("Unexpexted File Type", 
                    "EditX can only open text files.\n\nChoose a different app to open this file.")
        except AttributeError:
            self.file_name = "Untitled.txt"

    def save_file(self):
        if self.file_name == "Untitled.txt":
            self.save_as()
            if self.file_saved_status == False:
                return
        else:    
            with open(self.file_name, "w") as text_file:
                text_file.write(self.text_area.get(1.0, tk.END))
                self.file_saved_status = True
                self.saved_successfully_window()
        self.file_content = self.text_area.get(1.0, tk.END)

    def save_as(self):
        try:
            self.file_name = asksaveasfilename(defaultextension=".*", initialfile="*.txt", initialdir=".",
                                                title="Save File", filetypes=(("Text Documents", "*.txt"),
                                                ("All Files", "*.*")))
            with open(self.file_name, "w") as text_file:
                text_file.write(self.text_area.get(1.0, tk.END))
            self.file_content = self.text_area.get(1.0, tk.END)
            self.status_bar.configure(text=self.file_name.split("/")[-1])
            self.file_saved_status = True
            self.saved_successfully_window()
        except FileNotFoundError:
            self.file_name = "Untitled.txt"
            self.file_saved_status = False

    # 2. Edit Sub Menu Commands
    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def undo(self):
        self.text_area.event_generate("<<Undo>>")

    def redo(self):
        self.text_area.event_generate("<<Redo>>")

    def select_all_text(self):
        self.text_area.event_generate("<<SelectAll>>")

    def clear_all_text(self):
        self.text_area.delete(1.0, tk.END)

    # 3. Help Sub Menu Command
    def about_msg(self):
        messagebox.showinfo("EditX", "Version : 1.0\n\nDeveloped by Kunal Dhanwaria")

if __name__ == "__main__":

    root = tk.Tk()
    root.title("EditX")
    root.minsize(400, 300)

    editx = TextEditor(root)

    root.mainloop()