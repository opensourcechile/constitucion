from git import Repo
import yaml
from chapter import Chapter
from html_builder import build_html_document

REPO_PATH = 'data/constitucion_chile'
STRUCTURE_FILE = '_data/estructura.yml'
IGNORED_FILES = [
    'README.md',
    '.gitignore',
    '.vscode'
]
DESTINATION_PATH = 'actual.html'


def get_structure():
    with open(STRUCTURE_FILE) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def filter_content_files(blob):
    return blob.name not in IGNORED_FILES


def get_sorted_filepaths_from_tree(tree):
    filtered_blobs = list(filter(filter_content_files, tree.blobs))
    filtered_blobs.sort(key=lambda b: b.name)
    return filtered_blobs


def process_chapter(repo, blob, chapter_key, chapter_data):
    current_chapter = Chapter(chapter_key, chapter_data['título'], chapter_data['artículos'])
    blamed_lines = repo.blame('master', blob.name)
    lines_with_commit_object = map(lambda t: (repo.commit(t[0]), t[1]), blamed_lines)
    current_chapter.process_blamed(lines_with_commit_object)
    return current_chapter
    

if __name__ == '__main__':
    repo = Repo(REPO_PATH)
    tree = repo.tree('master')
    blobs = get_sorted_filepaths_from_tree(tree)
    data = get_structure()
    chapters = []
    for i, entry in enumerate(data):
        chapter = process_chapter(repo, blobs[i], entry, data[entry])
        chapters.append(chapter)
    document = build_html_document(chapters)
    f = open(DESTINATION_PATH, 'w')
    f.write(document)
    f.close()


    


