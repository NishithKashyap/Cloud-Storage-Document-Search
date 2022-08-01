import PyPDF2
import tempfile
import docx
from apiclient import discovery, errors
from httplib2 import Http
from oauth2client import file   

def read_pdf(response):
    temp = tempfile.NamedTemporaryFile(suffix = '.pdf')
    temp.write(response)
    read_pdf = PyPDF2.PdfFileReader(temp)
    num_of_pages = read_pdf.numPages
    page_content = ''
    for i in range(num_of_pages):
        page = read_pdf.pages[i]
        page_content += page.extractText()
    temp.close()
    return page_content

def read_docx(response):
    temp = tempfile.NamedTemporaryFile(suffix = '.docx')
    temp.write(response)
    doc = docx.Document(temp)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def get_file_content(credentials_file_path, filename):

    # define store
    store = file.Storage(credentials_file_path)
    credentials = store.get()

    # define API service
    http = credentials.authorize(Http())
    drive = discovery.build('drive', 'v3', http=http)

    response = get_fileId(drive, filename)

    if response == "File not found" or filename.endswith('.txt'):
        return response

    elif filename.endswith('.pdf'):
        return read_pdf(response)
    
    elif filename.endswith('docx'):
        return read_docx(response)

def get_fileId(api_service, filename):
    page_token = None

    while True:
        try:
            param = {}

            if page_token:
                param['pageToken'] = page_token

            files = api_service.files().list(**param).execute()

            for file in files.get('files'):
                if file.get('name') == filename:
                    return api_service.files().get_media(fileId = file.get('id')).execute()

            # Google Drive API shows our files in multiple pages when the number of files exceed 100
            page_token = files.get('nextPageToken')

            if not page_token:
                break

        except errors.HttpError as error:
            print(f'An error has occurred: {error}')
            break

    return "File not found"
