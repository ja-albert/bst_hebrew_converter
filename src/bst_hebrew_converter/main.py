from pathlib import Path

import typer

from .bst_unicode_translator import create_bst_unicode_mapping
from .grabstein_io import read_grabstein_csv, write_grabstein_csvs
from .utils import translate_grabstein


app = typer.Typer()

grabsteine_file_option = typer.Argument(
    None, help="CSV-Datei mit Grabstein-Eingabe", metavar="GRABSTEINE_DATEI"
)
output_directory_option = typer.Option(
    Path("output"), "--output-directory", "-o", help="Ordner für die Ausgabedateien"
)


@app.command()
def main(
    grabsteine_file: Path = grabsteine_file_option,
    output_directory: Path = output_directory_option,
) -> None:
    # Erstelle ggfs. Ausgabeordner
    output_directory.mkdir(exist_ok=True, parents=True)

    # Erstelle Abbildung BstHebrew <-> Unicode
    bst_unicode_mappings = create_bst_unicode_mapping()

    # Lese Daten ein
    grabsteine = read_grabstein_csv(grabsteine_file)

    # Übersetze Texte
    grabsteine = [translate_grabstein(bst_unicode_mappings, _) for _ in grabsteine]

    # Schreibe Ergebnis Dateien
    write_grabstein_csvs(output_directory, grabsteine)
