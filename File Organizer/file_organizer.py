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
            for folder, extensions in destinations.items():
                if files.suffix.lower() in extensions:
                    shutil.move(str(files), str(download_folder / folder / files.name))
                    break




destinations = {
    'Imagens': {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
    'PDFs': {'.pdf'},
    'Planilhas': {'.xlsx', '.xls', '.csv'},
    'Documentos': {'.docx', '.doc', '.pptx', '.ppt', '.txt'},
    'Compactados': {'.zip', '.rar', '.7z'},
    'Videos': {'.mp4', '.mov', '.avi', '.mkv'},
    'Executaveis': {'.exe', '.msi', '.bat', '.sh'},
    'Musicas': {'.mp3', '.wav', '.flac', '.aac'}
}

make_folders()
move_files()