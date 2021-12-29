import datetime
from tkinter import *
from tkinter import filedialog
from os import listdir, getcwd, remove
from datetime import date, datetime

# Configuration Variables
HEIGHT, WIDTH = 700, 600
FONT = "HP Simplified Hans Light"
DATE = date.today().strftime("%d-%m-%Y")

PAGE_DIRECTORY = f"{getcwd()}\\pages\\".replace("\\", "/")

current_page = ""
current_name = ""
# load all text files into memory then next/back will just change the index
pages = [PAGE_DIRECTORY + page for page in listdir("pages")]


# Gets the file name out of a path, e.g. C:/.../foo.txt will return foo
def file_name(path):
    return path[:path.find(".")].replace(PAGE_DIRECTORY, "")


# Clear pre-existing items
def new_file(text, status):
    global current_page
    global current_name

    current_page, current_name = "", ""
    text.delete("1.0", END)
    status.config(text="New File")


def open_file(text, status, text_file=None):
    global current_page
    global current_name
    # Check if text_file exists/already given, otherwise ask
    text_file = text_file or filedialog.askopenfilename(
        initialdir=PAGE_DIRECTORY,
        title="Open File",
        filetypes=[("Text Files", ".txt")]
    )
    # Only if text_file exists, e.g. in case of user pressing Cancel on explorer
    if text_file:
        text.delete("1.0", END)

        current_page = text_file
        name = file_name(text_file)
        try:
            current_name = datetime.strptime(name, "%d-%m-%Y").strftime("%A, %B %d, %Y")
        except ValueError:
            current_name = name
        status.config(text=current_name)

        with open(text_file, "r") as file_contents:
            content = file_contents.read()
            text.insert(END, content)


def save_file(text, status, text_file=None):
    global current_page
    global current_name
    global pages
    # Check if text_file exists, otherwise ask
    text_file = text_file or filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile=file_name(current_page) or DATE,
        initialdir=PAGE_DIRECTORY,
        title="Save File",
        filetypes=[("Text Files", ".txt")]
    )
    # Only if text_file exists, e.g. in case of user pressing Cancel on explorer
    if text_file:
        current_page = text_file
        name = file_name(text_file)
        try:
            current_name = datetime.strptime(name, "%d-%m-%Y").strftime("%A, %B %d, %Y")
        except ValueError:
            current_name = name
        status.config(text=f"{current_name} (Saved)")

        with open(text_file, "w") as write_file:
            write_file.write(text.get("1.0", END)[:-1])

        # If adding new file, reload memory to preserve order
        if text_file not in pages:
            pages = [PAGE_DIRECTORY + page for page in listdir("pages")]


def delete_file(text, status):
    # Removes page from memory
    pages.remove(current_page)
    # Removes the actual file
    remove(current_page)
    # Clears the textbox
    new_file(text, status)
    status.config(text=f"Page Deleted")


# These loop through pages, and can loop back once reaching the end due to modulus
def next_page(text, status):
    if current_page:
        open_file(text, status, pages[(pages.index(current_page) + 1) % len(pages)])
    else:
        open_file(text, status, pages[-1])


def back_page(text, status):
    if current_page:
        open_file(text, status, pages[(pages.index(current_page) - 1) % len(pages)])
    else:
        open_file(text, status, pages[0])


def main():
    root = Tk()
    root.title("Journal")
    root.geometry(f"{WIDTH}x{HEIGHT}")

    toolbar = Frame(root, relief=RAISED, bg="#DCDCDC")
    toolbar.pack(side=TOP, fill=X)

    my_frame = Frame(root)
    my_frame.pack()

    status_bar = Label(my_frame, text="New File", font=("HP Simplified Hans", 16))
    status_bar.pack(fill=X, ipady=5)

    text_scroll = Scrollbar(my_frame)
    text_scroll.pack(side=RIGHT, fill=Y)

    text_box = Text(my_frame, height=50, font=(FONT, 16), wrap=WORD, undo=True, yscrollcommand=text_scroll.set, pady=10,
                    padx=10)
    text_box.pack()

    text_scroll.config(command=text_box.yview)

    file_button = Button(toolbar, relief=RAISED, compound=LEFT, text="New",
                         command=lambda: new_file(text_box, status_bar))
    file_button.pack(side=LEFT, padx=10, pady=10)
    open_button = Button(toolbar, relief=RAISED, compound=LEFT, text="Open",
                         command=lambda: open_file(text_box, status_bar))
    open_button.pack(side=LEFT, padx=10, pady=10)
    save_button = Button(toolbar, relief=RAISED, compound=LEFT, text="Save",
                         command=lambda: save_file(text_box, status_bar, current_page))
    save_button.pack(side=LEFT, padx=10, pady=10)
    saveas_button = Button(toolbar, relief=RAISED, compound=LEFT, text="Save As",
                           command=lambda: save_file(text_box, status_bar))
    saveas_button.pack(side=LEFT, padx=10, pady=10)
    delete_button = Button(toolbar, relief=RAISED, compound=LEFT, text="Delete")
    delete_button.pack(side=LEFT, padx=10, pady=10)
    # Add confirmation to the delete button
    delete_button.bind("<Button-1>", lambda x: status_bar.config(text="Double click to delete this page"))
    delete_button.bind("<Double-Button-1>", lambda x: delete_file(text_box, status_bar))

    next_button = Button(toolbar, relief=RAISED, compound=LEFT, text="-->",
                         command=lambda: next_page(text_box, status_bar))
    next_button.pack(side=RIGHT, padx=10, pady=10)
    back_button = Button(toolbar, relief=RAISED, compound=LEFT, text="<--",
                         command=lambda: back_page(text_box, status_bar))
    back_button.pack(side=RIGHT, padx=10, pady=10)

    text_box.bind("<KeyRelease>", lambda x: status_bar.config(text=current_name or "New File"))
    root.bind("<End>", lambda x: next_page(text_box, status_bar))
    root.bind("<Home>", lambda x: back_page(text_box, status_bar))

    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()
