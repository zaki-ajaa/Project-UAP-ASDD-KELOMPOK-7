import tkinter as tk
from tkinter import ttk, messagebox
from backend import linkedlist, bst, stack, queue, bubble_sort

PAL = {
    "bg": "#F9F9FB", "card": "#FFFFFF", "border": "#E5E5E5", "border_act": "#1B4332", "text": "#111111", "sub": "#666666",
    "green": "#1B4332", "green_hover": "#143225", "green_pressed": "#0E2219",
    "blue": "#1E3A8A", "blue_hover": "#172E6F", "blue_pressed": "#10204E",
    "danger": "#7F1D1D", "danger_hover": "#601414", "danger_pressed": "#420D0D",
    "neutral": "#374151", "neutral_hover": "#2B323F", "neutral_pressed": "#1F242E"
}
FONT_FAMILY, FONT_HEADING, FONT_TABLE = "Helvetica Neue", "Times New Roman", "Poppins"

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, width=130, height=36, radius=12, bg_color=PAL["green"]):
        super().__init__(parent, width=width, height=height, bg=parent["bg"] if "bg" in parent.keys() else PAL["card"], highlightthickness=0)
        self.command, self.bg_color, self.width, self.height, self.radius = command, bg_color, width, height, radius
        self.resolve_colors()
        self.draw_perfect_rounded_rect(bg_color)
        self.text_id = self.create_text(width // 2, height // 2, text=text, fill="white", font=(FONT_FAMILY, 10, "bold"))
        self.bind("<ButtonPress-1>", self.on_press); self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", lambda e: self.change_color(self.hover_color)); self.bind("<Leave>", lambda e: self.change_color(self.bg_color))

    def draw_perfect_rounded_rect(self, color):
        r, w, h = self.radius, self.width, self.height
        self.create_oval(0, 0, r*2, r*2, fill=color, outline="", tags="bg_shape")
        self.create_oval(w-r*2, 0, w, r*2, fill=color, outline="", tags="bg_shape")
        self.create_oval(0, h-r*2, r*2, h, fill=color, outline="", tags="bg_shape")
        self.create_oval(w-r*2, h-r*2, w, h, fill=color, outline="", tags="bg_shape")
        self.create_rectangle(r, 0, w-r, h, fill=color, outline="", tags="bg_shape")
        self.create_rectangle(0, r, w, h-r, fill=color, outline="", tags="bg_shape")

    def change_color(self, color): self.itemconfig("bg_shape", fill=color)
    def resolve_colors(self):
        if self.bg_color == PAL["green"]: self.hover_color, self.pressed_color = PAL["green_hover"], PAL["green_pressed"]
        elif self.bg_color == PAL["blue"]: self.hover_color, self.pressed_color = PAL["blue_hover"], PAL["blue_pressed"]
        elif self.bg_color == PAL["danger"]: self.hover_color, self.pressed_color = PAL["danger_hover"], PAL["danger_pressed"]
        else: self.hover_color, self.pressed_color = PAL["neutral_hover"], PAL["neutral_pressed"]

    def on_press(self, event): self.change_color(self.pressed_color); self.move(self.text_id, 0, 1)
    
    def on_release(self, event): 
        self.move(self.text_id, 0, -1)
        self.change_color(self.bg_color)
        if self.command: 
            self.command()

class SmartBookModern:
    def simpan_ke_file(self):
        with open("database.txt", "w") as f:
            curr = self.db_ll.head
            while curr:
                f.write(f"{curr.nama}|{curr.buku}|{curr.rating}\n")
                curr = curr.next

    def load_dari_file(self):
        try:
            with open("database.txt", "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        n, b, r = parts
                        self.db_ll.insert(n, b, int(r))
                        self.db_bst.insert(b, int(r))
        except FileNotFoundError:
            for n, b, r in [("Andi", "Struktur Data C++", 5), ("Budi", "Algoritma Python", 4)]:
                self.db_ll.insert(n, b, r); self.db_bst.insert(b, r)

    def __init__(self, root):
        self.root = root
        self.root.title("SmartBook System Management")
        self.root.geometry("1150x760")
        self.root.configure(bg=PAL["bg"])
        self.current_width = 1150
        self.placeholder_text = "🔍 Masukkan judul buku atau nama pengguna."

        self.db_ll, self.db_bst, self.undo_st, self.log_qu = linkedlist(), bst(), stack(), queue()
        self.current_rating = 0
        self.load_dari_file()

        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TFrame", background=PAL["bg"])
        style.configure("Card.TLabelframe", background=PAL["card"], borderwidth=1, relief="solid", bordercolor=PAL["border"])
        style.configure("Card.TLabelframe.Label", background=PAL["card"], foreground=PAL["text"], font=(FONT_FAMILY, 12, "bold"))
        style.configure("Custom.Treeview", background=PAL["card"], foreground=PAL["text"], rowheight=34, fieldbackground=PAL["card"], font=(FONT_TABLE, 10), borderwidth=0)
        style.configure("Custom.Treeview.Heading", font=(FONT_TABLE, 10, "bold"), foreground=PAL["text"])
        style.map("Custom.Treeview", background=[("selected", "#EEF7EF")], foreground=[("selected", PAL["green"])])
        style.configure("TCombobox", background="#FFFFFF", fieldbackground="#FFFFFF", foreground=PAL["text"], bordercolor=PAL["border"])

        self.scroll_canvas = tk.Canvas(self.root, bg=PAL["bg"], highlightthickness=0)
        self.v_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.v_scrollbar.set)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.main_frame = ttk.Frame(self.scroll_canvas, padding="30")
        self.canvas_window = self.scroll_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.main_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.itemconfig(self.canvas_window, width=e.width))
        self.scroll_canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") if event.delta else None)

        self.root.bind("<Configure>", self.cek_responsif)
        self.build_interface(is_mobile_view=False)

    def cek_responsif(self, event):
        if event.widget == self.root and abs(event.width - self.current_width) > 20:
            self.current_width = event.width
            self.build_interface(is_mobile_view=(event.width < 768))

    def focus_in(self, entry): entry.configure(highlightbackground=PAL["border_act"], highlightthickness=1)
    def focus_out(self, entry): entry.configure(highlightbackground=PAL["border"], highlightthickness=1)
    
    def search_focus_in(self, event):
        if self.en_cari.get() == self.placeholder_text:
            self.en_cari.delete(0, tk.END)
            self.en_cari.configure(fg=PAL["text"], highlightbackground=PAL["border_act"])

    def search_focus_out(self, event):
        if not self.en_cari.get():
            self.en_cari.insert(0, self.placeholder_text)
            self.en_cari.configure(fg=PAL["sub"], highlightbackground=PAL["border"])
        else:
            self.en_cari.configure(highlightbackground=PAL["border"])

    def set_stars(self, val):
        self.current_rating = val
        for i in range(5): self.star_btn[i].configure(fg="#FFD700" if i < val else "#D1D5DB")

    def build_interface(self, is_mobile_view):
        for w in self.main_frame.winfo_children(): w.destroy()

        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, pady=(0, 25))
        tk.Label(header, text="SmartBook Management", font=(FONT_HEADING, 26, "bold"), bg=PAL["bg"], fg=PAL["text"]).pack(side=tk.LEFT)
        RoundedButton(header, "↩ Undo", self.proses_undo, width=100, height=34, radius=12, bg_color=PAL["neutral"]).pack(side=tk.RIGHT, padx=5)

        body = ttk.Frame(self.main_frame)
        body.pack(fill=tk.BOTH, expand=True)
        left = ttk.Frame(body); left.pack(side="top" if is_mobile_view else "left", fill="both", expand=True, padx=5)
        right = ttk.Frame(body); right.pack(side="top" if is_mobile_view else "right", fill="both", expand=True, padx=20)

        #PANEL KIRI (CRUD Input)
        f_crud = ttk.LabelFrame(left, text=" Input Ulasan ", style="Card.TLabelframe", padding=20)
        f_crud.pack(fill=tk.X, pady=(0, 20))

        for lbl_text, var_name in [("NAMA PENGGUNA", "en_nama"), ("JUDUL BUKU", "en_buku")]:
            tk.Label(f_crud, text=lbl_text, font=(FONT_FAMILY, 9, "bold"), bg=PAL["card"], fg=PAL["sub"]).pack(anchor=tk.W)
            # Pointer diatur melalui insertbackground="black"
            entry = tk.Entry(f_crud, font=(FONT_FAMILY, 11), relief="flat", bg="#FFFFFF", fg=PAL["text"], insertbackground="black", highlightthickness=1, highlightbackground=PAL["border"])
            entry.pack(fill=tk.X, ipady=7, pady=(4, 12))
            setattr(self, var_name, entry)
            entry.bind("<FocusIn>", lambda e, en=entry: self.focus_in(en)); entry.bind("<FocusOut>", lambda e, en=entry: self.focus_out(en))

        tk.Label(f_crud, text="RATING", font=(FONT_FAMILY, 9, "bold"), bg=PAL["card"], fg=PAL["sub"]).pack(anchor=tk.W)
        star_frame = tk.Frame(f_crud, bg=PAL["card"]); star_frame.pack(anchor=tk.W, pady=(4, 18))
        self.star_btn = []
        for i in range(1, 6):
            btn = tk.Label(star_frame, text="★", font=(FONT_FAMILY, 22), fg="#D1D5DB", bg=PAL["card"], cursor="hand2")
            btn.pack(side=tk.LEFT, padx=3); btn.bind("<Button-1>", lambda e, val=i: self.set_stars(val)); self.star_btn.append(btn)
        
        btn_box = tk.Frame(f_crud, bg=PAL["card"]); btn_box.pack(fill=tk.X)
        RoundedButton(btn_box, "Add", self.aksi_create, width=100, height=36, radius=12, bg_color=PAL["green"]).pack(side=tk.LEFT, padx=3)
        RoundedButton(btn_box, "Update", self.aksi_update, width=100, height=36, radius=12, bg_color=PAL["blue"]).pack(side=tk.LEFT, padx=3)
        RoundedButton(btn_box, "Delete", self.aksi_delete, width=100, height=36, radius=12, bg_color=PAL["danger"]).pack(side=tk.LEFT, padx=3)

        #PANEL KANAN (Tabel & Pencarian)
        f_table = ttk.LabelFrame(right, text=" Database Ulasan ", style="Card.TLabelframe", padding=15)
        f_table.pack(fill=tk.BOTH, expand=True)

        # Baris Pencarian
        search_bar = tk.Frame(f_table, bg=PAL["card"])
        search_bar.pack(fill=tk.X, pady=(5, 10))
        
        # Pointer diatur melalui insertbackground="black"
        self.en_cari = tk.Entry(search_bar, font=(FONT_FAMILY, 10), relief="flat", bg="#F9F9FB", fg=PAL["sub"], insertbackground="black", highlightthickness=1, highlightbackground=PAL["border"])
        self.en_cari.insert(0, self.placeholder_text)
        self.en_cari.bind("<FocusIn>", self.search_focus_in)
        self.en_cari.bind("<FocusOut>", self.search_focus_out)
        self.en_cari.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 10))
        
        RoundedButton(search_bar, "Cari", self.aksi_cari_bst, width=90, height=32, radius=10, bg_color=PAL["green"]).pack(side=tk.LEFT)

        # Baris Filter
        filter_bar = tk.Frame(f_table, bg=PAL["card"])
        filter_bar.pack(fill=tk.X, pady=(0, 15))
        tk.Label(filter_bar, text="Filter Rating:", font=(FONT_FAMILY, 9, "bold"), bg=PAL["card"], fg=PAL["text"]).pack(side=tk.LEFT, padx=(5, 10))
        self.cb_filter = ttk.Combobox(filter_bar, values=["Semua", "⭐ 5", "⭐ 4", "⭐ 3", "⭐ 2", "⭐ 1"], state="readonly", font=(FONT_FAMILY, 10), width=8)
        self.cb_filter.pack(side=tk.LEFT, padx=5); self.cb_filter.current(0)
        RoundedButton(filter_bar, "Filter", self.aksi_top_rated, width=90, height=30, radius=8, bg_color=PAL["blue"]).pack(side=tk.LEFT, padx=10)

        # Tabel
        self.tree = ttk.Treeview(f_table, columns=("n", "b", "r"), show="headings", style="Custom.Treeview", height=10 if is_mobile_view else 14)
        self.tree.heading("n", text="Pengguna"); self.tree.heading("b", text="Judul Buku"); self.tree.heading("r", text="Rating")
        self.tree.column("n", width=100, anchor=tk.CENTER); self.tree.column("b", width=220); self.tree.column("r", width=80, anchor=tk.CENTER)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        sb = ttk.Scrollbar(f_table, orient=tk.VERTICAL, command=self.tree.yview); self.tree.configure(yscrollcommand=sb.set); sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.lbl_log = tk.Label(right, text="Copyright ©️ 2026 SmartBook. All rights reserved.", font=(FONT_FAMILY, 9, "italic"), bg=PAL["bg"], fg=PAL["sub"]); self.lbl_log.pack(anchor=tk.W, pady=5)
        self.refresh_tabel()
