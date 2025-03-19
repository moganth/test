import tkinter as tk
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_URL = "http://localhost:12354/reports/patient_counts"


def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def plot_chart(frame, chart_type):
    data = fetch_data()
    if not data:
        return

    names = [item["name"] for item in data]
    report_counts = [item["report_count"] for item in data]

    fig_width = max(8, len(names) * 0.8)
    fig, ax = plt.subplots(figsize=(fig_width, 5))

    if chart_type == "Bar Chart":
        ax.bar(names, report_counts, color="skyblue")
        ax.set_xlabel("Patients")
        ax.set_ylabel("Number of Reports")
        ax.set_title("Patient Reports Distribution")

        rotation_angle = 0 if len(names) <= 5 else 45
        ax.set_xticklabels(names, rotation=rotation_angle, ha="right")

        plt.tight_layout()

    elif chart_type == "Pie Chart":
        colors = ["lightcoral", "lightskyblue", "lightgreen", "gold", "violet"]
        ax.pie(report_counts, labels=names, autopct="%1.1f%%", colors=colors, startangle=140)
        ax.set_title("Patient Reports Distribution")

    elif chart_type == "Donut Chart":
        colors = ["lightcoral", "lightskyblue", "lightgreen", "gold", "violet"]
        wedges, texts, autotexts = ax.pie(report_counts, labels=names, autopct="%1.1f%%",
                                          colors=colors, startangle=140, wedgeprops={'width': 0.4})
        ax.set_title("Patient Reports Distribution")

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def run_gui():
    root = tk.Tk()
    root.title("Patient Report Visualization")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    chart_type_var = tk.StringVar(root)
    chart_type_var.set("Bar Chart")

    chart_dropdown = tk.OptionMenu(root, chart_type_var, "Bar Chart", "Pie Chart", "Donut Chart")
    chart_dropdown.pack(pady=5)

    btn = tk.Button(root, text="Show Report Chart", command=lambda: plot_chart(frame, chart_type_var.get()))
    btn.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
