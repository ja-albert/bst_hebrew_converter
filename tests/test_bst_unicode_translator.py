from bst_hebrew_converter.bst_unicode_translator import (
    create_bst_unicode_mapping,
    translate_bst_to_unicode,
    RIGHT_TO_LEFT_EMBEDDING,
    POP_DIRECTIONAL_FORMATTING,
)
import pytest


@pytest.mark.parametrize("test, expected", [("1", "1"), ("a", "א"), ("=", "\u0591")])
def test_mapping_creation(test: str, expected: str) -> None:
    mapping = create_bst_unicode_mapping()

    # some basic mappings that should always be true
    assert mapping[test].unicode == expected


@pytest.mark.parametrize(
    "test, expected",
    [
        ("hp", "פה"),
        ("... ... rb", "בר ... ..."),
        ("hbcm iytmf rva", "אשׁר שׂמתי מצבה"),
        ("hryic<yil d[vw ah", "הא ושׁעד ליצירה"),
    ],
)
def test_basic_translation(test: str, expected: str) -> None:
    mapping = create_bst_unicode_mapping()
    expected = RIGHT_TO_LEFT_EMBEDDING + expected + POP_DIRECTIONAL_FORMATTING

    assert translate_bst_to_unicode(mapping, test) == expected
