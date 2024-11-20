from a3000_csv_converter import convert_csv
from phoenix_pdf_converter import convert_pdf
from utils import Aufträge
from decimal import Decimal


def verify(
    phoenix_rechnung_pdf: bytes, a3000_lieferungen_csv: bytes
) -> tuple[Aufträge, dict[str, tuple[Decimal, Decimal]]]:
    lieferungen_aufträge = convert_csv(a3000_lieferungen_csv)
    rechnungen_aufträge = convert_pdf(phoenix_rechnung_pdf)

    unbekannte_aufträge: Aufträge = {}
    aufträge_mit_preisunterschieden: dict[str, tuple[Decimal, Decimal]] = {}

    for auftrag, preis in rechnungen_aufträge.items():
        if auftrag not in lieferungen_aufträge:
            unbekannte_aufträge[auftrag] = rechnungen_aufträge[auftrag]
        elif preis != lieferungen_aufträge[auftrag]:
            aufträge_mit_preisunterschieden = (preis, lieferungen_aufträge[preis])

    return lieferungen_aufträge, aufträge_mit_preisunterschieden
