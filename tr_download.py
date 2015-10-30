# -*- coding: utf-8 -*-
import sys
from subprocess import call

from lxml.etree import HTML

from workflow import Workflow, web
import re

reload(sys)
sys.setdefaultencoding('utf-8')

log = None

def main(wf):
    kw = wf.args[0]
    r = web.get(kw)
    r.raise_for_status()
    reg = re.compile('<ul id="dl-btn">.*</ul>', flags=re.DOTALL + re.MULTILINE)
    match = reg.search(r.text)
    if match:
        html = match.group(0)
        node = HTML(html).find('.//a')
        log.info(node.text)
        call(["open", node.get('href')])

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
