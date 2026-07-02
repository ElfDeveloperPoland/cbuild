import argparse
import sys
from pathlib import Path

import modules.parsing
import modules.utils


def main():
    # 1. Konfiguracja loggera (zanim cokolwiek się zacznie)
    log = modules.utils.setup_logger()

    # 2. Tworzenie parsera argumentów
    parser = argparse.ArgumentParser(
        description="CBUILD: Twój własny system budowania projektów w C."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser dla 'build'
    build_parser = subparsers.add_parser("build", help="Buduje projekt C")
    build_parser.add_argument("path", type=str, help="Ścieżka do pliku .cbuild")

    # Subparser dla 'clean'
    clean_parser = subparsers.add_parser("clean", help="Czyści pliki obiektowe")
    clean_parser.add_argument("path", type=str, help="Ścieżka do folderu z projektem")

    args = parser.parse_args()

    # 3. Logika obsługi komend
    if args.command == "build":
        config_path = Path(args.path)
        if not config_path.exists():
            log.error(f"Nie znaleziono pliku: [bold red]{config_path}[/bold red]")
            sys.exit(1)

        try:
            config = modules.parsing.parse_cbuild(file_path=config_path)
            modules.parsing.build_project(config, log)
        except Exception as e:
            log.error(f"Wystąpił błąd podczas budowania: [bold red]{e}[/bold red]")
            sys.exit(1)

    elif args.command == "clean":
        target_dir = Path(args.path)
        log.info(f"Czyszczenie folderu: [bold yellow]{target_dir}[/bold yellow]")

        # Prosta implementacja czyszczenia
        deleted_count = 0
        for ext in ["*.o", "*.a"]:
            for f in target_dir.glob(ext):
                f.unlink()
                deleted_count += 1

        log.info(f"Usunięto [bold cyan]{deleted_count}[/bold cyan] plików.")


if __name__ == "__main__":
    main()
