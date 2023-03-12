from .bst_unicode_translator import BstUnicodeMapping, translate_bst_to_unicode
from .grabstein_io import Grabstein, GrabsteinRecord


def translate_grabstein(
    bst_unicode_mappings: dict[str, BstUnicodeMapping], grabstein: Grabstein
) -> Grabstein:
    result = Grabstein(grabstein.id)
    for record in grabstein.records:
        values = record.values[:]

        if record.key.startswith("grabstein.inschrift.vorderseite.text"):
            values[0] = translate_bst_to_unicode(bst_unicode_mappings, values[0])
        elif record.key == "grabstein.zitate":
            values[2] = translate_bst_to_unicode(bst_unicode_mappings, values[2])

        new_record = GrabsteinRecord(record.id, result, record.key, values)
        result.records.append(new_record)

    return result
