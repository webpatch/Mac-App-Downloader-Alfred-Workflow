# -*- coding: utf8 -*-
import sys
import re

from workflow import Workflow, ICON_WEB, web, ICON_WARNING
from lxml.etree import HTML
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')

MACX_PLS_ICON = '560A7E42-6169-4E6E-8DAE-E029A1914D39.png'
MACX_ICON = 'F4EE9C2E-4675-40F3-9A4A-6A0FBD61FF0A.png'
# tr_icon = 'B2D23B49-F381-4056-9847-B1701BB8CB3B.png'
log = None


def ajax_get(kw):
    r = web.post('http://soft.macx.cn/ajax_result.asp', data=dict(keyword=kw))
    r.raise_for_status()
    return r.text


def html_get(kw):
    r = web.post('http://soft.macx.cn/index.htm', data=dict(keyword=kw))
    r.raise_for_status()
    reg = re.compile('<ul class="results ">.*?</ul>', flags=re.DOTALL + re.MULTILINE)
    match = reg.search(r.text)
    if match:
        return match.group(0)
    return None


def ajax_handler(wf, text, query):
    li_arr = HTML(text).findall('.//li')
    if li_arr:
        for dd in li_arr:
            a = dd.find('.//a')
            href, title = 'http://soft.macx.cn' + a.get('href'), a.text.strip().replace('&nbsp', ' ')
            wf.add_item(title=title, subtitle=href, valid=True, arg=href, icon=MACX_ICON)
    else:
        wf.add_item(title='槽糕！没找到 “{}”'.format(' '.join(query)), subtitle='去“macx.cn”手动搜索看看？',
                    valid=True, arg='http://soft.macx.cn', icon='icon.png')


def html_handler(wf, text, query):
    if text:
        li_arr = HTML(text).findall('.//li')[2:]
        for dd in li_arr:
            a = dd.find('.//a[@class="title"]')
            href, title = a.get('href'), a.text.strip().replace('&nbsp', ' ')
            d = dd.find('.//span[@class="description"]')
            desc = d.text.strip()
            time = d.find('.//span[@class="date"]').text.strip()
            tags = '/'.join([a.text.strip() for a in d.findall('.//a')])
            wf.add_item(title=title, subtitle='[ {} ] [ {} ]  {}'.format(time, tags, desc), valid=True,
                        arg=href, icon=MACX_PLS_ICON)
    else:
        wf.add_item(title='槽糕！没找到 “{}”'.format(' '.join(query)), subtitle='去“macx.cn”手动搜索看看？',
                    valid=True, arg='http://soft.macx.cn', icon='icon.png')


def main(wf):
    parse = argparse.ArgumentParser()
    parse.add_argument('--ajax', dest='ajax', action='store_true')
    parse.add_argument('query', nargs='*', default=None)
    args = parse.parse_args()

    query = args.query
    if query:
        mode = 'ajax' if args.ajax else 'html'
        op = {'ajax': {'get': ajax_get, 'handler': ajax_handler}, 'html': {'get': html_get, 'handler': html_handler}}
        txt = op[mode]['get'](' '.join(query))
        op[mode]['handler'](wf, txt, query)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
