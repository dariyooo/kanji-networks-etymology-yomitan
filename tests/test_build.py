from types import SimpleNamespace

from kanjinetworks import KanjiNetworksParser, get_text

from kanji_networks_etymology.build import INDEX_FIELDS, TMP_DIR, build_kanji_bank


def test_index_has_required_fields():
    for field in ("sourceLanguage", "targetLanguage", "author", "url", "description", "attribution"):
        assert field in INDEX_FIELDS


def test_strips_pdf_whitespace_from_both_ends():
    expected = "As per 式# (stand straight).\nInternal spacing  stays."
    definition = "\x0c \t\r\n" + expected + " \n\r\t\x0c"
    kanji = SimpleNamespace(kanji="試", definition=definition)  # attributes like the parser's Kanji objects

    for obj in (kanji, {"kanji": "試", "definition": definition}):
        assert build_kanji_bank([obj]) == [["試", "", "", "etymology", [expected], {}]]


def test_shi_definition_from_source_has_no_surrounding_whitespace():
    TMP_DIR.mkdir(exist_ok=True)
    bank = build_kanji_bank(KanjiNetworksParser().parse(get_text(text_cache_path=str(TMP_DIR / "kanjinetworks.txt"))))
    definitions = [entry[4][0] for entry in bank if entry[0] == "試"]
    assert definitions, "試 must be present in the exported bank"
    for definition in definitions:
        assert definition
        assert not definition[0].isspace()
        assert not definition[-1].isspace()
