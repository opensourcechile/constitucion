from git import Repo
from datetime import datetime
from diff_match_patch import diff_match_patch

REPO_PATH = 'data/constitucion_chile'
BUILT_FILES_PATH = '_posts/'
IGNORED_FILES = [
    'README.md',
    '.gitignore',
    '.vscode'
]

def filter_content_files(blob):
    return blob.name not in IGNORED_FILES

def get_sorted_blobs_from_commit(commit):
    blobs = list(filter(filter_content_files, commit.tree.blobs))
    blobs.sort(key=lambda b: b.name)
    return blobs

def concatenate_blobs(blobs):
    concatenated = ''
    for blob in blobs:
        concatenated += '\n'
        concatenated += str(blob.data_stream.read().decode('utf-8'))
    return concatenated

def write_to_path(content, filepath):
    f = open(filepath, 'w')
    f.write(content)
    f.close()

def get_sorted_commits():
    repo = Repo(REPO_PATH)
    commits = list(repo.iter_commits('master', max_count=50))
    commits.reverse()
    return commits

def diff_contents(previous, current):
    dmp = diff_match_patch()
    diff = dmp.diff_main(previous, current)
    dmp.diff_cleanupSemantic(diff)
    return diff

def compile_diffed_markdown(diffed):
    result = ''
    for element in diffed:
        status = element[0] 
        content = element[1]
        if status == -1:
            content = content.replace('\n', '')
            result += f'<strike>{content}</strike>'
        elif status == 0:
            result += content
        elif status == 1:
            result += f'<b>{content}</b>'
    return result

def diffed_markdown(previous, current):
    diffed = diff_contents(previous, current)
    return compile_diffed_markdown(diffed)

def build_jekyll_post(content, title, date, author, previous_post_name):
    header = build_header(title, date, author, previous_post_name)
    return f'''---\n{header}\n---\n{content}'''

def build_header(title, date, author, previous_post_name):
    lines = [
        'layout: post',
        f'title: "{title}"',
        f'date: {date}',
        f'author: {author}',
        f'previous_post: {previous_post_name}'
    ]
    return '\n'.join(lines)



if __name__=='__main__':
    commits = get_sorted_commits()
    previous_commit_content = None
    previous_post_name = None
    for commit in commits:
        title = commit.message.split('\n')[0].replace(' ', '_')
        date = datetime.fromtimestamp(commit.authored_date).date()
        author = commit.author
        post_name = f'{date}-{title}'
        print(post_name)
        blobs = get_sorted_blobs_from_commit(commit)
        current_commit_content = concatenate_blobs(blobs)

        content = current_commit_content
        if previous_commit_content is not None:
            content = diffed_markdown(previous_commit_content, current_commit_content)

        jekyll_post = build_jekyll_post(content, title, date, author, previous_post_name)
        previous_post_name = post_name
        previous_commit_content = current_commit_content

        filepath = BUILT_FILES_PATH + f'{post_name}.md'
        write_to_path(jekyll_post, filepath)

