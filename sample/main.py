import configparser
from utilities.connectToDrive import connect_to_drive
from utilities.retrieveAllFiles import retrieve_file_metadata
from utilities.retrieveFileByFileName import retrieve_specific_file_metadata
from utilities.getFileContent import get_file_content
from utilities.indexFile import index_all_files
from utilities.DBOperations import createTable, fetchWordOccurence

config = configparser.ConfigParser()
config.read('configurations.ini')

# defining variables
credentials_file_path = './credentials/credentials.json'
word_occurence = {}

# establish connect and store credentials in the file
def establish_connection():
    print('Establishing connection to google drive')
    connect_to_drive(credentials_file_path) 

# retrieve all files from drive
def retrieve_all_file():
    print('Retrieving all the files metadata from drive')
    return retrieve_file_metadata(credentials_file_path)

# retrieve file by filename
def retrieve_specific_file(fileName):
    print(f"Retrieving {fileName} metadata")
    return retrieve_specific_file_metadata(credentials_file_path, fileName)

# get file content
# test file names : "Document 3.txt", "Coding Assignment.pdf", "Untitled document.docx"
def retrieve_file_content(fileName): 
    print(f"Retriving contents of the file {fileName}")
    return get_file_content(credentials_file_path, fileName)
    
def index_file():
    createTable()
    index_all_files(credentials_file_path, word_occurence)
    print('Indexed the text files')

def find_word(word):
    return fetchWordOccurence(word)
