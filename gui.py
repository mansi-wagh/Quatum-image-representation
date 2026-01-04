import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import time

from utils.universal_loader import load_image_any
from models.frqi import frqi_encode
from models.neqr import neqr_encode

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ===================== WINDOW =====================
root = tk.Tk()
root.title("Quantum Image Representation")
root.geometry("1200x750")
root.resizable(False, False)

# ===================== GLOBALS =====================
current_path = None
current_array = None

# ===================== TITLES =====================
tk.Label(root, text="Input Image", font=("Arial", 11, "bold")).place(x=40, y=5)
tk.Label(root, text="Quantum Image", font=("Arial", 11, "bold")).place(x=350, y=5)

# ===================== IMAGE PANELS =====================
input_label = tk.Label(root, relief="solid")
input_label.place(x=40, y=30, width=256, height=256)

quantum_label = tk.Label(root, relief="solid")
quantum_label.place(x=350, y=30, width=256, height=256)

# ===================== STATS PANEL =====================
stats_label = tk.Label(
    root,
    text="Time:\nSpace:",
    relief="solid",
    width=28,
    height=5,
    font=("Arial", 10, "bold"),
    justify="center"
)
stats_label.place(x=880, y=260)

# ===================== CIRCUIT FRAME =====================
circuit_frame = tk.LabelFrame(
    root,
    text="Quantum Circuit Representation",
    padx=10,
    pady=10
)
circuit_frame.place(x=40, y=380, width=1120, height=300)

# ===================== FUNCTIONS =====================
def load_image():
    global current_path, current_array

    current_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.mat")]
    )

    if not current_path:
        return

    # Load numerical data for quantum encoding
    current_array = load_image_any(current_path)

    # Show clear input preview (NOT downsampled)
    if current_path.lower().endswith((".png", ".jpg", ".jpeg")):
        img = Image.open(current_path).convert("L")
        img = img.resize((256, 256), Image.BILINEAR)
    else:
        # MAT preview
        preview = (current_array * 255).astype("uint8")
        img = Image.fromarray(preview).resize((256, 256), Image.BILINEAR)

    tk_img = ImageTk.PhotoImage(img)
    input_label.config(image=tk_img)
    input_label.image = tk_img


def show_quantum_image():
    # Pixelated quantum-style visualization
    small = Image.fromarray((current_array * 255).astype("uint8"))
    quantum_img = small.resize((256, 256), Image.NEAREST)

    tk_qimg = ImageTk.PhotoImage(quantum_img)
    quantum_label.config(image=tk_qimg)
    quantum_label.image = tk_qimg


def draw_circuit(qc):
    for widget in circuit_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(10, 3))
    ax = fig.add_subplot(111)
    ax.axis("off")

    qc.draw(output="mpl", ax=ax)

    canvas = FigureCanvasTkAgg(fig, master=circuit_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def run_frqi():
    if current_array is None:
        return

    start = time.time()
    qc, qubits = frqi_encode(current_array)
    elapsed = (time.time() - start) * 1000

    show_quantum_image()
    stats_label.config(
        text=f"FRQI\nTime: {elapsed:.2f} ms\nSpace: {qubits} qubits"
    )
    draw_circuit(qc)


def run_neqr():
    if current_array is None:
        return

    start = time.time()
    qc, qubits = neqr_encode(current_array)
    elapsed = (time.time() - start) * 1000

    show_quantum_image()
    stats_label.config(
        text=f"NEQR\nTime: {elapsed:.2f} ms\nSpace: {qubits} qubits"
    )
    draw_circuit(qc)

# ===================== CONTROL PANEL =====================
control_frame = tk.LabelFrame(root, text="Controls", padx=10, pady=10)
control_frame.place(x=40, y=300)

tk.Button(
    control_frame, text="Load Image", width=18, command=load_image
).grid(row=0, column=0, pady=5)

method_frame = tk.LabelFrame(control_frame, text="Quantum Method", padx=10, pady=5)
method_frame.grid(row=1, column=0, pady=8)

tk.Label(method_frame, text="NEQR").pack(anchor="w")
tk.Label(method_frame, text="FRQI").pack(anchor="w")

tk.Button(
    control_frame, text="Convert NEQR", width=18, command=run_neqr
).grid(row=2, column=0, pady=5)

tk.Button(
    control_frame, text="Convert FRQI", width=18, command=run_frqi
).grid(row=3, column=0, pady=5)

# ===================== START =====================
root.mainloop()
