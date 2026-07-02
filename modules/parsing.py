import subprocess
from pathlib import Path

import tomllib
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

console = Console()


def load_config(file_path):
    path = Path(file_path)
    if not path.exists():
        console.print(f"[bold red]Błąd:[/bold red] Plik {file_path} nie istnieje.")
        return None
    with open(path, "rb") as f:
        return tomllib.load(f)


def build_project(path):
    config = load_config(path)
    if not config:
        return

    project_name = config["project"]["name"]
    cflags = config["build"]["cflags"]  # Zakładam, że to lista w TOML
    compiler = config["build"]["compiler"]
    files = config["build"]["files"]

    console.print(
        Panel(
            f"[bold blue]Budowanie projektu:[/bold blue] {project_name}", expand=False
        )
    )

    with Progress() as progress:
        task = progress.add_task("[green]Kompilacja...", total=len(files))

        objs = []
        for i in files:
            obj = i.replace(".c", ".o")
            objs.append(obj)

            # Rich: pasek postępu aktualizuje się w pętli
            progress.update(task, description=f"Kompilowanie [yellow]{i}[/yellow]...")

            # *cflags rozpakowuje listę do argumentów
            cmd = [compiler, "-c", i, "-o", obj] + cflags

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                console.print(f"[bold red]Błąd w pliku {i}![/bold red]")
                console.print(result.stderr)
                return
            progress.advance(task)

    console.print("[bold cyan]Linkowanie...[/bold cyan]")
    link_cmd = ["gcc"] + objs + ["-o", "moj_program"]
    subprocess.run(link_cmd)

    console.print("[bold green]✔ Budowanie zakończone sukcesem![/bold green]")
