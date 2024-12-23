import csv
from warnings import warn
from .utils import get_decimal, FormatChange, Aufträge


class CSVFormatChange(FormatChange):
    def __init__(self, msg: str):
        super().__init__(msg)


def convert_csv(file: bytes) -> Aufträge:
    if isinstance(file, bytes):
        file = file.decode("utf-8").splitlines()
    csv_reader = csv.reader(file, delimiter=";")

    aufträge: Aufträge = {}

    for row in csv_reader:
        if csv_reader.line_num == 1:
            if len(row) != 13:
                warn("Zahl der Reihen in der CSV-Datei geändert", CSVFormatChange)
            assert row[0] == "LfdNr"
            assert row[1] == "Lieferant"
            assert row[2] == "�"
            assert row[3] == "#"
            assert row[4] == "Sendedatum"
            assert row[5] == "letzte �nderung"
            assert row[6] == "R"
            assert row[7] == "Auftragsart"
            assert row[8] == "Status"
            assert row[9] in ["Rechungsnummer", "Rechnungsnummer"]
            if row[9] != "Rechungsnummer":
                warn(
                    "Das Feld für die Rechnungsnummer wurde umbenannt (Rechtschreibfehler korrigiert)",
                    CSVFormatChange,
                )
            assert row[10] == "Bediener"
            assert row[11] == "Nr.-Auftrag"
            assert row[12] == "Datum/Verbuchungsdatum"
            continue

        assert 99999 > int(row[0]) > 0
        assert row[1].startswith(" (") and row[1].endswith(")")
        preis = get_decimal(row[2])
        assert int(row[3]) >= 0
        # TODO check dates
        if row[8] not in ["gesendet", "verbucht", "offen"]:  # TODO
            warn(f"Unbekannter Status: {row[8]}", CSVFormatChange)

        if row[8] != "verbucht":
            continue
        if row[9] == "":
            warn(f"Keine Rechnungsnummer für Zeile {csv_reader.line_num}")
            continue
        rechnung_nummer = row[9]
        aufträge[rechnung_nummer] = preis

    return aufträge


if __name__ == "__main__":
    from rich import print

    fd = open("data.csv", "r")
    print(convert_csv(fd))
