import logging
import subprocess
from pathlib import Path


def parse_cbuild(file_path: str) -> dict:
    """Parsuje plik .cbuild i zwraca słownik konfiguracji."""
    config = {}
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku konfiguracji: {file_path}")

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                # Poprawka: dodano nawiasy () do strip()
                config[key.strip()] = value.strip().split()
    return config


def build_project(config: dict, logger: logging.Logger) -> bool:
    """Buduje projekt C na podstawie konfiguracji."""
    sources = config.get("src", [])
    out_list = config.get("out", ["app"])
    output = out_list[0] if out_list else "app"

    object_files = []

    for src in sources:
        # Sprawdzenie czy plik źródłowy istnieje
        if not Path(src).exists():
            logger.error(f"Plik źródłowy nie istnieje: [bold red]{src}[/bold red]")
            return False

        obj = src.replace(".c", ".o")
        logger.info(
            f"Kompilowanie: [bold cyan]{src}[/bold cyan] -> [bold green]{obj}[/bold green]"
        )

        res = subprocess.run(
            ["gcc", "-c", src, "-o", obj], capture_output=True, text=True
        )

        if res.returncode != 0:
            logger.error(f"Błąd kompilacji pliku [bold red]{src}[/bold red]")
            logger.debug(res.stderr)
            return False

        object_files.append(obj)

    logger.info(
        f"Linkowanie: [bold yellow]{' '.join(object_files)}[/bold yellow] -> [bold magenta]{output}[/bold magenta]"
    )

    res = subprocess.run(
        ["gcc"] + object_files + ["-o", output], capture_output=True, text=True
    )

    if res.returncode == 0:
        logger.info("[bold green]Projekt zbudowany pomyślnie![/bold green]")
        return True
    else:
        logger.error(f"Błąd linkowania: {res.stderr}")
        return False
