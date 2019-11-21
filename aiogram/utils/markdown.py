LIST_MD_SYMBOLS = '*_`['

MD_SYMBOLS = (
    (LIST_MD_SYMBOLS[0], LIST_MD_SYMBOLS[0]),
    (LIST_MD_SYMBOLS[1], LIST_MD_SYMBOLS[1]),
    (LIST_MD_SYMBOLS[2], LIST_MD_SYMBOLS[2]),
    (LIST_MD_SYMBOLS[2] * 3 + '\n', '\n' + LIST_MD_SYMBOLS[2] * 3),
    ('<b>', '</b>'),
    ('<i>', '</i>'),
    ('<code>', '</code>'),
    ('<pre>', '</pre>'),
)


def _join(*content, sep=' '):
    return sep.join(map(str, content))


def _escape(s, symbols=LIST_MD_SYMBOLS):
    for symbol in symbols:
        s = s.replace(symbol, '\\' + symbol)
    return s


def _md(string, symbols=('', '')):
    start, end = symbols
    return start + string + end


def text(*content, sep=' '):
    """
    Join all elements with separator

    :param content:
    :param sep:
    :return:
    """
    return _join(*content, sep=sep)


def bold(*content, sep=' '):
    """
    Make bold text (Markdown)

    :param content:
    :param sep:
    :return:
    """
    return _md(_join(*content, sep=sep), symbols=MD_SYMBOLS[0])


def hbold(*content, sep=' '):
    """
    Make bold text (HTML)

    :param content:
    :param sep:
    :return:
    """
    return _md(_join(*content, sep=sep), symbols=MD_SYMBOLS[4])


def italic(*content, sep=' '):
    """
    Make italic text (Markdown)

    :param content:
    :param sep:
    :return:
    """
    return _md(_join(*content, sep=sep), symbols=MD_SYMBOLS[1])


def hitalic(*content, sep=' '):
    """
    Make italic text (HTML)

    :param content:
    :param sep:
    :return:
    """
    return _md(_join(*content, sep=sep), symbols=MD_SYMBOLS[5])


def code(*content, sep=' '):
    """
    Make mono-width text (Markdown)

    :param content:
    :param sep:
    :return:
    """
    return _md(_join(*content, sep=sep), symbols=MD_SYMBOLS[2])


def hcode(*content, sep=' '):
    """
    Make mono-width text (HTML)

    :param content:
    :param sep:
    :return:
    """
    return _md(_join(*content, sep=sep), symbols=MD_SYMBOLS[6])


def pre(*content, sep='\n'):
    """
    Make mono-width text block (Markdown)

    :param content:
    :param sep:
    :return:
    """
    return _md(_join(*content, sep=sep), symbols=MD_SYMBOLS[3])


def hpre(*content, sep='\n'):
    """
    Make mono-width text block (HTML)

    :param content:
    :param sep:
    :return:
    """
    return _md(_join(*content, sep=sep), symbols=MD_SYMBOLS[7])


def link(title, url):
    """
    Format URL (Markdown)

    :param title:
    :param url:
    :return:
    """
    return "[{0}]({1})".format(_escape(title), url)


def hlink(title, url):
    """
    Format URL (HTML)

    :param title:
    :param url:
    :return:
    """
    return "<a href=\"{0}\">{1}</a>".format(url, _escape(title))


def escape_md(*content, sep=' '):
    """
    Escape markdown text

    E.g. for usernames

    :param content:
    :param sep:
    :return:
    """
    return _escape(_join(*content, sep=sep))
