#!/usr/bin/env python

import os
import shutil
import pytest
from .context import parsing
from parsing import simple_cleaning, parse_doc, parse_docx


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
DOC_DIR = os.path.join(TEST_DIR, "documents")
TMP_DIR = os.path.join(TEST_DIR, "tmp")
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)


def archive_test_file(abspath: str) -> str:
    '''copy file into test dir'''
    filename = abspath.split("/")[-1]
    print(filename, abspath)
    tmp_abspath = os.path.join(TEST_DIR, "tmp", filename)
    shutil.copy(abspath, tmp_abspath)
    return tmp_abspath


def restore_test_file(abspath: str) -> str:
    '''restore file from test dir'''
    filename = abspath.split("/")[-1]
    tmp_abspath = os.path.join(TEST_DIR, "tmp", filename)
    shutil.move(tmp_abspath, abspath)
    return abspath


class TestFileParsing:
    @pytest.mark.parametrize("input", ["document.rtf", "document.md", "document.xlsx"]) 
    def test_wrong_extension(self, input):
        """testing accepted extensions"""
        with pytest.raises(ValueError) as e:
            abspath = os.path.join(DOC_DIR, input)
            parse_doc(abspath)
            assert (
                e
                == "Extension incorrecte: les fichiers acceptés terminent par *.odt, *.docx, *.doc,  *.pdf"
            )
            
    @pytest.mark.parametrize("input", ["document.doc", "document.docx", "document.pdf"])
    def test_wrong_file_path(self, input):
        """testing FileNotFound Error"""
        file_path = os.path.join(DOC_DIR, input)
        with pytest.raises(FileNotFoundError) as e:
            parse_doc(file_path)
            assert e == "", e
    
    @pytest.mark.parametrize("file_name", ["testnew.pdf", "newtest.pdf", "HDR.pdf"])
    def test_pdf(self, file_name):
        abspath = os.path.join(DOC_DIR, file_name)
        archive_test_file(abspath)
        full_text = parse_doc(abspath)
        # and restore it
        restore_test_file(abspath)
        doc_name, doc_ext = abspath.split("/")[-1].split(".")
        assert doc_ext == "pdf"
        assert len(full_text) > 0, len(full_text)
        assert isinstance(full_text, str), type(full_text)
        assert any("article" in _x for _x in full_text.split(" ")) is True, full_text[:2000]
        assert any("Code" in _x for _x in full_text.split(" ")) is True, full_text[:2000]
    
    @pytest.mark.parametrize("file_path",["HDR.odt","newtest.odt", "testnew.odt"])
    def test_odt(self, file_path):    
        abspath = os.path.join(DOC_DIR, file_path)
        archive_test_file(abspath)
        full_text = parse_doc(abspath)
        # and restore it
        restore_test_file(abspath)
        doc_name, doc_ext = abspath.split("/")[-1].split(".")
        assert doc_ext == "odt", (doc_ext, abspath)
        assert len(full_text) > 0, full_text
        assert any("article" in _x for _x in full_text.split(" ")) is True, full_text[:2000]
        assert any("Code" in _x for _x in full_text.split(" ")) is True, full_text[:2000]

    @pytest.mark.parametrize("file_path",["newtest.docx", "testnew.docx"])
    def test_docx(self, file_path):
        abspath = os.path.join(DOC_DIR, file_path)
        archive_test_file(abspath)
        full_text = parse_doc(abspath)
        restore_test_file(abspath)
        doc_name, doc_ext = abspath.split("/")[-1].split(".")
        assert doc_ext == "docx" or doc_ext=="doc", (doc_ext, abspath)
        assert len(full_text) > 0, full_text
        assert any("article" in _x for _x in full_text.split(" ")) is True, full_text[:2000]
        assert any("Code" in _x for _x in full_text.split(" ")) is True, full_text[:2000]
    
    @pytest.mark.parametrize("input", ["HDR.docx", "HDR.doc"])
    def test_wrong_docx(self, input):
        """testing FileNotFound Error"""
        file_path = os.path.join(DOC_DIR, input)
        archive_test_file(abspath)
        with pytest.raises(Exception) as e:
            parse_doc(file_path)
            restore_test_file(file_path)
            assert e == "Le format du document est incorrect: impossible de lire le contenu", e
    
    @pytest.mark.parametrize("filename",["newtest.docx", "testnew.docx"])
    def test_simple_cleaning(self, filename):
        abspath = os.path.join(DOC_DIR, filename)
        archive_test_file(abspath)
        full_text = parse_docx(abspath)
        restore_test_file(abspath)
        words = []
        for n in full_text:
            words.extend(n.split(" "))
        assert isinstance(full_text, list)
        clean_str = simple_cleaning(full_text)
        assert isinstance(clean_str, str)
        clean_words = clean_str.split(" ")
        assert len(clean_words) < len(words), [n for n in zip(words, clean_words)] 