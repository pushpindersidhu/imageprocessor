from tkinter import *
from tkmacosx import Button
from PIL import ImageTk
from image_processor import ImageProcessor

root = Tk()
image_processor = ImageProcessor()
root.title("Image Processor")
root.geometry("1000x600")
root.resizable(False, False)
root.config(bg="#020617")


def update_image(modifiedPILImage=None):
    modified_image = None

    if modifiedPILImage is None:
        new_image = image_processor.get_image()

        origional_image = ImageTk.PhotoImage(new_image.resize((300, 300)))
        original_label.config(image=origional_image)
        original_label.image = origional_image

        modified_image = ImageTk.PhotoImage(new_image)
    else:
        modified_image = ImageTk.PhotoImage(modifiedPILImage)

    modified_label.config(image=modified_image)
    modified_label.image = modified_image


left_frame = Frame(root, width=300, height=600, bg="#020617")
left_frame.grid(row=0, column=0, padx=15, pady=5, sticky=NW, columnspan=2)

right_frame = Frame(root, width=700, height=600, bg="#020617")
right_frame.grid(row=0, column=2, padx=15, pady=5)

Label(left_frame, text="Original", bg="#020617", fg="#ffffff", justify=LEFT).grid(
    row=0, column=0, padx=0, pady=5, columnspan=2, sticky=W
)

Button(
    left_frame,
    text="Open Image",
    command=lambda: [image_processor.open(), update_image()],
    height=32,
    fg="#fbbf24",
    bg="#0f172a",
    activebackground=("#0f172a", "#0f172a"),
    borderless=1,
    bd=0,
    highlightthickness=0,
    relief="flat",
    focuscolor="#0f172a",
    highlightbackground="#0f172a",
    highlightcolor="#0f172a",
    activeforeground="#fbbf24",
).grid(row=0, column=2, padx=0, pady=5, columnspan=2, sticky=E)

image = ImageTk.PhotoImage(image_processor.get_image())
original_image = ImageTk.PhotoImage(image_processor.resize(width=300))
original_label = Label(left_frame, image=original_image, bg="#020617", fg="#ffffff")
original_label.grid(row=1, column=0, padx=1, pady=5, columnspan=4, sticky=W)

modified_label = Label(
    right_frame, image=image, width=700, height=600, bg="#020617", fg="#ffffff"
)
modified_label.grid(row=0, column=0, padx=0, pady=1)

tool_bar = Frame(
    left_frame,
    width=300,
    bg="#020617",
)
tool_bar.grid(row=2, column=0, padx=1, pady=5, columnspan=4, sticky=W)

function_buttons = [
    ("Grayscale", lambda: update_image(image_processor.grayscale())),
    ("Negative", lambda: update_image(image_processor.negative())),
    ("Pencil", lambda: update_image(image_processor.pencil())),
    ("Red", lambda: update_image(image_processor.red())),
    ("Green", lambda: update_image(image_processor.green())),
    ("Blue", lambda: update_image(image_processor.blue())),
    ("Blur", lambda: update_image(image_processor.blur())),
    ("Edge", lambda: update_image(image_processor.edge())),
    ("Sharpen", lambda: update_image(image_processor.sharpen())),
    (
        "Power Law Transform",
        lambda: update_image(image_processor.powlawtrans(gamma=1.5)),
    ),
]

for i, (text, command) in enumerate(function_buttons):
    Button(
        tool_bar,
        text=text,
        command=command,
        width=146,
        height=35,
        fg="#fbbf24",
        bg="#0f172a",
        activebackground=("#0f172a", "#0f172a"),
        borderless=1,
        bd=0,
        justify=CENTER,
        highlightthickness=0,
        relief="flat",
        focuscolor="#0f172a",
        highlightbackground="#0f172a",
        highlightcolor="#0f172a",
        activeforeground="#fbbf24",
    ).grid(row=i // 2, column=i % 2, padx=2, pady=5)

root.mainloop()
