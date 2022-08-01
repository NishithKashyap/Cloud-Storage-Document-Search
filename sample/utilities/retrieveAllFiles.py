from apiclient import discovery, errors
from httplib2 import Http
from oauth2client import file

def retrieve_file_metadata(credentials_file_path):

    # define store
    store = file.Storage(credentials_file_path)
    credentials = store.get()

    # define API service
    http = credentials.authorize(Http())
    drive = discovery.build('drive', 'v3', http=http)

    return retrieve_all_files(drive)


# define a function to retrieve all files
def retrieve_all_files(api_service):
    results = []
    page_token = None

    while True:
        try:
            param = {}

            if page_token:
                param['pageToken'] = page_token

            files = api_service.files().list(**param).execute()

            # append the files from the current result page to our list
            results.extend(files.get('files'))

            # Google Drive API shows our files in multiple pages when the number of files exceed 100
            page_token = files.get('nextPageToken')

            if not page_token:
                break

        except errors.HttpError as error:
            print(f'An error has occurred: {error}')
            break

    return results