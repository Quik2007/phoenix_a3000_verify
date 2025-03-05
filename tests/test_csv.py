import phoenix_a3000_verify

def test_empty():
    with open("tests/csv/empty.csv", "rb") as f:
        data = f.read()

        text = data.decode("windows-1252")
        aufträge = phoenix_a3000_verify.convert_csv(data)
        assert aufträge == {}