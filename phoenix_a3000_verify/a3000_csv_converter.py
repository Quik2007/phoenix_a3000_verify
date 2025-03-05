import csv
from warnings import warn
from .utils import get_decimal, FormatChange, Aufträge, UserError
from charset_normalizer import from_bytes

def detect_and_decode(data: bytes) -> str:
    try:
        result = from_bytes(data).best()
        result = str(result) if result else data.decode("utf-8", errors="replace")
    except Exception as e:
        raise UserError("Keine lesbare CSV-Datei")
    return result


class CSVFormatChange(FormatChange):
    def __init__(self, msg: str):
        super().__init__(msg)


def convert_csv(file: bytes) -> Aufträge:
    if isinstance(file, bytes):
        file = detect_and_decode(file).splitlines()
    elif not isinstance(file, list):
        raise ValueError
    csv_reader = csv.reader(file, delimiter=";")

    aufträge: Aufträge = {}

    for row in csv_reader:
        if csv_reader.line_num == 1:
            if len(row) != 13:
                warn("Zahl der Reihen in der CSV-Datei geändert", CSVFormatChange)
            assert row[0] == "LfdNr"
            assert row[1] == "Lieferant"
            # the header of row[2] is converted to an empty string using Windows-1252, but to an unknown char (�) in utf-8
            assert row[3] == "#"
            assert row[4] == "Sendedatum"
            # row[5] should be "letzte Änderung". However, in UTF-8 it's "�" and in Windows-1252 "letzte ánderung"
            assert row[5].lower().startswith("letzte ") and row[5].endswith("nderung")
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
