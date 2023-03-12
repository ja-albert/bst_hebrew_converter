import csv
from dataclasses import dataclass
from importlib import resources
from typing import TextIO

from hebrew import Hebrew

BST_UNICODE_MAPPING_FILES = f"{__package__}.data.bst_unicode"
UNKNOWN_CHAR = "�"
RIGHT_TO_LEFT_EMBEDDING = "\u202B"
POP_DIRECTIONAL_FORMATTING = "\u202C"


@dataclass
class BstUnicodeMapping:
    bst: str
    unicode: str
    diacritic: bool


def create_bst_unicode_mapping() -> dict[str, BstUnicodeMapping]:
    mapping = {}

    files = list(resources.files(BST_UNICODE_MAPPING_FILES).iterdir())
    files = sorted(files, key=lambda t: t.name)

    for file in files:
        if not (file.is_file() and file.name.endswith(".csv")):
            continue

        with file.open(encoding="utf-8", newline="") as f:
            mapping.update(import_mappings(f))

    return mapping


def import_mappings(f: TextIO) -> dict[str, BstUnicodeMapping]:
    mapping = {}

    reader = csv.DictReader(f)
    for row in reader:
        bst = row["ASCII"]
        unicode = row["Unicode"]
        diacritic = row["Diakritisch"] == "WAHR"
        mapping[bst] = BstUnicodeMapping(bst, unicode, diacritic)

    return mapping


def translate_bst_to_unicode(mapping: dict[str, BstUnicodeMapping], text: str) -> str:
    """
    Let bx, by be BST chars
    Let ux, uy be the corresponding Unicode chars
    Let bd, be be BST diacritics
    Let ud, ue be the corresponding Unicode diacritics

    BST: bx, by, bd, be (= bd, be diacritics for by)
    Then Unicode should be: uy, ud, ue, ux
    """

    text = preprocess_text(text)

    char_groups = []
    stack = []
    for char in text:
        # Collect all chars as Unicode on a stack
        stack.append(mapping[char].unicode)

        if not mapping[char].diacritic:
            # If the current char is not diacritic:
            # Store the reversed current stack,
            # as the diacritics on the stack belong to the previous char
            char_groups.append(postprocess_stack(stack))
            stack = []

    # Empty remaining stack
    char_groups.append(postprocess_stack(stack))

    # Reverse all characters, as BST is written LTR instead of RTL
    result = "".join(char_groups[::-1])

    return postprocess_text(result)


def preprocess_text(text: str) -> str:
    # Remove "(!)" and "(?)"
    text = text.replace("(!)", "")
    text = text.replace("(?)", "")

    return text


def postprocess_stack(stack: list[str]) -> str:
    if not stack:
        return ""

    BST_UNICODE_DOT = "\u05B0"  # Unicode character represented by BST "." (decimal dot)
    stack_ends_with_space_or_dot = stack[-1] in (" ", BST_UNICODE_DOT)
    all_other_chars_are_dots = all(_ == BST_UNICODE_DOT for _ in stack[:-1])
    if stack_ends_with_space_or_dot and all_other_chars_are_dots:
        # If stack would have ended with a dot or a space
        # and all other characters are dots,
        # then assume the ASCII dots are meant.
        stack = ["." if _ == BST_UNICODE_DOT else _ for _ in stack]

    return "".join(stack[::-1])


def postprocess_text(text: str) -> str:
    h = Hebrew(text)

    result = str(h.text_only())

    # Explizitly markup direction
    return RIGHT_TO_LEFT_EMBEDDING + result + POP_DIRECTIONAL_FORMATTING
