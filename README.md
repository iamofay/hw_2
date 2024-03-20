# hw_2
 OOP

# Попробуйте дописать классы для работы с файлами, расположенными не на локальном диске (облако, удаленный сервер, s3-like storage)

Все зависит от структуры хранения файлов и дальнейшего обращения к ним.

# 1. В случае хранения файлов на удаленном сервере измениться путь к этим файлам, а так же в зависимости от протокола возможно придется прикрутить авторизацию.

# 2. В случае с облаком на примере google drive необходимо добавлять библиотеки и задавать константы определяющие взаимодействие с облаком (в т.ч. авторизация):


from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

# Соответственно немного изменится логика представления файлов в облачном хранилище, т.к. в данном случае файлы демонстрируются не внутри папки, а по типам файлов: 


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    #print(service.about(fields='user, storageQuota, exportFormats, importFormats').get())

# В данном куске кода могут определяться типы отображаемых файлов, выбирается это через параметры q строки.
    results = service.files().list(
              q="mimeType='application/vnd.google-apps.folder' and name='examples'",
              spaces="drive",
              fields="nextPageToken, files(id, name)",
          ).execute()


    print(results)
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()

По цепочке нужно менять и логику сохранения копии файла, например 

def upload_basic():
  """Insert new file.
  Returns : Id's of the file uploaded

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default()

  try:
    #create drive api client
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": "download.jpeg"}
    media = MediaFileUpload("download.jpeg", mimetype="image/jpeg")
    #pylint: disable=maybe-no-member
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print(f'File ID: {file.get("id")}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  return file.get("id")


if __name__ == "__main__":
  upload_basic()

# Если глобально отвечать на вопрос: Много ли кода придется дописать / переписать при добавлении новых типов файлов и способов их хранения?

В зависимости от типа хранилища, но под каждый тип по сути свои блоки кода, которые отвечают за демонстрацию\выбор и сохранение файла. Возможно это будут отдельные функции в классах, а параметр класса будет определять соответствующую функцию для типа хранилища.

