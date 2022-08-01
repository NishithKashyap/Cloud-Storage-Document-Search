from oauth2client import client, file, tools

def connect_to_drive(credentials_file_path):

    # define variables
    clientsecret_file_path = './credentials/client_secrets.json'

    # define scope
    SCOPE = 'https://www.googleapis.com/auth/drive'

    # define store
    store = file.Storage(credentials_file_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        print('Establishing connection...')
        flow = client.flow_from_clientsecrets(clientsecret_file_path, SCOPE)
        credentials = tools.run_flow(flow, store)
        print('Connection established')

    else:
        print('Connection already established')