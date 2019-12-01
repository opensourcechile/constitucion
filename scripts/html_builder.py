from datetime import datetime
import re

from chapter import Chapter, Article
from typing import List


def article_to_html(article: Article):
    result = '<details>\n'
    result += f'  <summary><span class="summary-title">Artículo {article.formatted_title}</span>'
    result += f'\n    <span class="post-meta">Temas: {", ".join(article.topics)}</span>\n  </summary>\n'
    for commit, line in article.blamed_lines:
        if len(line) > 1:
            result += f'  <div class="article-line" data-template="{commit.hexsha}">{line}\n  </div>\n'
    result += '</details>\n'
    return result


def chapter_to_html(chapter: Chapter):
    result = ''
    result += f'<h2>{chapter.formatted_title}</h2>\n'
    result += f'<h3>{chapter.topic}</h3>\n'
    for article in chapter.articles:
        result += article_to_html(article)
    return result


def build_header():
    result = '---\n'
    result +='layout: default\n'
    result +='title: Constitución actual\n'
    result += '---\n'
    return result


def build_templates(chapters):
    result = '<div style="display: none;">\n'
    commits = Chapter.get_all_commits_in_chapters(chapters)
    for commit in commits:
        result += build_commit_template(commit)
    result += '</div>\n'
    return result


def build_script():
    result = '<script>\n'
    script = '''  tippy('.article-line', {
    content(reference) {
      const id = reference.getAttribute('data-template');
      const template = document.getElementById(id);
      return template.innerHTML;
    },
    interactive: true,
    theme: 'light'
  });\n'''
    result += script
    result += '</script>\n'
    return result


def build_commit_template(commit):
    title = commit.message.split('\n')[0]
    formatted_title = re.sub('[^A-Za-z0-9]+', '', title)
    date = datetime.fromtimestamp(commit.authored_date).date()
    date_url = date.strftime('%Y/%m/%d')
    link = f'/{date_url}/{formatted_title}.html'
    result = f'  <div id="{commit.hexsha}">\n'
    result += f'    <a href="{link}">\n'
    result += f'    Última modificación: {title} - {date}\n'
    result += '    </a>\n'
    result += '  </div>\n'
    return result


def build_html_document(chapters: List[Chapter]):
    result = ''
    result += build_header()
    for chapter in chapters:
        result += chapter_to_html(chapter)
        result += '\n'
    result += build_templates(chapters)
    result += build_script()
    return result

