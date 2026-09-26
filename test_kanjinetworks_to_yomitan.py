import unittest

from kanjinetworks import Kanji, KanjiNetworksParser, get_text

from kanjinetworks_to_yomitan import build_kanji_bank


class BuildKanjiBankTests(unittest.TestCase):
    def test_strips_pdf_whitespace_from_both_ends(self):
        expected = "As per 式# (stand straight).\nInternal spacing  stays."
        definition = "\x0c \t\r\n" + expected + " \n\r\t\x0c"
        kanji = Kanji()
        kanji.kanji = "試"
        kanji.definition = definition

        for obj in (kanji, {"kanji": "試", "definition": definition}):
            with self.subTest(input_type=type(obj).__name__):
                bank = build_kanji_bank([obj])
                self.assertEqual(bank, [["試", "", "", "etymology", [expected], {}]])
                self.assertFalse(bank[0][4][0].startswith("\x0c"))

    def test_shi_definition_from_source_has_no_surrounding_whitespace(self):
        bank = build_kanji_bank(KanjiNetworksParser().parse(get_text()))
        definitions = [entry[4][0] for entry in bank if entry[0] == "試"]
        self.assertTrue(definitions, "試 must be present in the exported bank")
        for definition in definitions:
            self.assertTrue(definition)
            self.assertFalse(definition.startswith("\x0c"))
            self.assertFalse(definition[0].isspace())
            self.assertFalse(definition[-1].isspace())


if __name__ == "__main__":
    unittest.main()
