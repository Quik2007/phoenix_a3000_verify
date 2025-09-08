from .a3000_csv_converter import convert_csv
from .phoenix_pdf_converter import convert_pdf
from .utils import Aufträge
from decimal import Decimal


def verify(
    phoenix_rechnung_pdfs: list[bytes], a3000_lieferungen_csvs: list[bytes]
) -> tuple[Aufträge, dict[str, tuple[Decimal, Decimal]]]:
    lieferungen_aufträge = {
        k: v
        for csv_bytes in a3000_lieferungen_csvs
        for k, v in convert_csv(csv_bytes).items()
    }
    rechnungen_aufträge = {
        k: v
        for pdf_bytes in phoenix_rechnung_pdfs
        for k, v in convert_pdf(pdf_bytes).items()
    }
    unbekannte_aufträge: Aufträge = {}
    aufträge_mit_preisunterschieden: dict[str, tuple[Decimal, Decimal]] = {}

    for auftrag, preis in rechnungen_aufträge.items():
        if auftrag not in lieferungen_aufträge:
            unbekannte_aufträge[auftrag] = rechnungen_aufträge[auftrag]
        elif preis != lieferungen_aufträge[auftrag]:
            aufträge_mit_preisunterschieden[auftrag] = (
                preis,
                lieferungen_aufträge[auftrag],
            )

    return unbekannte_aufträge, aufträge_mit_preisunterschieden
