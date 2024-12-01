import math
from collections import defaultdict
from tkinter import Tk, filedialog, Label, Button, Text, END, Scrollbar, Frame
from tkinter import font as tkfont

def read_exe_file(file_path):
    """Reads binary content from the selected file."""
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def convert_to_hex_bytes(data):
    """Converts binary data to a hex string."""
    return data.hex()

def divide_hex_data(hex_data, parts, start, chunk_size=8):
    """Divide the hex data into chunks and count occurrences."""
    part_length = len(hex_data) // parts
    my_dict = defaultdict(int)

    for i in range(start, start + part_length, chunk_size * 2):  
        chunk = hex_data[i:i + chunk_size * 2]
        my_dict[chunk] += 1

    return my_dict

def calculate_entropy(data_dict, chunk_count):
    """Calculate Shannon entropy from a frequency dictionary."""
    entropy = -sum((freq / chunk_count) * math.log(freq / chunk_count) for freq in data_dict.values())
    return entropy

def calculate_entropies(file_path, parts=10, chunk_size=8):
    """Main function to calculate entropies over parts of a file."""
    exe_data = read_exe_file(file_path)
    if exe_data is None:
        return []

    hex_data = convert_to_hex_bytes(exe_data)
    hex_length = len(hex_data)
    part_length = hex_length // parts
    total_chunks = (part_length // (chunk_size * 2))  
    entropies = []

    for i in range(parts):
        start = i * part_length
        data_dict = divide_hex_data(hex_data, parts, start, chunk_size)
        entropy = calculate_entropy(data_dict, total_chunks)
        entropies.append(entropy)

    return entropies


def browse_file():
    """Opens a file dialog to select a file."""
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        file_label.config(text=f"Selected File: {file_path}")
        calculate_and_display_entropy(file_path)

def calculate_and_display_entropy(file_path):
    """Calculate entropies and display them in the GUI."""
    parts = 5
    chunk_size = 8
    entropies = calculate_entropies(file_path, parts=parts, chunk_size=chunk_size)
    
    result_text.delete(1.0, END)
    if entropies:
        result_text.insert(END, f"Entropies for {parts} parts:\n\n")
        for i, entropy in enumerate(entropies):
            result_text.insert(END, f"Part {i+1}: {entropy:.4f}\n")
    else:
        result_text.insert(END, "Error: Could not calculate entropies.\n")


root = Tk()
root.title("Entropy Calculator")
root.geometry("600x500")
root.config(bg="#f4f4f9")  


title_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
button_font = tkfont.Font(family="Helvetica", size=12)
text_font = tkfont.Font(family="Courier", size=10)


frame = Frame(root, bg="#f4f4f9")
frame.pack(pady=20)


file_label = Label(frame, text="No file selected", wraplength=550, anchor="w", justify="left", font=title_font, bg="#f4f4f9")
file_label.grid(row=0, column=0, padx=10, pady=10)


browse_button = Button(frame, text="Browse File", command=browse_file, font=button_font, bg="#4CAF50", fg="white", relief="flat", width=20)
browse_button.grid(row=1, column=0, pady=10)


scrollbar = Scrollbar(frame)
scrollbar.grid(row=2, column=1, sticky="ns", pady=10)

result_text = Text(frame, height=15, width=70, wrap="word", font=text_font, bg="#f1f1f1", fg="#333333", bd=0, yscrollcommand=scrollbar.set)
result_text.grid(row=2, column=0, padx=10, pady=10)

scrollbar.config(command=result_text.yview)


exit_button = Button(root, text="Exit", command=root.quit, font=button_font, bg="#FF5722", fg="white", relief="flat", width=20)
exit_button.pack(pady=10)

root.mainloop()
