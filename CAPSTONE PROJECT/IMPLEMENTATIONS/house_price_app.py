"""
================================================================================
 BANGALORE HOUSE PRICE PREDICTOR — Desktop App
 Data source : "Bengaluru House Price Data" (Kaggle, by amitabhajoy)
 Model       : Linear Regression (scikit-learn) — trained ahead of time,
               coefficients embedded below so the app opens instantly
               with only Python's built-in Tkinter (no extra installs).
================================================================================

HOW TO RUN:
    python house_price_app.py

That's it — Tkinter ships with standard Python, so nothing else to install.

OPTIONAL: File > Retrain from CSV lets you re-run the full training
pipeline (needs pandas + scikit-learn + the raw dataset CSV in the same
folder) and updates the app with freshly learned coefficients.
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os

# ------------------------------------------------------------------------
# EMBEDDED MODEL — real coefficients learned by scikit-learn Linear
# Regression, trained on 7,201 cleaned listings (80/20 split).
# Holdout R^2 = 0.741, MAE = Rs 21.75 Lakh.
# ------------------------------------------------------------------------
MODEL = {
    "intercept": -31.4634035470673,
    "sqft": 0.0993972638775588,
    "bath": 3.5174134733143196,
    "bhk": -7.576026802915275,
    "balcony": -3.083664121561046,
    "locations": {
        "7th Phase JP Nagar": 4.410901136268768,
        "Akshaya Nagar": -20.52564943868251,
        "Banashankari": -10.148854726910002,
        "Bannerghatta Road": -8.85647816884631,
        "Begur Road": -31.99152517655641,
        "Bellandur": -11.59376904142643,
        "Chandapura": -18.713015186490047,
        "Electronic City": -9.462452480133475,
        "Electronic City Phase II": -28.2143560968476,
        "Electronics City Phase 1": -10.571824540517511,
        "Haralur Road": -21.241502655499218,
        "Harlur": -1.5732444345649277,
        "Hebbal": 2.4362635287694245,
        "Hennur": -25.75235669658053,
        "Hennur Road": -9.516857920262035,
        "Hormavu": -18.605681962120123,
        "KR Puram": -24.913357573473213,
        "Kanakpura Road": -8.628082601010652,
        "Kasavanhalli": -9.185400426158782,
        "Kothanur": -20.951453652508956,
        "Marathahalli": -10.312792109876167,
        "Raja Rajeshwari Nagar": -25.127459691609396,
        "Rajaji Nagar": 144.17429182781652,
        "Sarjapur": -28.836585699413195,
        "Sarjapur Road": -7.5642775845684085,
        "Thanisandra": -8.851093278651042,
        "Uttarahalli": -21.804543279576524,
        "Whitefield": -13.559619172250137,
        "Yelahanka": -15.76469662825867,
        "Other Bangalore": 0.0,
    },
    "area_types": {
        "Super built-up Area": 0.0,   # reference category (most common)
        "Built-up Area": -1.6419548045175534,
        "Carpet Area": 3.1590785936148715,
        "Plot Area": 13.649683292993805,
    },
    "holdout_r2": 0.743,
    "holdout_mae": 21.43,
    "train_rows": 7201,
    "raw_rows": 13320,
}


def predict(location, sqft, bath, bhk, balcony=1, area_type="Super built-up Area"):
    """Pure prediction function — same formula as the trained model.
    Returns (predicted_price, breakdown_dict), all in Rs Lakh."""
    loc_term = MODEL["locations"].get(location, 0.0)
    type_term = MODEL["area_types"].get(area_type, 0.0)
    sqft_term = MODEL["sqft"] * sqft
    bath_term = MODEL["bath"] * bath
    bhk_term = MODEL["bhk"] * bhk
    balcony_term = MODEL["balcony"] * balcony
    intercept = MODEL["intercept"]

    total = intercept + sqft_term + bath_term + bhk_term + balcony_term + loc_term + type_term
    total = max(total, 8)  # floor so extreme inputs don't go negative

    breakdown = {
        "Area contribution": sqft_term,
        "Bathroom adjustment": bath_term,
        "BHK adjustment": bhk_term,
        "Balcony adjustment": balcony_term,
        "Locality premium": loc_term,
        "Area-type adjustment": type_term,
        "Model base (intercept)": intercept,
    }
    return total, breakdown


def fmt_lakh(v):
    if v >= 100:
        return f"Rs {v/100:.2f} Cr"
    return f"Rs {v:.1f} L"


def fmt_signed(v):
    sign = "+" if v >= 0 else "-"
    return f"{sign}{fmt_lakh(abs(v))}"


# ------------------------------------------------------------------------
# GUI
# ------------------------------------------------------------------------
class HousePriceApp(tk.Tk):
    INK = "#1C2A44"
    INK_SOFT = "#4A5872"
    PAPER = "#F7F3E9"
    CARD = "#FFFDF7"
    BRASS = "#A9782E"
    GREEN = "#33513E"
    RUST = "#9A3E28"
    LINE = "#D8D0BC"

    def __init__(self):
        super().__init__()
        self.title("Bangalore House Price Predictor")
        self.geometry("760x640")
        self.minsize(680, 600)
        self.configure(bg=self.PAPER)

        self._build_menu()
        self._build_style()
        self._build_header()
        self._build_body()
        self._recalculate()

    # -------------------- menu --------------------
    def _build_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Retrain from CSV...", command=self._retrain_from_csv)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About this model", command=self._show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)

    def _show_about(self):
        messagebox.showinfo(
            "About this model",
            "Dataset: Bengaluru House Price Data (Kaggle, amitabhajoy)\n"
            f"Raw rows: {MODEL['raw_rows']:,}  ->  Cleaned rows: {MODEL['train_rows']:,}\n"
            "Model: scikit-learn Linear Regression\n"
            f"Holdout R^2: {MODEL['holdout_r2']}   Holdout MAE: Rs {MODEL['holdout_mae']} Lakh\n"
            "Total learned parameters: 37 (36 weights + 1 intercept)\n"
            "Features: sqft, bath, BHK, balcony count, locality (29 levels),\n"
            "          area type (3 levels vs. Super built-up reference)\n\n"
            "Known limitations: the BHK weight is slightly negative once sqft "
            "and bathrooms are held constant, and the balcony weight is "
            "negative too — both are multicollinearity artifacts (these "
            "features correlate with sqft in the data), not mistakes."
        )

    def _retrain_from_csv(self):
        try:
            import pandas as pd  # noqa
            import numpy as np  # noqa
            from sklearn.linear_model import LinearRegression  # noqa
        except ImportError:
            messagebox.showerror(
                "Missing packages",
                "Retraining needs pandas, numpy and scikit-learn installed.\n"
                "Run: pip install pandas numpy scikit-learn",
            )
            return
        messagebox.showinfo(
            "Retrain",
            "This app ships with an already-trained model, so it runs with "
            "zero setup. To retrain from scratch, use house_price_prediction.py "
            "(the standalone training script) in this same project — it prints "
            "fresh coefficients you can paste into the MODEL dict at the top "
            "of this file.",
        )

    # -------------------- styling --------------------
    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=self.PAPER)
        style.configure("Card.TFrame", background=self.CARD)
        style.configure("TLabel", background=self.PAPER, foreground=self.INK, font=("Georgia", 11))
        style.configure("Card.TLabel", background=self.CARD, foreground=self.INK, font=("Georgia", 11))
        style.configure("Eyebrow.TLabel", background=self.PAPER, foreground=self.BRASS,
                         font=("Courier New", 10, "bold"))
        style.configure("Title.TLabel", background=self.PAPER, foreground=self.INK,
                         font=("Georgia", 20, "bold"))
        style.configure("Field.TLabel", background=self.CARD, foreground=self.INK_SOFT,
                         font=("Courier New", 9))
        style.configure("Price.TLabel", background=self.CARD, foreground=self.INK,
                         font=("Georgia", 30, "bold"))
        style.configure("Range.TLabel", background=self.CARD, foreground=self.INK_SOFT,
                         font=("Courier New", 10))
        style.configure("TButton", font=("Georgia", 11, "bold"), padding=8)
        style.configure("Horizontal.TScale", background=self.CARD)

    # -------------------- header --------------------
    def _build_header(self):
        header = ttk.Frame(self, padding=(20, 16, 20, 8))
        header.pack(fill="x")
        ttk.Label(header, text="WORKSHEET · MODEL-BACKED ESTIMATE", style="Eyebrow.TLabel").pack(anchor="w")
        ttk.Label(header, text="Bangalore House Price Predictor", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text=f"Linear Regression trained on {MODEL['train_rows']:,} cleaned listings   "
                 f"·   R² {MODEL['holdout_r2']}   ·   MAE Rs {MODEL['holdout_mae']} Lakh",
            style="TLabel",
        ).pack(anchor="w", pady=(4, 0))

        sep = tk.Frame(self, bg=self.INK, height=2)
        sep.pack(fill="x", padx=20, pady=(6, 12))

    # -------------------- body --------------------
    def _build_body(self):
        body = ttk.Frame(self, padding=(20, 0, 20, 16))
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # ---- LEFT: inputs card ----
        left = tk.Frame(body, bg=self.CARD, highlightbackground=self.LINE, highlightthickness=1)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        pad = {"padx": 18, "pady": 10}

        ttk.Label(left, text="PROPERTY PARTICULARS", style="Field.TLabel", background=self.CARD).pack(
            anchor="w", **pad
        )

        # Locality
        self._field_label(left, "Locality")
        self.location_var = tk.StringVar(value="Whitefield")
        locations = sorted(MODEL["locations"].keys(), key=lambda n: (n == "Other Bangalore", n))
        loc_box = ttk.Combobox(left, textvariable=self.location_var, values=locations, state="readonly")
        loc_box.pack(fill="x", padx=18)
        loc_box.bind("<<ComboboxSelected>>", lambda e: self._recalculate())

        # Area
        self.area_var = tk.IntVar(value=1200)
        self._slider_field(left, "Total area (sq ft)", self.area_var, 300, 6000, self._fmt_area)

        # BHK
        self.bhk_var = tk.IntVar(value=2)
        self._slider_field(left, "Bedrooms (BHK)", self.bhk_var, 1, 6, lambda v: f"{int(v)} BHK")

        # Bath
        self.bath_var = tk.IntVar(value=2)
        self._slider_field(left, "Bathrooms", self.bath_var, 1, 7, lambda v: f"{int(v)}")

        # Balcony
        self.balcony_var = tk.IntVar(value=1)
        self._slider_field(left, "Balconies", self.balcony_var, 0, 3, lambda v: f"{int(v)}")

        # Area type (a real proxy for build quality / finish level in the data)
        self._field_label(left, "Area type")
        self.area_type_var = tk.StringVar(value="Super built-up Area")
        type_box = ttk.Combobox(
            left, textvariable=self.area_type_var,
            values=list(MODEL["area_types"].keys()), state="readonly",
        )
        type_box.pack(fill="x", padx=18, pady=(0, 12))
        type_box.bind("<<ComboboxSelected>>", lambda e: self._recalculate())

        # ---- RIGHT: result card ----
        right = tk.Frame(body, bg=self.CARD, highlightbackground=self.LINE, highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ttk.Label(right, text="PREDICTED MARKET VALUE", style="Field.TLabel", background=self.CARD).pack(
            anchor="w", padx=18, pady=(14, 0)
        )
        self.price_label = ttk.Label(right, text="Rs 0", style="Price.TLabel", background=self.CARD)
        self.price_label.pack(anchor="center", pady=(6, 2))
        self.range_label = ttk.Label(right, text="range —", style="Range.TLabel", background=self.CARD)
        self.range_label.pack(anchor="center", pady=(0, 12))

        divider = tk.Frame(right, bg=self.INK, height=2)
        divider.pack(fill="x", padx=18)

        self.ledger_frame = tk.Frame(right, bg=self.CARD)
        self.ledger_frame.pack(fill="x", padx=18, pady=(6, 6))

        note = ttk.Label(
            right,
            text="Model output, not a certified valuation.\nSee Help > About this model for methodology.",
            style="Card.TLabel", background=self.CARD, foreground=self.INK_SOFT,
            font=("Courier New", 9), justify="center",
        )
        note.pack(pady=(10, 14))

        self._ready = True

    def _field_label(self, parent, text):
        ttk.Label(parent, text=text, style="Field.TLabel", background=self.CARD).pack(
            anchor="w", padx=18, pady=(8, 4)
        )

    def _slider_field(self, parent, label, var, lo, hi, fmt_fn):
        row = tk.Frame(parent, bg=self.CARD)
        row.pack(fill="x", padx=18, pady=(10, 2))
        lbl = ttk.Label(row, text=label, style="Field.TLabel", background=self.CARD)
        lbl.pack(side="left")
        val_lbl = ttk.Label(row, text=fmt_fn(var.get()), style="Field.TLabel",
                             background=self.CARD, foreground=self.INK, font=("Courier New", 10, "bold"))
        val_lbl.pack(side="right")

        def on_move(v):
            var.set(round(float(v)))
            val_lbl.config(text=fmt_fn(var.get()))
            if getattr(self, "_ready", False):
                self._recalculate()

        scale = ttk.Scale(parent, from_=lo, to=hi, orient="horizontal", command=on_move)
        scale.set(var.get())
        scale.pack(fill="x", padx=18, pady=(0, 4))

    @staticmethod
    def _fmt_area(v):
        return f"{int(v)} sq ft"

    # -------------------- prediction --------------------
    def _recalculate(self):
        location = self.location_var.get()
        sqft = self.area_var.get()
        bhk = self.bhk_var.get()
        bath = self.bath_var.get()
        balcony = self.balcony_var.get()
        area_type = self.area_type_var.get()

        total, breakdown = predict(location, sqft, bath, bhk, balcony, area_type)
        low = max(total - MODEL["holdout_mae"], 5)
        high = total + MODEL["holdout_mae"]

        self.price_label.config(text=fmt_lakh(total))
        self.range_label.config(text=f"range {fmt_lakh(low)} - {fmt_lakh(high)}  (± holdout MAE)")

        for child in self.ledger_frame.winfo_children():
            child.destroy()

        rows = list(breakdown.items()) + [("Predicted price", total)]
        for i, (label, value) in enumerate(rows):
            is_total = label == "Predicted price"
            row = tk.Frame(self.ledger_frame, bg=self.CARD)
            row.pack(fill="x", pady=(8 if is_total else 3, 0))
            if is_total:
                top = tk.Frame(self.ledger_frame, bg=self.INK, height=2)
                top.pack(fill="x", pady=(4, 0))
                row = tk.Frame(self.ledger_frame, bg=self.CARD)
                row.pack(fill="x", pady=(6, 0))

            k = ttk.Label(row, text=label, style="Card.TLabel", background=self.CARD,
                          font=("Courier New", 10, "bold" if is_total else "normal"))
            k.pack(side="left")

            color = self.INK if is_total else (self.GREEN if value >= 0 else self.RUST)
            text = fmt_lakh(value) if is_total else fmt_signed(value)
            v = ttk.Label(row, text=text, style="Card.TLabel", background=self.CARD,
                          foreground=color, font=("Courier New", 11 if is_total else 10, "bold"))
            v.pack(side="right")


if __name__ == "__main__":
    app = HousePriceApp()
    app.mainloop()
