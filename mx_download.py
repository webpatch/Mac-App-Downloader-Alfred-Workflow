# -*- coding: utf-8 -*-
import sys
import argparse
from subprocess import call

from lxml.etree import HTML

from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')

log = None


def main(wf):
    parse = argparse.ArgumentParser()
    parse.add_argument('--app', dest='app')
    parse.add_argument('query', nargs='*', default=None)
    args = parse.parse_args()
    query = args.query[0]
    log.warn(query)
    if query:
        id = query.rsplit('/', 1)[-1].split('.')[0]
        url = 'http://soft.macx.cn/downloado.do?softid={}&cpus=2&urls=3'.format(id)
        r = web.get(url)
        r.raise_for_status()
        a = r.text
        node = HTML(a).find('.//a[@rel="facebox"][last()]')
        log.info(node.text)
        open = ['open']
        if args.app:
            open.extend(['-a',args.app])
        if node is not None and node.text == '浏览器直接下载':
            open.append(node.get('href'))
        else:
            open.append(url)
        call(open)


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
