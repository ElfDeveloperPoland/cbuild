import logging

from rich.logging import RichHandler


def setup_logger(level: str = "INFO") -> logging.Logger:
    """Konfiguruje i zwraca ładny logger z biblioteki rich."""
    FORMAT = "%(message)s"

    logging.basicConfig(
        level=level,
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    # Zwracamy instancję loggera do użycia w aplikacji
    return logging.getLogger("rich")
