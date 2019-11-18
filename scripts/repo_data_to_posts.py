import difflib
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

def standardize_titles(text):
    lines = text.split('\n')
    special_chars = ['º','°',':','.']
    for index, line in enumerate(lines):
        if len(line) == 0:
            continue
        is_title = str.startswith(line, '#')
        if is_title and line[-1] in special_chars:
            line = line[:-1]
        # cApitulo I: Subtitulo
        is_chapter = str.startswith(line, '# ')
        if is_chapter and ':' in line:
            subs = line.split(':')
            line = f'{subs[0]}\n\n## {subs[1]}'
        line = line.replace('  ', ' ')
        lines[index] = line

    return '\n'.join(lines)


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

def diff_line_by_line(previous, current):
    ### this should be in its own class
    result = []
    diff = difflib.ndiff(previous.split('\n'), current.split('\n'))

    current_h3 = None
    modified_h3 = set()

    for line in diff:
        first = line[0]
        content = line[2:]

        is_h3 = content.startswith('### ')
        if is_h3:
            current_h3 = content[4:]
            content = content + ' {#' + current_h3.lower().replace(' ', '-').translate({ord(c): None for c in 'áéíóú'}) + '}'

        if first == '-':
            result.append(f'<div class="removed" markdown="1">{content}\n</div>')
        elif first == '+':
            result.append(f'<div class="added" markdown="1">{content}\n</div>')
        else:
            result.append(content)

        if first in ['-', '+'] and current_h3 is not None:
            modified_h3.add(current_h3)

    return ('\n'.join(result), modified_h3)


def compile_diffed_markdown(diffed):
    result = ''
    for element in diffed:
        status = element[0] 
        content = element[1]
        if status == -1:
            original_content = content
            content = content.replace('\n', '')
            content = content.replace(' ', '')
            if len(content) == 0:
                continue
            else:
                result += f'<span class="removed">{original_content}</span>'
        elif status == 0:
            result += content
        elif status == 1:
            original_content = content
            content.replace('\n', '')
            content.replace(' ', '')
            if len(content) == 0:
                result += original_content
            else:
                result += f'<span class="added">{original_content}</span>'
    return result

def diffed_markdown(previous, current):
    diffed = diff_contents(previous, current)
    return compile_diffed_markdown(diffed)

def build_jekyll_post(content, title, date, author, previous_post_name, modified_sections):
    header = build_header(title, date, author, previous_post_name, modified_sections)
    return f'''---\n{header}\n---\n{content}'''

def build_header(title, date, author, previous_post_name, modified_sections):
    lines = [
        'layout: post',
        f'title: "{title}"',
        f'date: {date}',
        f'author: {author}',
        f'previous_post: {previous_post_name}',
        'modified_sections:'
    ]
    for section in modified_sections:
        lines.append(f' - {section.lower().replace(" ", "-")}')
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
        current_commit_content = standardize_titles(current_commit_content)

        content = current_commit_content
        modified_sections = set()
        if previous_commit_content is not None:
            content, modified_sections = diff_line_by_line(previous_commit_content, current_commit_content)

        jekyll_post = build_jekyll_post(content,
                                        title,
                                        date,
                                        author,
                                        previous_post_name,
                                        modified_sections)
        previous_post_name = post_name
        previous_commit_content = current_commit_content

        filepath = BUILT_FILES_PATH + f'{post_name}.md'
        write_to_path(jekyll_post, filepath)

