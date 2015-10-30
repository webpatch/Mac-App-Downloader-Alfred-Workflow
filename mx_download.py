# -*- coding: utf-8 -*-
import sys
from subprocess import call

from lxml.etree import HTML

from workflow import Workflow, web

reload(sys)
sys.setdefaultencoding('utf-8')

log = None


def main(wf):
    kw = wf.args[0]
    id = kw.rsplit('/', 1)[-1].split('.')[0]
    url = 'http://soft.macx.cn/downloado.do?softid={}&cpus=2&urls=3'.format(id)
    r = web.get(url)
    r.raise_for_status()
    a = r.text
    node = HTML(a).find('.//a[@rel="facebox"][last()]')
    log.info(node.text)
    if node is not None and node.text == '浏览器直接下载':
        call(["open", node.get('href')])
    else:
        call(["open", url])


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
