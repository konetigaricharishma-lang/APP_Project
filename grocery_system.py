import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

# ============================================================
# GROCERY DELIVERY + BILLING SYSTEM
# Python Tkinter - Single File Project
# No database / no external packages required
# ============================================================

# -------------------- COLORS --------------------
BG = "#F4F7FB"
CARD = "#FFFFFF"
PRIMARY = "#176B4D"
PRIMARY_DARK = "#0F5138"
SECONDARY = "#E8F5EE"
ACCENT = "#FFB703"
DANGER = "#D9534F"
TEXT = "#1F2937"
MUTED = "#6B7280"
BORDER = "#D8DEE8"
LIGHT_GREEN = "#DFF3E8"

# -------------------- DATA --------------------
products = {
    "Rice (1 kg)": ("Groceries", 70),
    "Wheat Flour (1 kg)": ("Groceries", 55),
    "Sugar (1 kg)": ("Groceries", 48),
    "Toor Dal (1 kg)": ("Groceries", 140),
    "Cooking Oil (1 L)": ("Groceries", 135),
    "Salt (1 kg)": ("Groceries", 25),
    "Milk (1 L)": ("Dairy", 32),
    "Curd (500 g)": ("Dairy", 40),
    "Butter (100 g)": ("Dairy", 55),
    "Cheese (200 g)": ("Dairy", 110),
    "Bread": ("Bakery", 40),
    "Biscuits": ("Snacks", 30),
    "Chips": ("Snacks", 30),
    "Chocolate": ("Snacks", 60),
    "Apple (1 kg)": ("Fruits", 160),
    "Banana (1 dozen)": ("Fruits", 70),
    "Orange (1 kg)": ("Fruits", 100),
    "Tomato (1 kg)": ("Vegetables", 45),
    "Potato (1 kg)": ("Vegetables", 40),
    "Onion (1 kg)": ("Vegetables", 50),
    "Carrot (1 kg)": ("Vegetables", 60),
    "Coca Cola (750 ml)": ("Beverages", 45),
    "Juice (1 L)": ("Beverages", 100),
    "Mineral Water (1 L)": ("Beverages", 20),
    "Dish Wash Liquid": ("Household", 90),
    "Laundry Detergent": ("Household", 120),
}

categories = ["All"] + sorted(set(v[0] for v in products.values()))

# Demo users. New users are stored only while the program is running.
users = {
    "admin": {"password": "admin123", "name": "Administrator", "mobile": "9876543210",
              "email": "admin@example.com", "address": ""}
}

cart = {}
current_user = None
bill_number = 1001
current_order_number = None
last_order = None


# -------------------- APP --------------------
root = tk.Tk()
root.title("Grocery Delivery & Billing System")
root.geometry("1200x780")
root.minsize(1050, 700)
root.configure(bg=BG)


def clear_root():
    for widget in root.winfo_children():
        widget.destroy()


def make_button(parent, text, command, bg=PRIMARY, width=15):
    return tk.Button(
        parent, text=text, command=command,
        font=("Segoe UI", 10, "bold"),
        bg=bg, fg="white", activebackground=PRIMARY_DARK,
        activeforeground="white", relief="flat", bd=0,
        cursor="hand2", padx=12, pady=8, width=width
    )


def card(parent, padx=18, pady=15):
    frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                     highlightthickness=1)
    frame.pack(fill="x", padx=padx, pady=pady)
    return frame


def label(parent, text, size=10, bold=False, color=TEXT):
    return tk.Label(
        parent, text=text,
        font=("Segoe UI", size, "bold" if bold else "normal"),
        bg=parent.cget("bg"), fg=color
    )


def entry(parent, width=28, show=None):
    return tk.Entry(
        parent, font=("Segoe UI", 10), width=width,
        show=show, relief="solid", bd=1,
        highlightthickness=1, highlightbackground=BORDER
    )


def header(parent, title, subtitle=""):
    top = tk.Frame(parent, bg=PRIMARY, height=72)
    top.pack(fill="x")
    top.pack_propagate(False)

    tk.Label(top, text="🛒", font=("Segoe UI Emoji", 28),
             bg=PRIMARY, fg="white").pack(side="left", padx=(25, 8))
    title_box = tk.Frame(top, bg=PRIMARY)
    title_box.pack(side="left", pady=8)
    tk.Label(title_box, text=title, font=("Segoe UI", 20, "bold"),
             bg=PRIMARY, fg="white").pack(anchor="w")
    if subtitle:
        tk.Label(title_box, text=subtitle, font=("Segoe UI", 9),
                 bg=PRIMARY, fg="#D9F5E7").pack(anchor="w")


def center_window(width=480, height=600):
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")


# -------------------- LOGIN --------------------
def show_login():
    global current_user
    current_user = None
    clear_root()
    center_window(500, 650)

    outer = tk.Frame(root, bg=BG)
    outer.pack(fill="both", expand=True)

    tk.Label(outer, text="🛒", font=("Segoe UI Emoji", 52),
             bg=BG, fg=PRIMARY).pack(pady=(35, 0))
    tk.Label(outer, text="GROCERY MART", font=("Segoe UI", 25, "bold"),
             bg=BG, fg=PRIMARY_DARK).pack()
    tk.Label(outer, text="Delivery & Billing System",
             font=("Segoe UI", 11), bg=BG, fg=MUTED).pack(pady=(0, 20))

    box = tk.Frame(outer, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    box.pack(fill="x", padx=55)

    tk.Label(box, text="Sign In", font=("Segoe UI", 18, "bold"),
             bg=CARD, fg=TEXT).pack(pady=(25, 18))

    tk.Label(box, text="Username / Email", font=("Segoe UI", 10, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=35)
    username = tk.Entry(box, font=("Segoe UI", 11), relief="solid", bd=1)
    username.pack(fill="x", padx=35, pady=(5, 15), ipady=5)

    tk.Label(box, text="Password", font=("Segoe UI", 10, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=35)
    password = tk.Entry(box, font=("Segoe UI", 11), show="●", relief="solid", bd=1)
    password.pack(fill="x", padx=35, pady=(5, 5), ipady=5)

    show_var = tk.BooleanVar(value=False)

    def toggle_password():
        password.config(show="" if show_var.get() else "●")

    tk.Checkbutton(box, text="Show password", variable=show_var,
                   command=toggle_password, bg=CARD, fg=MUTED,
                   activebackground=CARD).pack(anchor="w", padx=32)

    def login():
        key = username.get().strip()
        pw = password.get()
        user = users.get(key)

        if user and user["password"] == pw:
            global current_user
            current_user = key
            show_home()
        else:
            messagebox.showerror("Login Failed",
                                 "Invalid username/email or password.")

    make_button(box, "LOGIN", login, width=24).pack(pady=(15, 8))

    def forgot():
        messagebox.showinfo(
            "Forgot Password",
            "For this demo project, create a new account from the Sign Up page.\n"
            "No database or email service is connected."
        )

    tk.Button(box, text="Forgot Password?", command=forgot,
              bg=CARD, fg=PRIMARY, relief="flat", cursor="hand2",
              font=("Segoe UI", 9, "underline")).pack()

    def signup():
        show_signup()

    make_button(box, "CREATE NEW ACCOUNT", signup, bg=PRIMARY_DARK, width=24).pack(
        pady=(8, 25)
    )

    tk.Label(outer, text="Demo login: admin  /  admin123",
             font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(pady=18)

    username.focus()
    root.bind("<Return>", lambda event: login())


# -------------------- SIGN UP --------------------
def show_signup():
    clear_root()
    center_window(560, 720)

    header(root, "Create Account", "Register a customer account")

    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=35, pady=20)

    box = tk.Frame(body, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    box.pack(fill="x")

    fields = {}

    data = [
        ("Full Name", "name"),
        ("Username", "username"),
        ("Email", "email"),
        ("Mobile Number", "mobile"),
        ("Password", "password"),
        ("Confirm Password", "confirm"),
    ]

    for text_value, key in data:
        tk.Label(box, text=text_value, font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=35, pady=(12, 3))
        e = tk.Entry(box, font=("Segoe UI", 10), relief="solid", bd=1)
        if key in ("password", "confirm"):
            e.config(show="●")
        e.pack(fill="x", padx=35, ipady=5)
        fields[key] = e

    def create_account():
        name = fields["name"].get().strip()
        username = fields["username"].get().strip()
        email = fields["email"].get().strip()
        mobile = fields["mobile"].get().strip()
        pw = fields["password"].get()
        confirm = fields["confirm"].get()

        if not all([name, username, email, mobile, pw, confirm]):
            messagebox.showwarning("Missing Details", "Please fill all fields.")
            return

        if username in users:
            messagebox.showerror("Account Exists", "Username already exists.")
            return

        if pw != confirm:
            messagebox.showerror("Password Error", "Passwords do not match.")
            return

        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror("Mobile Error", "Enter a valid 10-digit mobile number.")
            return

        users[username] = {
            "password": pw,
            "name": name,
            "mobile": mobile,
            "email": email,
            "address": ""
        }

        messagebox.showinfo("Success", "Account created successfully!")
        show_login()

    make_button(box, "CREATE ACCOUNT", create_account, width=22).pack(pady=20)
    make_button(body, "← BACK TO LOGIN", show_login,
                bg=PRIMARY_DARK, width=22).pack(pady=5)


# -------------------- HOME --------------------
def show_home():
    global cart
    clear_root()
    root.geometry("1200x780")

    user = users[current_user]

    header(root, "GROCERY MART", f"Welcome, {user['name']}")

    nav = tk.Frame(root, bg=CARD, height=52,
                   highlightbackground=BORDER, highlightthickness=1)
    nav.pack(fill="x")
    nav.pack_propagate(False)

    make_button(nav, "🛒 Shop", show_shop, width=12).pack(side="left", padx=(20, 5), pady=7)
    make_button(nav, "🧺 Cart", show_cart, bg=PRIMARY_DARK, width=12).pack(side="left", padx=5, pady=7)
    make_button(nav, "👤 Profile", show_profile, bg=PRIMARY_DARK, width=12).pack(side="left", padx=5, pady=7)
    make_button(nav, "📦 Last Order", show_last_order, bg=PRIMARY_DARK, width=14).pack(side="left", padx=5, pady=7)
    make_button(nav, "Logout", show_login, bg=DANGER, width=10).pack(side="right", padx=20, pady=7)

    content = tk.Frame(root, bg=BG)
    content.pack(fill="both", expand=True, padx=35, pady=25)

    welcome = tk.Frame(content, bg=PRIMARY, height=145)
    welcome.pack(fill="x", pady=(0, 20))
    welcome.pack_propagate(False)

    tk.Label(welcome, text=f"Hello, {user['name']} 👋",
             font=("Segoe UI", 23, "bold"), bg=PRIMARY, fg="white").pack(
        anchor="w", padx=30, pady=(22, 2)
    )
    tk.Label(welcome,
             text="Fresh groceries delivered to your doorstep.",
             font=("Segoe UI", 11), bg=PRIMARY, fg="#DFF3E8").pack(
        anchor="w", padx=30
    )
    make_button(welcome, "START SHOPPING", show_shop, bg=ACCENT, width=18).pack(
        anchor="w", padx=30, pady=13
    )

    tk.Label(content, text="Quick Options", font=("Segoe UI", 16, "bold"),
             bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 12))

    options = tk.Frame(content, bg=BG)
    options.pack(fill="x")

    quick = [
        ("🛍", "Shop Groceries", show_shop),
        ("🧺", "View Cart", show_cart),
        ("🚚", "Delivery Details", show_delivery),
        ("🧾", "Generate Receipt", show_receipt),
    ]

    for icon, title, command in quick:
        f = tk.Frame(options, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        f.pack(side="left", expand=True, fill="both", padx=6)
        tk.Label(f, text=icon, font=("Segoe UI Emoji", 27),
                 bg=CARD).pack(pady=(15, 5))
        tk.Label(f, text=title, font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=TEXT).pack(pady=(0, 15))
        f.bind("<Button-1>", lambda e, c=command: c())
        for child in f.winfo_children():
            child.bind("<Button-1>", lambda e, c=command: c())


# -------------------- SHOP --------------------
def show_shop():
    clear_root()
    root.geometry("1200x780")

    header(root, "Grocery Shop", "Choose items and add them to your cart")

    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=25, pady=18)

    top = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    top.pack(fill="x", pady=(0, 12))

    tk.Label(top, text="Category:", font=("Segoe UI", 10, "bold"),
             bg=CARD, fg=TEXT).pack(side="left", padx=(18, 8), pady=12)

    category_var = tk.StringVar(value="All")
    category_box = ttk.Combobox(top, textvariable=category_var,
                                values=categories, state="readonly", width=18)
    category_box.pack(side="left", pady=12)

    tk.Label(top, text="Search:", font=("Segoe UI", 10, "bold"),
             bg=CARD, fg=TEXT).pack(side="left", padx=(30, 8))

    search_var = tk.StringVar()
    search = tk.Entry(top, textvariable=search_var, width=28,
                      font=("Segoe UI", 10), relief="solid", bd=1)
    search.pack(side="left", pady=10, ipady=3)

    make_button(top, "VIEW CART", show_cart, bg=PRIMARY_DARK, width=13).pack(
        side="right", padx=15
    )

    table_frame = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    table_frame.pack(fill="both", expand=True)

    columns = ("item", "category", "price", "quantity", "amount")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

    headings = {
        "item": "Item", "category": "Category", "price": "Price",
        "quantity": "Quantity", "amount": "Amount"
    }
    widths = {"item": 280, "category": 150, "price": 110, "quantity": 120, "amount": 130}

    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(col, width=widths[col], anchor="center")
    tree.column("item", anchor="w")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
    scrollbar.pack(side="right", fill="y", pady=8)

    bottom = tk.Frame(main, bg=BG)
    bottom.pack(fill="x", pady=12)

    tk.Label(bottom, text="Quantity:", font=("Segoe UI", 10, "bold"),
             bg=BG, fg=TEXT).pack(side="left")
    qty_var = tk.IntVar(value=1)
    qty_spin = tk.Spinbox(bottom, from_=1, to=99, textvariable=qty_var,
                          width=6, font=("Segoe UI", 10))
    qty_spin.pack(side="left", padx=8)

    def add_selected():
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Select Item", "Please select an item.")
            return
        item = tree.item(selection[0])["values"][0]
        try:
            qty = int(qty_var.get())
            if qty < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Quantity", "Enter a valid quantity.")
            return

        cart[item] = cart.get(item, 0) + qty
        messagebox.showinfo("Added", f"{qty} × {item} added to cart.")

    make_button(bottom, "ADD TO CART", add_selected, width=16).pack(side="left", padx=10)
    make_button(bottom, "OPEN CART", show_cart, bg=PRIMARY_DARK, width=14).pack(side="left")
    make_button(bottom, "BACK HOME", show_home, bg="#64748B", width=14).pack(side="right")

    def refresh(*args):
        tree.delete(*tree.get_children())
        selected_cat = category_var.get()
        query = search_var.get().lower().strip()

        for item, (cat, price) in products.items():
            if selected_cat != "All" and cat != selected_cat:
                continue
            if query and query not in item.lower():
                continue
            tree.insert("", "end",
                        values=(item, cat, f"₹{price:.2f}", 1, f"₹{price:.2f}"))

    category_box.bind("<<ComboboxSelected>>", refresh)
    search_var.trace_add("write", refresh)
    refresh()


# -------------------- CART --------------------
def cart_total():
    return sum(products[item][1] * qty for item, qty in cart.items())


def show_cart():
    clear_root()
    root.geometry("1200x780")

    header(root, "Shopping Cart", "Review your groceries before delivery")

    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=30, pady=20)

    table_box = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    table_box.pack(fill="both", expand=True)

    columns = ("item", "quantity", "price", "amount")
    tree = ttk.Treeview(table_box, columns=columns, show="headings", height=16)
    for col, heading_text, width in [
        ("item", "Item", 430), ("quantity", "Quantity", 150),
        ("price", "Price", 150), ("amount", "Amount", 170)
    ]:
        tree.heading(col, text=heading_text)
        tree.column(col, width=width, anchor="center")
    tree.column("item", anchor="w")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh():
        tree.delete(*tree.get_children())
        for item, qty in cart.items():
            price = products[item][1]
            tree.insert("", "end",
                        values=(item, qty, f"₹{price:.2f}", f"₹{price * qty:.2f}"))
        total_label.config(text=f"Subtotal: ₹{cart_total():.2f}")

    def remove_selected():
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Select Item", "Select an item to remove.")
            return
        item = tree.item(selection[0])["values"][0]
        cart.pop(item, None)
        refresh()

    def clear_cart():
        if cart and messagebox.askyesno("Clear Cart", "Remove all items from cart?"):
            cart.clear()
            refresh()

    controls = tk.Frame(main, bg=BG)
    controls.pack(fill="x", pady=15)

    make_button(controls, "REMOVE ITEM", remove_selected, bg=DANGER, width=15).pack(side="left")
    make_button(controls, "CLEAR CART", clear_cart, bg="#64748B", width=14).pack(side="left", padx=8)
    make_button(controls, "CONTINUE SHOPPING", show_shop, width=18).pack(side="left")

    total_label = tk.Label(controls, text="", font=("Segoe UI", 15, "bold"),
                           bg=BG, fg=PRIMARY_DARK)
    total_label.pack(side="right", padx=15)

    make_button(controls, "CHECKOUT →", show_delivery, bg=ACCENT, width=15).pack(
        side="right", padx=10
    )

    refresh()


# -------------------- DELIVERY --------------------
def show_delivery():
    if not cart:
        messagebox.showwarning("Empty Cart", "Please add items to the cart first.")
        show_shop()
        return

    clear_root()
    root.geometry("1100x780")

    header(root, "Delivery Details", "Choose delivery method, address and time slot")

    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=35, pady=18)

    left = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    left.pack(side="left", fill="both", expand=True, padx=(0, 10))

    right = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    right.pack(side="right", fill="both", expand=True, padx=(10, 0))

    tk.Label(left, text="Delivery Type", font=("Segoe UI", 15, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=25, pady=(22, 10))

    delivery_var = tk.StringVar(value="Home Delivery")
    tk.Radiobutton(left, text="🏠 Home Delivery", variable=delivery_var,
                   value="Home Delivery", bg=CARD, activebackground=CARD,
                   font=("Segoe UI", 10)).pack(anchor="w", padx=25)
    tk.Radiobutton(left, text="🏪 Store Pickup", variable=delivery_var,
                   value="Store Pickup", bg=CARD, activebackground=CARD,
                   font=("Segoe UI", 10)).pack(anchor="w", padx=25)

    address_frame = tk.Frame(left, bg=CARD)
    address_frame.pack(fill="x", padx=25, pady=12)

    fields = {}
    for text_value, key in [
        ("House / Flat No.", "house"),
        ("Street / Area", "street"),
        ("City", "city"),
        ("Pincode", "pincode"),
        ("Landmark", "landmark")
    ]:
        tk.Label(address_frame, text=text_value, font=("Segoe UI", 9, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", pady=(6, 2))
        e = tk.Entry(address_frame, font=("Segoe UI", 10), relief="solid", bd=1)
        e.pack(fill="x", ipady=3)
        fields[key] = e

    saved = users[current_user].get("address", "")
    if saved:
        fields["house"].insert(0, saved)

    def toggle_address(*args):
        state = "normal" if delivery_var.get() == "Home Delivery" else "disabled"
        for e in fields.values():
            e.config(state=state)

    delivery_var.trace_add("write", toggle_address)

    tk.Label(right, text="Delivery Slot", font=("Segoe UI", 15, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=25, pady=(22, 10))

    slot_var = tk.StringVar(value="6 PM - 9 PM")
    for slot in ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"]:
        tk.Radiobutton(right, text=slot, variable=slot_var, value=slot,
                       bg=CARD, activebackground=CARD,
                       font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=3)

    tk.Label(right, text="Contact Number", font=("Segoe UI", 9, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=25, pady=(18, 2))
    contact = tk.Entry(right, font=("Segoe UI", 10), relief="solid", bd=1)
    contact.pack(fill="x", padx=25, ipady=4)
    contact.insert(0, users[current_user]["mobile"])

    tk.Label(right, text="Special Delivery Instructions",
             font=("Segoe UI", 9, "bold"), bg=CARD, fg=TEXT).pack(
        anchor="w", padx=25, pady=(18, 2)
    )
    instructions = tk.Text(right, height=5, font=("Segoe UI", 10),
                            relief="solid", bd=1)
    instructions.pack(fill="x", padx=25)

    bottom = tk.Frame(main, bg=BG)
    bottom.pack(fill="x", pady=15)

    def continue_checkout():
        if delivery_var.get() == "Home Delivery":
            if not all(fields[k].get().strip() for k in fields):
                messagebox.showwarning("Address Required",
                                       "Please fill all delivery address fields.")
                return
            address = ", ".join(fields[k].get().strip() for k in
                                ["house", "street", "city", "pincode"])
            users[current_user]["address"] = address

        mobile = contact.get().strip()
        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror("Mobile Error", "Enter a valid 10-digit mobile number.")
            return

        delivery_data = {
            "type": delivery_var.get(),
            "slot": slot_var.get(),
            "contact": mobile,
            "address": (
                ", ".join(fields[k].get().strip() for k in
                          ["house", "street", "city", "pincode"])
                if delivery_var.get() == "Home Delivery" else "Store Pickup"
            ),
            "landmark": fields["landmark"].get().strip()
            if delivery_var.get() == "Home Delivery" else "",
            "instructions": instructions.get("1.0", "end").strip()
        }

        show_checkout(delivery_data)

    make_button(bottom, "← CART", show_cart, bg="#64748B", width=12).pack(side="left")
    make_button(bottom, "CONTINUE TO PAYMENT →", continue_checkout,
                bg=ACCENT, width=22).pack(side="right")


# -------------------- CHECKOUT / PAYMENT --------------------
def show_checkout(delivery_data):
    clear_root()
    root.geometry("1100x780")

    header(root, "Checkout", "Discount, GST, delivery charge, tip and payment")

    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=30, pady=18)

    left = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    left.pack(side="left", fill="both", expand=True, padx=(0, 10))

    right = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    right.pack(side="right", fill="both", expand=True, padx=(10, 0))

    tk.Label(left, text="Order Summary", font=("Segoe UI", 16, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=22, pady=(20, 10))

    summary = tk.Text(left, height=13, font=("Consolas", 10),
                      bg="#FAFBFC", relief="solid", bd=1)
    summary.pack(fill="both", expand=True, padx=22, pady=(0, 20))

    subtotal = cart_total()
    lines = []
    for item, qty in cart.items():
        price = products[item][1]
        lines.append(f"{item:<25} x{qty:<3} ₹{price * qty:.2f}")
    summary.insert("end", "\n".join(lines))
    summary.config(state="disabled")

    tk.Label(right, text="Bill Details", font=("Segoe UI", 16, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=22, pady=(20, 12))

    tk.Label(right, text="Discount (%)", font=("Segoe UI", 9, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=22)
    discount_var = tk.StringVar(value="0")
    discount_entry = tk.Entry(right, textvariable=discount_var,
                              font=("Segoe UI", 10), relief="solid", bd=1)
    discount_entry.pack(fill="x", padx=22, pady=(3, 12), ipady=3)

    tk.Label(right, text="Tip Delivery Partner", font=("Segoe UI", 10, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=22, pady=(3, 5))

    tip_var = tk.StringVar(value="0")
    tip_frame = tk.Frame(right, bg=CARD)
    tip_frame.pack(fill="x", padx=20)

    for amount in ["0", "10", "20", "30", "50"]:
        tk.Radiobutton(tip_frame, text="No Tip" if amount == "0" else f"₹{amount}",
                       variable=tip_var, value=amount,
                       bg=CARD, activebackground=CARD).pack(side="left", padx=2)

    custom_tip = tk.Entry(right, font=("Segoe UI", 9), width=10,
                          relief="solid", bd=1)
    custom_tip.pack(anchor="w", padx=22, pady=5)
    tk.Label(right, text="Custom tip (optional)", font=("Segoe UI", 8),
             bg=CARD, fg=MUTED).pack(anchor="w", padx=22)

    tk.Label(right, text="Payment Method", font=("Segoe UI", 10, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=22, pady=(12, 3))
    payment_var = tk.StringVar(value="Cash on Delivery")
    payment_box = ttk.Combobox(
        right, textvariable=payment_var,
        values=["Cash on Delivery", "UPI", "Debit / Credit Card", "Wallet"],
        state="readonly"
    )
    payment_box.pack(fill="x", padx=22)

    totals_box = tk.Frame(right, bg=SECONDARY)
    totals_box.pack(fill="x", padx=22, pady=15)

    subtotal_label = tk.Label(totals_box, text="", bg=SECONDARY,
                              fg=TEXT, font=("Segoe UI", 10))
    subtotal_label.pack(anchor="w", padx=12, pady=(10, 2))

    discount_label = tk.Label(totals_box, text="", bg=SECONDARY,
                              fg=TEXT, font=("Segoe UI", 10))
    discount_label.pack(anchor="w", padx=12, pady=2)

    gst_label = tk.Label(totals_box, text="", bg=SECONDARY,
                         fg=TEXT, font=("Segoe UI", 10))
    gst_label.pack(anchor="w", padx=12, pady=2)

    delivery_label = tk.Label(totals_box, text="", bg=SECONDARY,
                              fg=TEXT, font=("Segoe UI", 10))
    delivery_label.pack(anchor="w", padx=12, pady=2)

    tip_label = tk.Label(totals_box, text="", bg=SECONDARY,
                         fg=TEXT, font=("Segoe UI", 10))
    tip_label.pack(anchor="w", padx=12, pady=2)

    total_label = tk.Label(totals_box, text="", bg=SECONDARY,
                           fg=PRIMARY_DARK, font=("Segoe UI", 15, "bold"))
    total_label.pack(anchor="w", padx=12, pady=(5, 12))

    def get_tip():
        custom = custom_tip.get().strip()
        if custom:
            try:
                value = float(custom)
                return max(0, value)
            except ValueError:
                return 0
        try:
            return max(0, float(tip_var.get()))
        except ValueError:
            return 0

    def calculate(event=None):
        try:
            disc_pct = float(discount_var.get())
            disc_pct = max(0, min(100, disc_pct))
        except ValueError:
            disc_pct = 0

        discount = subtotal * disc_pct / 100
        taxable = subtotal - discount
        gst = taxable * 0.05
        delivery_charge = 0 if delivery_data["type"] == "Store Pickup" else 30
        tip = get_tip()
        total = taxable + gst + delivery_charge + tip

        subtotal_label.config(text=f"Subtotal:                 ₹{subtotal:.2f}")
        discount_label.config(text=f"Discount:                -₹{discount:.2f}")
        gst_label.config(text=f"GST (5%):                 ₹{gst:.2f}")
        delivery_label.config(text=f"Delivery Charge:         ₹{delivery_charge:.2f}")
        tip_label.config(text=f"Delivery Partner Tip:    ₹{tip:.2f}")
        total_label.config(text=f"TOTAL:                    ₹{total:.2f}")

        return discount, gst, delivery_charge, tip, total

    discount_entry.bind("<KeyRelease>", calculate)
    custom_tip.bind("<KeyRelease>", calculate)
    tip_var.trace_add("write", lambda *args: calculate())

    calculate()

    bottom = tk.Frame(main, bg=BG)
    bottom.pack(fill="x", pady=5)

    make_button(bottom, "← DELIVERY", lambda: show_delivery_from_data(delivery_data),
                bg="#64748B", width=14).pack(side="left")

    def place_order():
        discount, gst, delivery_charge, tip, total = calculate()

        method = payment_var.get()

        if method == "UPI":
            messagebox.showinfo(
                "UPI Payment",
                "Demo UPI payment screen.\n\n"
                "In a real application, a payment gateway would open here.\n"
                "For this project, the payment is simulated."
            )
        elif method == "Debit / Credit Card":
            messagebox.showinfo(
                "Card Payment",
                "Demo card payment screen.\n\n"
                "No real card details are collected in this project."
            )

        global bill_number, current_order_number, last_order

        current_order_number = f"ORD{random.randint(10000, 99999)}"

        last_order = {
            "bill": bill_number,
            "order": current_order_number,
            "date": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            "customer": users[current_user]["name"],
            "mobile": delivery_data["contact"],
            "items": dict(cart),
            "subtotal": subtotal,
            "discount": discount,
            "gst": gst,
            "delivery": delivery_charge,
            "tip": tip,
            "total": total,
            "payment": method,
            "delivery_type": delivery_data["type"],
            "slot": delivery_data["slot"],
            "address": delivery_data["address"],
            "landmark": delivery_data["landmark"],
            "instructions": delivery_data["instructions"]
        }

        bill_number += 1
        cart.clear()
        show_order_confirmation()

    make_button(bottom, "PLACE ORDER ✓", place_order,
                bg=PRIMARY, width=18).pack(side="right")


def show_delivery_from_data(data):
    # Go back to delivery page. Previous entries can be entered again.
    show_delivery()


# -------------------- ORDER CONFIRMATION --------------------
def show_order_confirmation():
    clear_root()
    root.geometry("850x720")

    header(root, "Order Confirmed", "Your grocery order has been placed successfully")

    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=60, pady=25)

    success = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    success.pack(fill="x")

    tk.Label(success, text="✓", font=("Segoe UI", 48, "bold"),
             bg=CARD, fg=PRIMARY).pack(pady=(25, 0))
    tk.Label(success, text="ORDER CONFIRMED",
             font=("Segoe UI", 22, "bold"), bg=CARD, fg=PRIMARY_DARK).pack()
    tk.Label(success, text=f"Order No: {last_order['order']}",
             font=("Segoe UI", 11), bg=CARD, fg=MUTED).pack(pady=5)

    info = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    info.pack(fill="both", expand=True, pady=15)

    details = [
        ("Customer", last_order["customer"]),
        ("Delivery", last_order["delivery_type"]),
        ("Delivery Slot", last_order["slot"]),
        ("Payment", last_order["payment"]),
        ("Total", f"₹{last_order['total']:.2f}")
    ]

    for name, value in details:
        row = tk.Frame(info, bg=CARD)
        row.pack(fill="x", padx=30, pady=7)
        tk.Label(row, text=name, font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=TEXT, width=20, anchor="w").pack(side="left")
        tk.Label(row, text=value, font=("Segoe UI", 10),
                 bg=CARD, fg=TEXT).pack(side="left")

    buttons = tk.Frame(main, bg=BG)
    buttons.pack(fill="x")

    make_button(buttons, "TRACK ORDER", show_tracking, width=16).pack(side="left", padx=5)
    make_button(buttons, "VIEW RECEIPT", show_receipt, bg=PRIMARY_DARK, width=16).pack(
        side="left", padx=5
    )
    make_button(buttons, "BACK HOME", show_home, bg="#64748B", width=14).pack(
        side="right", padx=5
    )


# -------------------- TRACKING --------------------
def show_tracking():
    clear_root()
    root.geometry("800x700")

    header(root, "Order Tracking", "Track the current status of your order")

    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=70, pady=30)

    if not last_order:
        tk.Label(main, text="No order found.", font=("Segoe UI", 15, "bold"),
                 bg=BG, fg=TEXT).pack(pady=50)
        make_button(main, "BACK HOME", show_home).pack()
        return

    tk.Label(main, text=f"Order {last_order['order']}",
             font=("Segoe UI", 18, "bold"), bg=BG, fg=TEXT).pack(pady=(5, 25))

    statuses = [
        ("✓", "Order Placed", "Your order has been received"),
        ("✓", "Order Confirmed", "The store has confirmed your order"),
        ("✓", "Packing", "Your groceries are being packed"),
        ("→", "Out for Delivery", "Delivery partner will deliver your order"),
        ("○", "Delivered", "Waiting for delivery"),
    ]

    for icon, title, desc in statuses:
        row = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        row.pack(fill="x", pady=5)

        tk.Label(row, text=icon, font=("Segoe UI", 20, "bold"),
                 bg=CARD, fg=PRIMARY if icon != "○" else MUTED,
                 width=4).pack(side="left", padx=10, pady=8)

        text_frame = tk.Frame(row, bg=CARD)
        text_frame.pack(side="left", pady=8)
        tk.Label(text_frame, text=title, font=("Segoe UI", 11, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Label(text_frame, text=desc, font=("Segoe UI", 9),
                 bg=CARD, fg=MUTED).pack(anchor="w")

    make_button(main, "VIEW RECEIPT", show_receipt, width=17).pack(pady=20)


# -------------------- RECEIPT --------------------
def show_receipt():
    clear_root()
    root.geometry("900x780")

    header(root, "Final Receipt", "Printable-style grocery order receipt")

    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=45, pady=18)

    receipt_box = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    receipt_box.pack(fill="both", expand=True)

    text = tk.Text(receipt_box, font=("Consolas", 10), bg="#FCFCFC",
                   fg=TEXT, relief="flat", padx=25, pady=20)
    text.pack(fill="both", expand=True)

    if not last_order:
        text.insert("end", "\n\nNo receipt available yet.\n")
    else:
        o = last_order
        lines = []
        lines.append("=" * 68)
        lines.append("                    GROCERY MART")
        lines.append("              DELIVERY & BILLING SYSTEM")
        lines.append("=" * 68)
        lines.append(f"Bill No       : {o['bill']}")
        lines.append(f"Order No      : {o['order']}")
        lines.append(f"Date          : {o['date']}")
        lines.append(f"Customer      : {o['customer']}")
        lines.append(f"Mobile        : {o['mobile']}")
        lines.append("-" * 68)
        lines.append(f"{'ITEM':<34}{'QTY':>8}{'PRICE':>12}{'AMOUNT':>14}")
        lines.append("-" * 68)

        for item, qty in o["items"].items():
            price = products[item][1]
            amount = price * qty
            lines.append(f"{item[:32]:<34}{qty:>8}{price:>12.2f}{amount:>14.2f}")

        lines.append("-" * 68)
        lines.append(f"{'Subtotal':<52}₹{o['subtotal']:>10.2f}")
        lines.append(f"{'Discount':<52}-₹{o['discount']:>9.2f}")
        lines.append(f"{'GST (5%)':<52}₹{o['gst']:>10.2f}")
        lines.append(f"{'Delivery Charge':<52}₹{o['delivery']:>10.2f}")
        lines.append(f"{'Delivery Partner Tip':<52}₹{o['tip']:>10.2f}")
        lines.append("=" * 68)
        lines.append(f"{'TOTAL':<52}₹{o['total']:>10.2f}")
        lines.append("=" * 68)
        lines.append(f"Payment Method : {o['payment']}")
        lines.append(f"Delivery Type  : {o['delivery_type']}")
        lines.append(f"Delivery Slot  : {o['slot']}")

        if o["delivery_type"] == "Home Delivery":
            lines.append(f"Address        : {o['address']}")
            if o["landmark"]:
                lines.append(f"Landmark       : {o['landmark']}")
        if o["instructions"]:
            lines.append(f"Instructions   : {o['instructions']}")

        lines.append("=" * 68)
        lines.append("             THANK YOU FOR SHOPPING WITH US!")
        lines.append("                  HAVE A NICE DAY 😊")
        lines.append("=" * 68)

        text.insert("end", "\n".join(lines))

    text.config(state="disabled")

    buttons = tk.Frame(main, bg=BG)
    buttons.pack(fill="x", pady=12)

    def save_receipt():
        if not last_order:
            messagebox.showwarning("Receipt", "No receipt available.")
            return

        try:
            filename = f"receipt_{last_order['order']}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text.get("1.0", "end"))
            messagebox.showinfo("Saved", f"Receipt saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    make_button(buttons, "SAVE RECEIPT", save_receipt, width=15).pack(side="left")
    make_button(buttons, "TRACK ORDER", show_tracking,
                bg=PRIMARY_DARK, width=15).pack(side="left", padx=8)
    make_button(buttons, "HOME", show_home, bg="#64748B", width=12).pack(side="right")


# -------------------- PROFILE --------------------
def show_profile():
    clear_root()
    root.geometry("700x700")

    user = users[current_user]

    header(root, "My Profile", "View and update your customer information")

    main = tk.Frame(root, bg=BG)
    main.pack(fill="both", expand=True, padx=60, pady=25)

    box = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    box.pack(fill="x")

    fields = {}

    for title, key in [
        ("Full Name", "name"),
        ("Mobile Number", "mobile"),
        ("Email", "email"),
    ]:
        tk.Label(box, text=title, font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", padx=35, pady=(18, 4))
        e = tk.Entry(box, font=("Segoe UI", 10), relief="solid", bd=1)
        e.pack(fill="x", padx=35, ipady=5)
        e.insert(0, user[key])
        fields[key] = e

    tk.Label(box, text="Saved Address", font=("Segoe UI", 10, "bold"),
             bg=CARD, fg=TEXT).pack(anchor="w", padx=35, pady=(18, 4))
    address = tk.Text(box, height=4, font=("Segoe UI", 10),
                      relief="solid", bd=1)
    address.pack(fill="x", padx=35)
    address.insert("1.0", user.get("address", ""))

    def save_profile():
        mobile = fields["mobile"].get().strip()
        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror("Mobile Error", "Enter a valid 10-digit mobile number.")
            return

        user["name"] = fields["name"].get().strip()
        user["mobile"] = mobile
        user["email"] = fields["email"].get().strip()
        user["address"] = address.get("1.0", "end").strip()

        messagebox.showinfo("Saved", "Profile updated successfully.")

    make_button(box, "SAVE CHANGES", save_profile, width=18).pack(pady=20)

    buttons = tk.Frame(main, bg=BG)
    buttons.pack(fill="x", pady=15)
    make_button(buttons, "← HOME", show_home, bg="#64748B", width=12).pack(side="left")
    make_button(buttons, "LOGOUT", show_login, bg=DANGER, width=12).pack(side="right")


# -------------------- LAST ORDER --------------------
def show_last_order():
    if not last_order:
        messagebox.showinfo("Last Order", "You have not placed an order yet.")
        return
    show_tracking()


# -------------------- START --------------------
show_login()
root.mainloop()
