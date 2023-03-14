#H/w6

import os
import shutil
import string
import unicodedata

IMAGE_EXTENSIONS = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO_EXTENSIONS = ('AVI', 'MP4', 'MOV', 'MKV')
DOCUMENT_EXTENSIONS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
AUDIO_EXTENSIONS = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVE_EXTENSIONS = ('ZIP', 'GZ', 'TAR')

def normalise(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    name = ''.join(c for c in name if c in valid_chars)
    name = name.lower().replace(' ', '_')
    return name

def organise_folder(path):
    file_list = os.listdir(path)
    folder_count = { 'images': 0, 'video': 0, 'documents': 0, 'audio': 0, 'archives': 0 }

    for file in file_list:
        if os.path.isdir(os.path.join(path, file)):
            organise_folder(os.path.join(path, file))
        else:
            ext = os.path.splitext(file)[1][1:].upper()

            if ext in IMAGE_EXTENSIONS:
                folder = 'images'
            elif ext in VIDEO_EXTENSIONS:
                folder = 'video'
            elif ext in DOCUMENT_EXTENSIONS:
                folder = 'documents'
            elif ext in AUDIO_EXTENSIONS:
                folder = 'audio'
            elif ext in ARCHIVE_EXTENSIONS:
                folder = 'archives'
                temp_dir = os.path.join(path, os.path.splitext(file)[0])
                os.makedirs(temp_dir, exist_ok=True)
                shutil.unpack_archive(os.path.join(path, file), temp_dir)
                organise_folder(temp_dir)
                shutil.rmtree(temp_dir)
            else:
                folder = 'unknown'

            if folder != 'unknown':
                src_path = os.path.join(path, file)
                dest_path = os.path.join(path, folder, normalise(os.path.splitext(file)[0]) + '.' + ext)
                os.makedirs(os.path.join(path, folder), exist_ok=True)
                os.rename(src_path, dest_path)
                folder_count[folder] += 1

    print(f"Files in {path}:")
    for folder, count in folder_count.items():
        if count > 0:
            print(f"{count} file(s) moved to {folder} folder")

if name == '__main__':
    path = '/Users/kira/Python12.Hw6.py'
    if os.path.isdir(path):
        organise_folder(path)
        print("Done.")
    else:
        print("Invalid directory path.")