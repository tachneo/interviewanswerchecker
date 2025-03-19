import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import requests
import warnings
import urllib3
import re
import datetime
from google import genai

# For charting with matplotlib
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -----------------------------
# Disable SSL verification globally
# -----------------------------
_original_request = requests.Session.request
def no_verify_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return _original_request(self, method, url, **kwargs)
requests.Session.request = no_verify_request

warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)

# Replace with your actual Gemini API key. pip install -q -U google-genai
API_KEY = "AI"
client = genai.Client(api_key=API_KEY)

# -----------------------------
# Main Window Setup
# -----------------------------
root = tk.Tk()
root.title("Advanced Interview Evaluation Tool")
root.geometry("1200x850")
root.configure(bg="#f0f8ff")

# -----------------------------
# Menu Bar Setup
# -----------------------------
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Export Evaluation", command=lambda: export_evaluation())
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# -----------------------------
# Create a PanedWindow for two-column layout
# -----------------------------
paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left frame: Inputs and Evaluation Output
left_frame = ttk.Frame(paned, padding="10")
paned.add(left_frame, weight=3)

# Right frame: Reporting, Score Card & Certificate Option
right_frame = ttk.Frame(paned, padding="10")
paned.add(right_frame, weight=1)

# -----------------------------
# Left Frame Layout
# -----------------------------
title_label = ttk.Label(left_frame, text="Interview Evaluation Tool", font=("Helvetica", 22, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Candidate Name Input
candidate_name_label = ttk.Label(left_frame, text="Candidate Name:", font=("Helvetica", 14, "bold"))
candidate_name_label.grid(row=1, column=0, sticky="w", pady=(5, 2))
candidate_name_entry = ttk.Entry(left_frame, width=70, font=("Helvetica", 12))
candidate_name_entry.grid(row=1, column=1, pady=(5, 2), sticky="w")

# Interview Question
question_label = ttk.Label(left_frame, text="Interview Question:", font=("Helvetica", 14, "bold"))
question_label.grid(row=2, column=0, sticky="w", pady=(5, 2))
question_text = scrolledtext.ScrolledText(left_frame, height=4, width=70, font=("Helvetica", 12),
                                          wrap="word", bd=2, relief="groove")
question_text.grid(row=3, column=0, columnspan=2, pady=(0, 15))

# Candidate Answer
cand_answer_label = ttk.Label(left_frame, text="Candidate's Answer:", font=("Helvetica", 14, "bold"))
cand_answer_label.grid(row=4, column=0, sticky="w", pady=(5, 2))
cand_answer_text = scrolledtext.ScrolledText(left_frame, height=6, width=70, font=("Helvetica", 12),
                                             wrap="word", bd=2, relief="groove")
cand_answer_text.grid(row=5, column=0, columnspan=2, pady=(0, 15))

# Buttons Frame for Evaluate, Clear, and Generate Certificate actions
buttons_frame = ttk.Frame(left_frame)
buttons_frame.grid(row=6, column=0, columnspan=2, pady=(5, 15), sticky="ew")
evaluate_button = ttk.Button(buttons_frame, text="Evaluate Answer", command=lambda: evaluate_candidate_answer())
evaluate_button.pack(side=tk.LEFT, padx=(5, 10))
clear_button = ttk.Button(buttons_frame, text="Clear", command=lambda: clear_fields())
clear_button.pack(side=tk.LEFT, padx=(5, 10))
certificate_button = ttk.Button(buttons_frame, text="Generate Certificate", command=lambda: generate_certificate())
certificate_button.pack(side=tk.LEFT, padx=(5, 10))

# Colorful Evaluation Output
output_label = ttk.Label(left_frame, text="Evaluation Output:", font=("Helvetica", 14, "bold"))
output_label.grid(row=7, column=0, sticky="w", pady=(5, 2))
evaluation_output = scrolledtext.ScrolledText(left_frame, height=12, width=70, font=("Helvetica", 12),
                                              wrap="word", bd=2, relief="groove")
evaluation_output.grid(row=8, column=0, columnspan=2, pady=(0, 15))
evaluation_output.config(state=tk.DISABLED)

# Define tags for colorful output in evaluation window
evaluation_output.tag_config("score", foreground="blue", font=("Helvetica", 16, "bold"))
evaluation_output.tag_config("result_pass", foreground="green", font=("Helvetica", 16, "bold"))
evaluation_output.tag_config("result_fail", foreground="red", font=("Helvetica", 16, "bold"))
evaluation_output.tag_config("analysis", foreground="black", font=("Helvetica", 12))

# -----------------------------
# Right Frame Layout (Reporting & Score Card)
# -----------------------------
scorecard_title = ttk.Label(right_frame, text="Score Card", font=("Helvetica", 20, "bold"))
scorecard_title.pack(pady=(0, 10))

# Label to display the numeric score
score_label = ttk.Label(right_frame, text="Score: N/A", font=("Helvetica", 16))
score_label.pack(pady=(0, 10))

# Chart container for matplotlib chart
chart_container = ttk.Frame(right_frame)
chart_container.pack(pady=(0, 15), fill=tk.BOTH, expand=True)

# Evaluation Details frame for strengths, weaknesses, and recommendation
details_frame = ttk.LabelFrame(right_frame, text="Evaluation Details", padding="10")
details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
strengths_label = ttk.Label(details_frame, text="Strengths:", font=("Helvetica", 12, "bold"))
strengths_label.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
strengths_text = tk.Text(details_frame, height=4, width=30, font=("Helvetica", 10),
                         wrap="word", bd=2, relief="groove")
strengths_text.grid(row=1, column=0, padx=5, pady=5)
weaknesses_label = ttk.Label(details_frame, text="Weaknesses:", font=("Helvetica", 12, "bold"))
weaknesses_label.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
weaknesses_text = tk.Text(details_frame, height=4, width=30, font=("Helvetica", 10),
                          wrap="word", bd=2, relief="groove")
weaknesses_text.grid(row=1, column=1, padx=5, pady=5)
recommendation_label = ttk.Label(details_frame, text="Recommendation:", font=("Helvetica", 12, "bold"))
recommendation_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
recommendation_text = ttk.Label(details_frame, text="N/A", font=("Helvetica", 12))
recommendation_text.grid(row=2, column=1, sticky="w", padx=5, pady=5)

# Options frame for additional reporting features
options_frame = ttk.LabelFrame(right_frame, text="Options", padding="10")
options_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
show_chart_var = tk.BooleanVar(value=True)
show_chart_check = ttk.Checkbutton(options_frame, text="Show Score Chart", variable=show_chart_var)
show_chart_check.grid(row=0, column=0, sticky="w", padx=5, pady=5)
show_details_var = tk.BooleanVar(value=True)
show_details_check = ttk.Checkbutton(options_frame, text="Show Detailed Analysis", variable=show_details_var)
show_details_check.grid(row=0, column=1, sticky="w", padx=5, pady=5)
export_button = ttk.Button(right_frame, text="Export Evaluation", command=lambda: export_evaluation())
export_button.pack(pady=(10, 5))

# Status bar at the bottom of the window
status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor="w")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Global variable to hold chart canvas
chart_canvas = None

# -----------------------------
# Functions for App Logic
# -----------------------------
def update_chart(evaluation_text):
    """Update the score chart on the right pane based on the extracted score."""
    global chart_canvas
    # Capture any text following "Score:" (even if not numeric)
    score_match = re.search(r"Score:\s*(.+)", evaluation_text, re.IGNORECASE)
    if score_match:
        score_str = score_match.group(1).strip()
        try:
            score = int(score_str)
        except:
            score = 0  # if not numeric, default chart score to 0
        score_label.config(text=f"Score: {score_str}")
    else:
        score = 0
        score_label.config(text="Score: N/A")
    
    if not show_chart_var.get():
        if chart_canvas:
            chart_canvas.get_tk_widget().destroy()
        return
    
    fig = Figure(figsize=(4, 2), dpi=100)
    ax = fig.add_subplot(111)
    ax.barh(["Score"], [score], color="#4CAF50")
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score (%)", fontsize=10)
    ax.set_title("Candidate Score", fontsize=12)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
    chart_canvas = FigureCanvasTkAgg(fig, master=chart_container)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack()

def update_details(evaluation_text):
    """Extract and update strengths, weaknesses, and recommendation details."""
    strengths = "Not specified"
    weaknesses = "Not specified"
    recommendation = "Not specified"
    
    strengths_match = re.search(r"Strengths:\s*(.+)", evaluation_text, re.IGNORECASE)
    if strengths_match:
        strengths = strengths_match.group(1).strip()
    weaknesses_match = re.search(r"Weaknesses:\s*(.+)", evaluation_text, re.IGNORECASE)
    if weaknesses_match:
        weaknesses = weaknesses_match.group(1).strip()
    recommendation_match = re.search(r"Recommendation:\s*(.+)", evaluation_text, re.IGNORECASE)
    if recommendation_match:
        recommendation = recommendation_match.group(1).strip()
    
    strengths_text.delete("1.0", tk.END)
    strengths_text.insert(tk.END, strengths)
    weaknesses_text.delete("1.0", tk.END)
    weaknesses_text.insert(tk.END, weaknesses)
    recommendation_text.config(text=recommendation)

def display_formatted_evaluation(evaluation):
    """
    Parse the evaluation text and display it in the evaluation_output widget 
    with a colorful and structured format.
    Expected format:
      Score: <number or text>
      Recommendation: <Pass/Fail or text>
      Analysis: <detailed explanation>
    """
    evaluation_output.config(state=tk.NORMAL)
    evaluation_output.delete("1.0", tk.END)
    
    score_match = re.search(r"Score:\s*(.+)", evaluation, re.IGNORECASE)
    result_match = re.search(r"Recommendation:\s*(.+)", evaluation, re.IGNORECASE)
    analysis_match = re.search(r"Analysis:\s*(.+)", evaluation, re.IGNORECASE | re.DOTALL)
    
    score_text = f"Score: {score_match.group(1).strip()}\n" if score_match else "Score: N/A\n"
    result_text = f"Recommendation: {result_match.group(1).strip()}\n\n" if result_match else "Recommendation: N/A\n\n"
    analysis_text = f"Analysis:\n{analysis_match.group(1).strip()}\n" if analysis_match else evaluation
    
    evaluation_output.insert(tk.END, score_text, "score")
    # Use pass/fail tag based on text if possible
    result_lower = result_match.group(1).strip().lower() if result_match else ""
    result_tag = "result_pass" if "pass" in result_lower else "result_fail"
    evaluation_output.insert(tk.END, result_text, result_tag)
    evaluation_output.insert(tk.END, analysis_text, "analysis")
    
    evaluation_output.config(state=tk.DISABLED)

def clear_fields():
    """Clear all input and output fields."""
    question_text.delete("1.0", tk.END)
    cand_answer_text.delete("1.0", tk.END)
    candidate_name_entry.delete(0, tk.END)
    evaluation_output.config(state=tk.NORMAL)
    evaluation_output.delete("1.0", tk.END)
    evaluation_output.config(state=tk.DISABLED)
    score_label.config(text="Score: N/A")
    strengths_text.delete("1.0", tk.END)
    weaknesses_text.delete("1.0", tk.END)
    recommendation_text.config(text="N/A")
    global chart_canvas
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()
    status_bar.config(text="Cleared fields.")

def export_evaluation():
    """Export the evaluation output to a text file."""
    eval_text = evaluation_output.get("1.0", tk.END).strip()
    if not eval_text:
        messagebox.showwarning("Export Warning", "No evaluation data to export!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(eval_text)
            messagebox.showinfo("Export Success", "Evaluation exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting evaluation: {e}")

def evaluate_candidate_answer():
    """
    Evaluate the candidate's answer using the Gemini API.
    The prompt instructs the API to output a structured evaluation.
    NOTE: Ensure that the score is on a scale of 0-100. If the answer is fully correct,
    the score should be 90 or above.
    """
    candidate_name = candidate_name_entry.get().strip()
    question = question_text.get("1.0", tk.END).strip()
    candidate_answer = cand_answer_text.get("1.0", tk.END).strip()
    
    if not question or not candidate_answer:
        evaluation_output.config(state=tk.NORMAL)
        evaluation_output.delete("1.0", tk.END)
        evaluation_output.insert(tk.END, "Please enter the interview question and candidate's answer.\n")
        evaluation_output.config(state=tk.DISABLED)
        status_bar.config(text="Error: Missing inputs.")
        return
    
    prompt = (
        "You are an expert interviewer. Evaluate the candidate's answer to the following interview question.\n\n"
        f"Candidate Name: {candidate_name if candidate_name else 'N/A'}\n"
        f"Question: {question}\n\n"
        f"Candidate's Answer: {candidate_answer}\n\n"
        "Please provide your evaluation in the following format:\n"
        "Score: <number>  (score out of 100; if the answer is fully correct, score should be 90 or above)\n"
        "Recommendation: <Pass/Fail>\n"
        "Analysis: <detailed explanation of performance>\n"
        "Strengths: <list of strengths>\n"
        "Weaknesses: <list of weaknesses>\n"
    )
    
    evaluation_output.config(state=tk.NORMAL)
    evaluation_output.delete("1.0", tk.END)
    evaluation_output.insert(tk.END, "Evaluating candidate's answer...\n", "analysis")
    evaluation_output.config(state=tk.DISABLED)
    status_bar.config(text="Evaluating...")
    root.update()
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        evaluation = response.text
    except Exception as e:
        evaluation = f"Error: {e}"
    
    display_formatted_evaluation(evaluation)
    status_bar.config(text="Evaluation completed.")
    
    update_chart(evaluation)
    if show_details_var.get():
        update_details(evaluation)

def generate_certificate():
    """
    Generate a minimal certificate-style report card in a new window.
    The certificate shows the candidate name, score, result, date, and a brief evaluation summary.
    """
    candidate_name = candidate_name_entry.get().strip() or "Candidate"
    evaluation_text = evaluation_output.get("1.0", tk.END).strip()
    if not evaluation_text:
        messagebox.showwarning("Certificate Warning", "No evaluation data available to generate certificate!")
        return

    # Capture score and recommendation using flexible regex
    score_match = re.search(r"Score:\s*(.+)", evaluation_text, re.IGNORECASE)
    recommendation_match = re.search(r"Recommendation:\s*(.+)", evaluation_text, re.IGNORECASE)
    analysis_match = re.search(r"Analysis:\s*(.+)", evaluation_text, re.IGNORECASE | re.DOTALL)
    
    score_val = score_match.group(1).strip() if score_match else "N/A"
    recommendation_val = recommendation_match.group(1).strip() if recommendation_match else "N/A"
    analysis_val = analysis_match.group(1).strip() if analysis_match else ""
    
    # Truncate the evaluation summary to keep certificate minimal
    analysis_summary = analysis_val[:150] + "..." if len(analysis_val) > 150 else analysis_val

    cert_win = tk.Toplevel(root)
    cert_win.title("Certificate of Evaluation")
    cert_win.geometry("800x600")
    cert_win.configure(bg="white")
    
    canvas = tk.Canvas(cert_win, width=780, height=580, bg="white")
    canvas.pack(padx=10, pady=10)
    
    # Draw certificate border
    canvas.create_rectangle(10, 10, 770, 570, width=4, outline="#4CAF50")
    
    # Certificate Title
    canvas.create_text(390, 60, text="Certificate of Evaluation",
                       font=("Times New Roman", 28, "bold"), fill="#333")
    
    # Candidate Name
    canvas.create_text(390, 120, text=f"{candidate_name}", font=("Times New Roman", 24, "bold"), fill="#555")
    
    # Score and Recommendation
    canvas.create_text(390, 180, text=f"Score: {score_val}", font=("Times New Roman", 20), fill="blue")
    result_color = "green" if "pass" in recommendation_val.lower() else "red"
    canvas.create_text(390, 220, text=f"Result: {recommendation_val.upper()}", font=("Times New Roman", 20), fill=result_color)
    
    # Date
    today = datetime.datetime.today().strftime("%B %d, %Y")
    canvas.create_text(390, 260, text=f"Date: {today}", font=("Times New Roman", 16), fill="#777")
    
    # Minimal Evaluation Summary
    canvas.create_text(390, 320, text="Summary", font=("Times New Roman", 20, "underline"), fill="#333")
    canvas.create_text(390, 380, text=analysis_summary,
                       font=("Times New Roman", 14), fill="#333", width=700)
    
    # Signature Lines
    canvas.create_line(100, 500, 300, 500, fill="#333", width=2)
    canvas.create_line(480, 500, 680, 500, fill="#333", width=2)
    canvas.create_text(200, 520, text="Interviewer Signature", font=("Times New Roman", 14), fill="#333")
    canvas.create_text(580, 520, text="Evaluator Signature", font=("Times New Roman", 14), fill="#333")

# -----------------------------
# Start the GUI event loop
# -----------------------------
root.mainloop()
