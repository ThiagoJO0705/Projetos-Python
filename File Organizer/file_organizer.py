import pathlib
import shutil

home = pathlib.Path.home()
download_folder = home / 'Downloads'

def make_folders():
    for keys in destinations.keys():
        folder_path = download_folder / keys
        folder_path.mkdir(exist_ok=True)

def move_files():
    for files in download_folder.iterdir():
        if files.is_file():
            if ignore_files_temp(files):
                continue

            moved = False
            for folder, extensions in destinations.items():
                if folder == 'Outros':
                    continue

                if files.suffix.lower() in extensions:
                    shutil.move(str(files), str(download_folder / folder / files.name))
                    moved = True
                    break

            if moved == False:
                shutil.move(str(files), str(download_folder / 'Outros' / files.name))


def ignore_files_temp(files):
    if files.suffix.lower() in files_temp:
        return True
    return False



destinations = {
    'Imagens': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg', '.jfif'},
    'PDFs': {'.pdf'},
    'Planilhas': {'.xlsx', '.xls', '.csv'},
    'Documentos': {'.docx', '.doc', '.pptx', '.ppt', '.txt'},
    'Compactados': {'.zip', '.rar', '.7z'},
    'Videos': {'.mp4', '.mov', '.avi', '.mkv'},
    'Executaveis': {'.exe', '.msi', '.bat', '.sh'},
    'Audios': {'.mp3', '.wav', '.flac', '.aac'},
    'Outros': {}
}

files_temp = {".part", ".crdownload", ".tmp"}


make_folders()
move_files()