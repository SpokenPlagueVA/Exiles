
import json
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

APP_NAME = "ExileGames"
DATA_FILE = Path.home() / "exilegames_squads.json"

BG = "#090b14"
PANEL = "#121626"
PANEL_LIGHT = "#1a2034"
NEON = "#00f5d4"
PURPLE = "#a855f7"
WHITE = "#f2f5ff"
MUTED = "#929bb5"


def load_squads():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return [
        {
            "game": "Fortnite",
            "platform": "PC",
            "style": "Casual",
            "players": "2",
            "host": "ExileBot",
        },
        {
            "game": "Minecraft",
            "platform": "PlayStation",
            "style": "Chill",
            "players": "3",
            "host": "ExileBot",
        },
        {
            "game": "Rocket League",
            "platform": "Xbox",
            "style": "Competitive",
            "players": "2",
            "host": "ExileBot",
        },
    ]


class ExileGames:
    def __init__(self, root):
        self.root = root
        self.root.title("ExileGames | Gaming Community")
        self.root.geometry("1050x700")
        self.root.minsize(800, 580)
        self.root.configure(bg=BG)

        self.squads = load_squads()
        self.platform_filter = tk.StringVar(value="All")
        self.page = "Home"

        self.build_layout()
        self.show_page("Home")

    def save_squads(self):
        try:
            DATA_FILE.write_text(
                json.dumps(self.squads, indent=2),
                encoding="utf-8",
            )
        except OSError as error:
            messagebox.showerror("Save error", str(error))

    def button(self, parent, text, command, color=NEON):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=BG,
            activebackground=WHITE,
            activeforeground=BG,
            relief="flat",
            bd=0,
            padx=15,
            pady=10,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )

    def build_layout(self):
        sidebar = tk.Frame(self.root, bg="#0d1020", width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="EXILE",
            bg="#0d1020",
            fg=NEON,
            font=("Segoe UI", 25, "bold"),
        ).pack(anchor="w", padx=22, pady=(28, 0))

        tk.Label(
            sidebar,
            text="G A M E S",
            bg="#0d1020",
            fg=PURPLE,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=25, pady=(0, 35))

        for name in ("Home", "Find Squads", "Create Squad", "About"):
            tk.Button(
                sidebar,
                text=f"   {name}",
                command=lambda n=name: self.show_page(n),
                anchor="w",
                bg="#0d1020",
                fg=WHITE,
                activebackground=PANEL_LIGHT,
                activeforeground=NEON,
                relief="flat",
                bd=0,
                padx=18,
                pady=14,
                font=("Segoe UI", 11),
                cursor="hand2",
            ).pack(fill="x", padx=8, pady=2)

        tk.Label(
            sidebar,
            text="BUILD 0.1.0\nMADE FOR GAMERS",
            bg="#0d1020",
            fg=MUTED,
            justify="left",
            font=("Segoe UI", 8),
        ).pack(side="bottom", anchor="w", padx=22, pady=24)

        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle):
        tk.Label(
            self.content,
            text=title,
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 25, "bold"),
        ).pack(anchor="w", padx=30, pady=(28, 4))

        tk.Label(
            self.content,
            text=subtitle,
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=32, pady=(0, 20))

    def show_page(self, page):
        self.page = page
        self.clear_content()

        if page == "Create Squad":
            self.show_create_form()
            return

        if page == "About":
            self.heading("About ExileGames", "Built by gamers, for gamers.")
            tk.Label(
                self.content,
                text=(
                    "Our mission is to bring PC and console players together.\n\n"
                    "This is the first local prototype.\n"
                    "Online accounts and live matchmaking are future features."
                ),
                bg=BG,
                fg=WHITE,
                justify="left",
                font=("Segoe UI", 12),
            ).pack(anchor="w", padx=32, pady=15)
            return

        if page == "Home":
            self.heading(
                "YOUR GAME. YOUR SQUAD.",
                "Welcome to ExileGames — find your next team.",
            )

            hero = tk.Frame(self.content, bg=PANEL, padx=24, pady=22)
            hero.pack(fill="x", padx=30, pady=(0, 20))

            tk.Label(
                hero,
                text="READY PLAYER ONE?",
                bg=PANEL,
                fg=NEON,
                font=("Segoe UI", 18, "bold"),
            ).pack(anchor="w")

            tk.Label(
                hero,
                text="Find teammates. Build your squad. Play your way.",
                bg=PANEL,
                fg=WHITE,
                font=("Segoe UI", 11),
            ).pack(anchor="w", pady=(8, 16))

            self.button(
                hero, "FIND YOUR SQUAD",
                lambda: self.show_page("Find Squads")
            ).pack(anchor="w")

            tk.Label(
                self.content,
                text=f"COMMUNITY SQUADS  •  {len(self.squads)} LISTED",
                bg=BG,
                fg=PURPLE,
                font=("Segoe UI", 12, "bold"),
            ).pack(anchor="w", padx=32, pady=(8, 12))

            self.render_squads(limit=3)
            return

        self.heading("FIND YOUR SQUAD", "Choose a platform and explore sessions.")

        filters = tk.Frame(self.content, bg=BG)
        filters.pack(fill="x", padx=30, pady=(0, 15))

        options = ("All", "PC", "PlayStation", "Xbox", "Nintendo Switch")
        menu = tk.OptionMenu(
            filters,
            self.platform_filter,
            *options,
            command=lambda _: self.refresh_squads(),
        )
        menu.config(
            bg=PANEL_LIGHT, fg=WHITE, activebackground=PANEL,
            highlightthickness=0, relief="flat"
        )
        menu["menu"].config(bg=PANEL, fg=WHITE)
        menu.pack(side="left")

        self.button(
            filters, "CREATE SQUAD",
            lambda: self.show_page("Create Squad")
        ).pack(side="right")

        self.squad_area = tk.Frame(self.content, bg=BG)
        self.squad_area.pack(fill="both", expand=True, padx=30, pady=5)
        self.refresh_squads()

    def refresh_squads(self):
        if not hasattr(self, "squad_area"):
            return
        for widget in self.squad_area.winfo_children():
            widget.destroy()
        self.render_squads(parent=self.squad_area)

    def render_squads(self, limit=None, parent=None):
        target = parent or self.content
        platform = self.platform_filter.get()

        visible = [
            squad for squad in self.squads
            if platform == "All" or squad["platform"] == platform
        ]
        if limit is not None:
            visible = visible[:limit]

        if not visible:
            tk.Label(
                target,
                text="No squads found. Create the first one!",
                bg=BG, fg=MUTED, font=("Segoe UI", 11),
            ).pack(anchor="w", pady=15)
            return

        for squad in visible:
            card = tk.Frame(
                target, bg=PANEL, padx=18, pady=13,
                highlightbackground="#28314a", highlightthickness=1
            )
            card.pack(fill="x", pady=6)

            top = tk.Frame(card, bg=PANEL)
            top.pack(fill="x")

            tk.Label(
                top, text=squad["game"], bg=PANEL, fg=WHITE,
                font=("Segoe UI", 14, "bold")
            ).pack(side="left")

            tk.Label(
                top, text=squad["platform"], bg=PANEL, fg=NEON,
                font=("Segoe UI", 9, "bold")
            ).pack(side="right")

            tk.Label(
                card,
                text=(
                    f'{squad["style"]}  •  '
                    f'{squad["players"]} open player slot(s)  •  '
                    f'Host: {squad["host"]}'
                ),
                bg=PANEL, fg=MUTED, font=("Segoe UI", 10),
            ).pack(anchor="w", pady=(8, 10))

            self.button(
                card, "JOIN SQUAD",
                lambda s=squad: self.join_squad(s),
                color=PURPLE,
            ).pack(anchor="w")

    def join_squad(self, squad):
        messagebox.showinfo(
            "ExileGames",
            f'You selected the {squad["game"]} squad!\n\n'
            "This prototype records no online membership yet. "
            "Online joining will come in a later version.",
        )

    def show_create_form(self):
        self.heading("CREATE A SQUAD", "Bring your next team together.")

        form = tk.Frame(self.content, bg=PANEL, padx=24, pady=22)
        form.pack(fill="x", padx=30)

        self.game_var = tk.StringVar()
        self.platform_var = tk.StringVar(value="PC")
        self.style_var = tk.StringVar(value="Casual")
        self.players_var = tk.StringVar(value="3")
        self.host_var = tk.StringVar(value="Player")

        def field(label, variable, choices=None):
            tk.Label(
                form, text=label, bg=PANEL, fg=WHITE,
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w", pady=(10, 5))

            if choices:
                widget = tk.OptionMenu(form, variable, *choices)
                widget.config(
                    bg=PANEL_LIGHT, fg=WHITE,
                    activebackground=PANEL, highlightthickness=0,
                    relief="flat", anchor="w",
                )
                widget["menu"].config(bg=PANEL_LIGHT, fg=WHITE)
            else:
                widget = tk.Entry(
                    form, textvariable=variable, bg=PANEL_LIGHT,
                    fg=WHITE, insertbackground=NEON, relief="flat",
                    font=("Segoe UI", 11),
                )
            widget.pack(fill="x", ipady=7)

        field("GAME NAME", self.game_var)
        field("PLATFORM", self.platform_var,
              ["PC", "PlayStation", "Xbox", "Nintendo Switch"])
        field("PLAY STYLE", self.style_var,
              ["Casual", "Competitive", "Chill", "Co-op"])
        field("OPEN PLAYER SLOTS", self.players_var,
              ["1", "2", "3", "4", "5", "6", "8"])
        field("HOST NAME", self.host_var)

        self.button(form, "PUBLISH SQUAD", self.create_squad).pack(
            anchor="w", pady=(22, 0)
        )

    def create_squad(self):
        game = self.game_var.get().strip()
        host = self.host_var.get().strip()

        if not game or not host:
            messagebox.showwarning(
                "Missing information", "Enter a game name and host name."
            )
            return

        self.squads.insert(0, {
            "game": game,
            "platform": self.platform_var.get(),
            "style": self.style_var.get(),
            "players": self.players_var.get(),
            "host": host,
        })
        self.save_squads()
        self.show_page("Find Squads")
        messagebox.showinfo(
            "Squad published",
            "Your squad has been saved on this computer!",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ExileGames(root)
    root.mainloop()
