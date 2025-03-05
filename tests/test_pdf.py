from phoenix_a3000_verify import convert_pdf
from phoenix_a3000_verify.utils import UserError

def test_invalid():
    with open("tests/pdf/invalid.pdf", "rb") as f:
        data = f.read()

    try:
        convert_pdf(data)
        raise ValueError("Should have thrown an UserError when trying to convert invalid PDF")
    except UserError:
        pass