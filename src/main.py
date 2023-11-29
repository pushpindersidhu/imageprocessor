from tkinter import *
from tkmacosx import Button
from PIL import ImageTk
from image_processor import ImageProcessor
from tkinter import ttk

root = Tk()
image_processor = ImageProcessor()
root.title("Image Processor")
root.geometry("1000x600")
root.resizable(False, False)
root.config(bg="#020617")

style = ttk.Style()

style.theme_create(
    "theme",
    parent="alt",
    settings={
        "TNotebook": {
            "configure": {
                "tabmargins": [2, 5, 2, 0],
                "background": "#020617",
                "foreground": "#d1d5db",
                "borderwidth": 0,
                "bordercolor": "#0f172a",
                "tabposition": "n",
            }
        },
        "TNotebook.Tab": {
            "configure": {
                "padding": [5, 5],
                "margin": [0, 0],
                "background": "#020617",
                "foreground": "#d1d5db",
                "borderwidth": 0,
                "relief": "flat",
            },
            "map": {
                "background": [("selected", "#0f172a")],
                "foreground": [("selected", "#fbbf24")],
                "expand": [("selected", [1, 1, 1, 0])],
            },
        },
    },
)

style.theme_use("theme")


def update_image(modifiedPILImage=None):
    modified_image = None

    if modifiedPILImage is None:
        new_image = image_processor.get_image()
        image_processor.modified_image = new_image

        origional_image = ImageTk.PhotoImage(new_image.resize((300, 300)))
        original_label.config(image=origional_image)
        original_label.image = origional_image

        modified_image = ImageTk.PhotoImage(new_image.resize((650, 525)))
    else:
        image_processor.modified_image = modifiedPILImage
        modifiedPILImage = modifiedPILImage.resize((650, 525))
        modified_image = ImageTk.PhotoImage(modifiedPILImage)

    modified_label.config(image=modified_image)
    modified_label.image = modified_image


left_frame = Frame(root, width=300, height=600, bg="#020617")
left_frame.grid(row=0, column=0, padx=5, pady=5, sticky=NW, columnspan=2)

right_frame = Frame(root, width=700, height=600, bg="#020617")
right_frame.grid(row=0, column=2, padx=5, pady=5, columnspan=2, sticky=NW)

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

Label(right_frame, text="Modified", bg="#020617", fg="#ffffff", justify=LEFT).grid(
    row=0, column=0, padx=0, pady=5, columnspan=1, sticky=W
)

Button(
    right_frame,
    text="Save Image",
    command=lambda: image_processor.save(),
    height=32,
    width=100,
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
).grid(row=0, column=1, padx=0, pady=5, columnspan=1, sticky=E)


modified_label = Label(
    right_frame, bg="#020617", fg="#ffffff", width=650, height=525
)
modified_label.grid(row=1, column=0, padx=0, pady=5, columnspan=2, sticky=W)

update_image()

tool_bar = ttk.Notebook(
    left_frame,
    width=300,
)
tool_bar.grid(row=2, column=0, padx=1, pady=5, columnspan=4, sticky=W)

function_buttons = {
    "Effects": [
        ("Grayscale", lambda: update_image(image_processor.grayscale())),
        ("Negative", lambda: update_image(image_processor.negative())),
        ("Pencil Sketch", lambda: update_image(image_processor.pencil())),
        (
            "Gaussian Blur",
            lambda: update_image(image_processor.gaussian(kernel_size=(10, 10))),
        ),
        ("Edge Detection", lambda: update_image(image_processor.edge())),
        ("Sharpen", lambda: update_image(image_processor.sharpen())),
        ("Emboss", lambda: update_image(image_processor.emboss())),
        ("Median Filter", lambda: update_image(image_processor.median_filter())),
    ],
    "Adjustments": [
        ("Threshold", lambda: update_image(image_processor.threshold())),
        ("Sepia", lambda: update_image(image_processor.sepia())),
        ("Cartoonize", lambda: update_image(image_processor.cartoonize())),
        ("Power Law", lambda: update_image(image_processor.powlawtrans())),
    ],
    "Orientation": [
        ("Rotate 90 degrees", lambda: update_image(image_processor.rotate(90))),
        ("Rotate 180 degrees", lambda: update_image(image_processor.rotate(180))),
        ("Rotate 270 degrees", lambda: update_image(image_processor.rotate(270))),
        ("Flip Horizontal", lambda: update_image(image_processor.flip_horizontal())),
        ("Flip Vertical", lambda: update_image(image_processor.flip_vertical())),
        ("Fish Eye", lambda: update_image(image_processor.fish_eye())),
        ("Shear X", lambda: update_image(image_processor.shear_x())),
        ("Shear Y", lambda: update_image(image_processor.shear_y())),
    ],
    "Channels": [
        ("Invert Colors", lambda: update_image(image_processor.invert_colors())),
        ("Red Channel", lambda: update_image(image_processor.red())),
        ("Green Channel", lambda: update_image(image_processor.green())),
        ("Blue Channel", lambda: update_image(image_processor.blue())),
    ],
}

for category, buttons in function_buttons.items():
    tab = Frame(
        tool_bar,
        width=200,
        height=600,
        bg="#020617",
        border=0,
        highlightcolor="#0f172a",
        highlightthickness=1,
        bd=0,
        relief="flat",
    )
    tool_bar.add(tab, text=category)
    for i, (text, command) in enumerate(buttons):
        Button(
            tab,
            text=text,
            command=command,
            width=140,
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
        ).grid(row=i // 2, column=i % 2, padx=4, pady=5)

menubar = Menu(root)

for category, buttons in function_buttons.items():
    category_menu = Menu(menubar, tearoff=0)
    for button_text, command in buttons:
        category_menu.add_command(label=button_text, command=command)
    menubar.add_cascade(label=category, menu=category_menu)

root.config(menu=menubar)

root.mainloop()
