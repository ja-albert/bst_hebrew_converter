from bst_hebrew_converter.grabstein_io import Grabstein, GrabsteinRecord


def test_dataclasses() -> None:
    grabstein = Grabstein("0")
    record = GrabsteinRecord(0, grabstein, "key", ["values"])
    grabstein.records.append(record)

    assert record.grabstein == grabstein
    assert len(grabstein.records) == 1
