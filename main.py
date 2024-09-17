import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import subprocess
import webbrowser
import shutil


class IDE:
    def __init__(self, master):
        self.name = "Divesh IDE"
        self.ver = "v1.0"
        self.dev_name = "Divesh Adivarekar"
        self.app_name = f"{self.name} - {self.ver}"
        self.master = master
        self.master.title(self.app_name)
        self.master.geometry("1024x768")
        # Set the icon of the window
        master.iconbitmap("favicon.ico")
        self.font_size = 12

        # create a notebook with create new and close tab buttons
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.tabs = []
        self.add_tab()
        self.add_button = ttk.Button(
            self.master, text=" ➕ New Tab ", command=self.add_tab
        )
        self.add_button_close = ttk.Button(
            self.master, text=" ❌Close Tab ", command=self.close_tab
        )
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_button_close.pack(side=tk.LEFT, padx=5, pady=5)

        self.filename = None
        self.dark_mode = False

        # Menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(
            label="Open", accelerator="Ctrl+O", command=self.open_file
        )
        file_menu.add_command(
            label="Save", accelerator="Ctrl+S", command=self.save_file
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", accelerator="Alt+F4", command=self.master.quit
        )
        menubar.add_cascade(label="File", menu=file_menu)

        # Create a "Font" menu with a dropdown of font families
        font_menu = tk.Menu(menubar, tearoff=0)
        self.font_family_var = tk.StringVar()
        font_families = font.families()
        self.font_family_var.set(font_families[0])
        for family in font_families:
            font_menu.add_radiobutton(
                label=family,
                variable=self.font_family_var,
                value=family,
                command=self.update_font,
            )
        menubar.add_cascade(label="Font", menu=font_menu)

        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        run_submenu = tk.Menu(run_menu, tearoff=0)
        run_submenu.add_command(label="Java", command=self.run_java)
        run_submenu.add_command(label="Python", command=self.run_python)
        run_submenu.add_command(label="html", command=self.run_html)
        run_menu.add_cascade(label="Select language", menu=run_submenu)
        menubar.add_cascade(label="Run", menu=run_menu)

        # Dark Mode button
        view_menu = tk.Menu(menubar, tearoff=0)
        view_submenu = tk.Menu(view_menu, tearoff=0)
        view_submenu.add_command(
            label="Increase Font Size",
            accelerator="Ctrl +",
            command=self.increase_font_size,
        )
        view_submenu.add_command(
            label="Decrease Font Size",
            accelerator="Ctrl -",
            command=self.decrease_font_size,
        )
        view_menu.add_cascade(label="Font Size", menu=view_submenu)
        view_menu.add_command(label="Dark Mode", command=self.toggle_dark_mode)
        menubar.add_cascade(label="View", menu=view_menu)

        # help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Shortcuts", command=self.shortcuts)
        help_menu.add_command(label="Visit website", command=self.help)
        help_menu.add_command(label="About", command=self.about)
        help_menu.add_command(label="Version", command=self.version)
        menubar.add_cascade(label="Help", menu=help_menu)

        # key binds
        self.master.bind("<Control-n>", self.new_file)
        self.master.bind("<Control-o>", self.open_file)
        self.master.bind("<Control-s>", self.save_file)
        self.master.bind("<Control-plus>", self.increase_font_size)
        self.master.bind("<Control-equal>", self.increase_font_size)
        self.master.bind("<Control-minus>", self.decrease_font_size)
        self.master.bind("<Control-F5>", self.run_code)
        self.master.bind("<Control-t>", self.add_tab)
        self.master.bind("<Control-w>", self.close_tab)

    def add_tab(self, event=None):
        self.text_box = tk.Text(self.notebook, wrap=tk.WORD)
        scroll_bar = ttk.Scrollbar(
            self.notebook, orient=tk.VERTICAL, command=self.text_box.yview
        )
        self.text_box.configure(yscrollcommand=scroll_bar.set)
        tab = self.notebook.add(self.text_box, text=f"Untitled {len(self.tabs)}")
        self.tabs.append(tab)
        self.notebook.select(tab)
        self.text_box.focus_set()

    def close_tab(self, event=None):
        if len(self.tabs) == 1:
            self.master.destroy()
        else:
            try:
                self.notebook.forget(0)
                self.tabs.remove(0)
            except ValueError:
                pass

    def on_tab_changed(self, event):
        current_tab = event.widget.select()
        index = event.widget.index(current_tab)
        self.text_box = self.notebook.nametowidget(current_tab)
        file_name = self.notebook.tab(index, "text")
        self.master.title(f"{self.app_name} - {file_name}")

    def new_file(self, event=None):
        self.add_tab()
        self.filename = None
        self.text_box.delete("1.0", "end")

    def open_file(self, events=None):
        file_types = [
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("HTML Files", "*.html"),
            ("CSS Files", "*.css"),
            ("JavaScript Files", "*.js"),
            ("Python Files", "*.py"),
            ("Java Files", "*.java"),
        ]

        self.filename = filedialog.askopenfilename(
            defaultextension=".", filetypes=file_types
        )

        program_name = self.filename.split("/")[-1]
        if self.filename:
            self.text_box.delete("1.0", "end")
            with open(self.filename, "r", encoding="utf-8") as file:
                text = file.read()
                self.text_box = self.notebook.nametowidget(self.notebook.select())
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(1.0, text)
            self.notebook.tab(self.notebook.select(), text=program_name)
            self.master.title(f"{self.app_name} - {program_name}")

    def save_file(self, event=None):
        if not self.filename:
            file_types = [
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JavaScript Files", "*.js"),
                ("Python Files", "*.py"),
                ("Java Files", "*.java"),
            ]

            self.filename = filedialog.asksaveasfilename(
                defaultextension=".", filetypes=file_types
            )

        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(self.text_box.get("1.0", "end-1c"))

        program_name = self.filename.split("/")[-1]
        self.notebook.tab(self.notebook.select(), text=program_name)

    def run_code(self, event=None):
        if not self.filename:
            messagebox.showwarning("Warning", "No file is open")
            return

        # Get file extension
        _, file_extension = os.path.splitext(self.filename)

        if file_extension == ".py":
            self.run_python()
        elif file_extension == ".java":
            self.run_java()
        elif file_extension == ".html":
            self.run_html()
        else:
            messagebox.showerror("Error", "Unsupported file type")

    def run_html(self):
        webbrowser.open(self.filename)

    def run_java(self):
        # Check if Java compiler is installed
        if not shutil.which("javac"):
            messagebox.showerror("Error", "Java compiler not found")
            return

        # Check if Java interpreter is installed
        if not shutil.which("java"):
            messagebox.showerror("Error", "Java interpreter not found")
            return

        # Compile the Java file
        subprocess.run(["javac", self.filename])
        program_name = self.filename.split(".")[0]
        program_name = program_name.split("/")[-1]
        # Run the Java program and capture the output
        process = subprocess.Popen(
            ["java", program_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, errors = process.communicate()
        self.output_screen(output, errors)

    def run_python(self):
        # Run the script and capture the output
        process = subprocess.Popen(
            ["python", f"{self.filename}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, errors = process.communicate()
        self.output_screen(output, errors)

    def output_screen(self, output, errors):
        # Create a new window to display the output
        output_window = tk.Toplevel()
        program_name = self.filename.split("/")[-1]
        output_window.title(f"{self.app_name} - Output {program_name}")
        # Set the icon of the window
        output_window.iconbitmap("favicon.ico")

        # Create a Text widget to display the output
        output_box = tk.Text(output_window)
        output_box.pack()

        # Display the output in the Text widget
        output_box.insert(tk.END, output.decode("utf-8"))
        output_box.insert(tk.END, errors.decode("utf-8"))

    def shortcuts(self):
        message = (
            "Here are some handy shortcuts:\n\n"
            "🔹 Ctrl+N: New File\n"
            "🔹 Ctrl+O: Open File\n"
            "🔹 Ctrl+S: Save File\n"
            "🔹 Ctrl+T: New Tab\n"
            "🔹 Ctrl+W: CLose Tab\n"
            "🔹 Ctrl+Plus or Ctrl+Equal: Increase Font Size\n"
            "🔹 Ctrl+Minus: Decrease Font Size\n"
            "🔹 Ctrl+F5: Run Code"
        )
        messagebox.showinfo("Keyboard Shortcuts", message)

    def help(self):
        url = "https://github.com/diveshadivarekar/Divesh-IDE"
        webbrowser.open(url)

    def version(self):
        messagebox.showinfo("Version", f"{self.ver}")

    def about(self):
        messagebox.showinfo(
            "About",
            f"Name - {self.name}\nVersion - {self.ver}\n\nDeveloped by: {self.dev_name}",
        )

    def toggle_dark_mode(self):
        if self.dark_mode:
            self.master.config(bg="white", cursor="plus black")
            self.text_box.config(bg="white", fg="black")
            self.dark_mode = False
        else:
            self.master.config(bg="black", cursor="plus white")
            self.text_box.config(bg="gray", fg="white")
            self.dark_mode = True

    def update_font(self):
        # Update the text widget's font family
        font_family = self.font_family_var.get()
        self.text_box.configure(font=(font_family, self.font_size))

    def increase_font_size(self, event=None):
        self.font_size += 2
        self.update_font()

    def decrease_font_size(self, event=None):
        self.font_size -= 2
        self.update_font()


if __name__ == "__main__":
    root = tk.Tk()
    app = IDE(root)
    root.mainloop()
