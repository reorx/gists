# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def debugp(*args):
    print(*args)


class ParseError(Exception):
    pass


def main():
    with open('search.html', 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    gs = soup.find_all(class_='gist-snippet')
    for g in gs:
        print()
        g_creator = g.find(class_='creator')
        if g_creator:
            try:
                a = g_creator.find_all('a', recursive=False)[1]
            except IndexError as e:
                raise ParseError('failed to get 1 element of .creator>a: {}'.format(e))
            g_url = a['href']
            g_filename = a.string
            print('url', g_url)
            print('filename', g_filename)
            # TODO counts, time-ago
        g_table = g.find('table', class_='highlight')
        if g_table:
            buf = []
            for tr in g_table.find_all('tr'):
                line_td = list(tr.find_all('td', recursive=False))[1]
                line = line_td.text
                if line == '\n':
                    buf.append('')
                else:
                    buf.append(line)
                #print('td:', repr(line_td.text))
            g_code = '\n'.join(buf)
            print('code======:\n{}\n======'.format(g_code))


if __name__ == '__main__':
    main()
