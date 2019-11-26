def article_to_html(article):
    result = '<details>\n'
    result += f'  <summary><span class="summary-title">Artículo {article.formatted_title}</span>'
    result += f'\n    <span class="post-meta">Temas: {", ".join(article.topics)}</span>\n  </summary>\n'
    for commit, line in article.blamed_lines:
        if len(line) > 1:
            result += f'  <div>{line}\n  </div>\n'
    result += '</details>\n'
    return result


def chapter_to_html(chapter):
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


def build_html_document(chapters):
    result = ''
    result += build_header()
    for chapter in chapters:
        result += chapter_to_html(chapter)
        result += '\n'
    return result

