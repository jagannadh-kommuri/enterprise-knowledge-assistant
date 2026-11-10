import base64
import io
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
from test_app import client, login, READER

def pdf_bytes():
    writer=PdfWriter()
    for text in ['Welcome to the fictional handbook.', 'The zephyrlaunch approval deadline is December 12.']:
        page=writer.add_blank_page(width=612,height=792)
        font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        stream=DecodedStreamObject();stream.set_data(f'BT /F1 12 Tf 50 700 Td ({text}) Tj ET'.encode())
        page[NameObject('/Contents')]=writer._add_object(stream)
    out=io.BytesIO();writer.write(out);return out.getvalue()

def test_pdf_page_provenance_and_access(client):
    login(client)
    result=client.post('/api/documents/pdf',json={'title':'Launch PDF','visibility':'admin','pdf_base64':base64.b64encode(pdf_bytes()).decode()})
    assert result.status_code==201,result.text
    answer=client.post('/api/ask',json={'question':'What is the zephyrlaunch approval deadline?'}).json()
    assert answer['sources'][0]['page']==2
    assert 'December 12' in answer['answer']
    login(client,READER)
    answer=client.post('/api/ask',json={'question':'What is the zephyrlaunch approval deadline?'}).json()
    assert answer['sources']==[]
    assert client.post('/api/documents/pdf',json={'title':'x','pdf_base64':'bad'}).status_code==403

def test_invalid_pdf(client):
    login(client)
    assert client.post('/api/documents/pdf',json={'title':'bad','pdf_base64':'invalid'}).status_code==422

def test_text_has_no_invented_page(client):
    login(client)
    client.post('/api/documents',json={'title':'Policy','content':'The zephyrlaunch deadline is tomorrow.'})
    answer=client.post('/api/ask',json={'question':'zephyrlaunch deadline'}).json()
    assert answer['sources'][0]['page'] is None
