from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

def extract_form_fields(pdf_path):
    with open(pdf_path, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)

        form_fields = {}

        if 'AcroForm' in doc.catalog:
            fields = resolve1(doc.catalog['AcroForm']).get('Fields', [])
            for field in fields:
                field = resolve1(field)
                name, value = field.get('T'), field.get('V')
                form_fields[name] = value

        return form_fields

fields = extract_form_fields("Fillable-923-form-test.pdf")

print(fields)