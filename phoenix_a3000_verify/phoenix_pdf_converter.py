from pdfreader import SimplePDFViewer
from rich import print
from .utils import Aufträge, get_decimal


def convert_pdf(file: bytes):
    viewer = SimplePDFViewer(file)

    aufträge: Aufträge = {}

    ende = False
    for canvas in viewer:
        print("Raw strings: ", canvas.strings)
        texts = [x.split() for x in canvas.strings[13:-1]]
        print("Splitted texts: ", texts)
        i = 0
        for auftrag in texts:
            if auftrag[0] == "SUMME":
                ende = True
                break
            i += 1
            index_nummer = 3 if i == 1 else 2

            auftrag_nummer = auftrag[index_nummer]
            assert len(auftrag_nummer) == 6

            preis_str = auftrag[-2]
            decimal = get_decimal(preis_str)

            aufträge[auftrag_nummer] = decimal
        if ende:
            break


if __name__ == "__main__":
    fd = open("rechnung.pdf", "rb")
    aufträge = convert_pdf()

    print(aufträge)
    print(f"Insgesamt {len(aufträge)} Aufträge")
