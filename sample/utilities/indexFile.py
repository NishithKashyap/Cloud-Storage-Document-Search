from fileinput import filename
import sys
from apiclient import discovery, errors
import oauth2client  
from httplib2 import Http
from utilities.DBOperations import addToDB, queryDB, createIndex

def index_all_files(credentials_file_path, word_occurrences):

    # define store
    store = oauth2client.file.Storage(credentials_file_path)
    credentials = store.get()

    # define API service
    http = credentials.authorize(Http())
    api_service = discovery.build('drive', 'v3', http=http)

    page_token = None

    while True:
        try:
            param = {}

            if page_token:
                param['pageToken'] = page_token

            files = api_service.files().list(**param).execute()

            for file in files.get('files'):
                if file.get('name').endswith('.txt'):                   
                    response = api_service.files().get_media(fileId = file.get('id')).execute()                   
                    index_file(response, file.get('name'), word_occurrences)

            # Google Drive API shows our files in multiple pages when the number of files exceed 100
            page_token = files.get('nextPageToken')

            if not page_token:
                break

            word_keys = word_occurrences.keys()
            
            for word in word_keys:
                line_nums = word_occurrences[word]
                for line_num in line_nums:
                    addToDB(word.replace("'",''), line_num.replace(" ",""), word_occurrences[word][line_num])
                        
            queryDB("SELECT * FROM WORD_INDEX")
            createIndex()

        except errors.HttpError as error:
            print(f'An error has occurred: {error}')
            break

    return "File not found"

def index_file(response, fileName, word_occurrences):
    delimiter_chars = ",.;:!?'/"

    try:
        words = [ str(word).strip(delimiter_chars) for word in response.split() ]
        for word in words:
            w = str(word).lower()[2:]
            if w in word_occurrences:
                if fileName in word_occurrences[w]:
                    word_occurrences[w][fileName] = word_occurrences[w][fileName] + 1
                else:
                    word_occurrences[w][fileName] = 1
            else:
                word_occurrences[w] = {fileName: 1}

    except IOError as ioe:
        sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
        sys.exit(1)

    except Exception as e:
        sys.stderr.write("Caught Exception: " + repr(e) + "\n")
        sys.exit(1)
