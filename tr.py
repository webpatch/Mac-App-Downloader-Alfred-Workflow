# -*- coding: utf-8 -*-
from workflow import Workflow, ICON_WEB, web
import sys
import urllib2

from HTMLParser import HTMLParser
import re
from lxml.etree import HTML

reload(sys)
sys.setdefaultencoding('utf-8')
ICON = 'B2D23B49-F381-4056-9847-B1701BB8CB3B.png'

log = None


def get_recent_list(url):
    r = web.get(url)
    r.raise_for_status()
    rs = r.text

    reg = re.compile('<section>.*?</section>', flags=re.DOTALL + re.MULTILINE)
    match = reg.search(rs)
    if match:
        return match.group(0)
    return None


def main(wf):
    if len(wf.args):
        kws = ' '.join(wf.args)
        url = 'http://www.mac-torrent-download.net/?s={}&x=0&y=0&open=1'.format(kws)
        text = get_recent_list(url)
        try:
            dd_arr = HTML(text).findall('.//dd')
            for dd in dd_arr:
                a = dd.find('.//a')
                href, title = a.get('href') + '?open=1', a.text.strip()
                info = dd.find('.//div[@class="blog_info"]')
                tags = ' / '.join([a.text for a in info.findall('.//a')])
                time = info.find('.//i').tail.strip()
                wf.add_item(title=title, subtitle='{} {}'.format(time, tags), valid=True, arg=href, icon=ICON)
        except Exception as e:
            wf.add_item(title='槽糕！没找到 “{}”'.format(kws), subtitle='去“mac-torrent-download.net”手动搜索看看？',
                        valid=True, arg=url, icon='icon.png')
        finally:
            wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
