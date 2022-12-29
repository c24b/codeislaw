#!/usr/bin/env python
# filename: parsing.py

"""
Parsing file module:

Load document with the accepted extensions and transform into list of text

"""

import os
from io import StringIO
import docx
from PyPDF2 import PdfReader
from pdfreader import SimplePDFViewer
from odf import text, teletype
from odf.opendocument import load
from docx.enum.style import WD_STYLE_TYPE


ACCEPTED_EXTENSIONS = ("odt", "pdf", "docx", "doc")

def get_styles(doc):
   styles= {}
   for ast in doc.automaticstyles.childNodes:

    name= ast.getAttribute('name')
    style= {}
    styles[name]= style

    for k in ast.attributes.keys():
        style[k[1]]= ast.attributes[k]
    for n in ast.childNodes:
        for k in n.attributes.keys():
            style[n.qname[1] + "/" + k[1]]= n.attributes[k]
    return styles

def parse_pdf(file_path: str) -> list:
    full_text = []
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            full_text.extend((page.extract_text()).split("\n"))
        return full_text

def parse_odt(file_path: str) -> list:
    full_text = []
    with open(file_path, "rb") as f:
        document = load(f)
        paragraphs = document.getElementsByType(text.P)
        for i in range(len(paragraphs)):
            full_text.append((teletype.extractText(paragraphs[i])))
        return full_text
def parse_docx(file_path:str) -> list:
    full_text = []
    with open(file_path, "rb") as f:
        document = docx.Document(f)
        paragraphs = document.paragraphs   
        for i in range(len(paragraphs)):
            #not usefull can't detect style properly
            if paragraphs[i].style.name == "Normal":
                full_text.append((paragraphs[i].text))
        return full_text

def parse_doc(file_path: str) -> str:
    """
    Parcourir le document pour en extraire le texte
    Arguments
    ----------
    file_path: str
        absolute filepath of the document
    Returns
    ----------
    full_text: array
        a list of sentences.
    Raises
    ----------
    Exception:
        Extension incorrecte. Les types de fichiers supportés sont odt, doc, docx, pdf
    FileNotFoundError:
        File has not been found. File_path must be incorrect
    """

    doc_name, doc_ext = file_path.split("/")[-1].split(".")
    if doc_ext not in ACCEPTED_EXTENSIONS:
        os.remove(file_path)
        raise ValueError(
            "Extension incorrecte: les fichiers acceptés terminent par *.odt, *.docx, *.doc,  *.pdf"
        )
        
    if doc_ext == "pdf":
        full_text = parse_pdf(file_path)    
    
    elif doc_ext == "odt":
        full_text = parse_odt(file_path)
    
    else:
        try:
            full_text = parse_docx(file_path)
        except Exception as e:
            if e == "File is not a zip file":
                try:
                    full_text = parse_odt(file_path)
                except Exception as e:
                    os.remove(file_path)
                    raise Exception("Le format du document est incorrect: impossible de lire le contenu")
            else:
                os.remove(file_path)
                raise Exception("Le format du document est incorrect: impossible de lire son contenu")
    os.remove(file_path)
    return " ".join([n for n in full_text if n not in [" ", "", None] and len(n) > 3])
    