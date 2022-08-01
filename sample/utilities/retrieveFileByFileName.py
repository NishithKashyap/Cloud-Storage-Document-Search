from apiclient import discovery, errors
from httplib2 import Http
from oauth2client import file

def retrieve_specific_file_metadata(credentials_file_path, filename_to_search):

    # define store
    store = file.Storage(credentials_file_path)
    credentials = store.get()

    # define API service
    http = credentials.authorize(Http())
    drive = discovery.build('drive', 'v3', http=http)

    return retrieve_file(drive, filename_to_search)


# define a function to retrieve all files
def retrieve_file(api_service, filename_to_search):
    page_token = None

    while True:
        try:
            param = {}

            if page_token:
                param['pageToken'] = page_token

            files = api_service.files().list(**param).execute()

            for file in files.get('files'):
                if file.get('name') == filename_to_search:
                    return file 

            # Google Drive API shows our files in multiple pages when the number of files exceed 100
            page_token = files.get('nextPageToken')

            if not page_token:
                break

        except errors.HttpError as error:
            print(f'An error has occurred: {error}')
            break

    return "File not found"