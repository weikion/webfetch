import re
from w3lib import html

async def keep_html_tags(html_str):
    # 先去掉script 标签所有内容
    res = html.remove_tags_with_content(html_str, which_ones=("script", "link", "head", 'button'))
    # 移除注释
    res = html.remove_comments(res)

    # 定义要保留的标签
    # tags = ['p', 'br', 'img', 'strong', 'video']

    # 使用正则表达式匹配标签
    # pattern = r'<(?!\/?({})(\s|\>))[^>]*>'.format('|'.join(tags))
    # res = re.sub(pattern, '', res)

    res = html.remove_tags(res, keep=('p', 'br', 'img', 'strong', 'u', 'i', 'video'))

    # 只保留标签的src和alt属性
    pattern = r"\b(?!(?:src|alt|poster|preload|width|height))\w+=\"(.*?)\""
    res = re.sub(pattern, '', res)

    return res


# html = '''
# <html>
# <head>
# <title>示例</title>
# </HEAD>
# <body>
# <p>这是一个段落。</p>
# <br class="esf">
# <img src="image.jpg" alt="图片" style="sfesf">
# <strong>这是一个加粗的文本。</strong>
# <div>这是一个div标签。</div>
# </body>
# </html>
# '''
#
# result = keep_html_tags(html)
#
# print(result)
