#!/usr/bin/env python
"""
Copyright (C) 2014  Chris Spencer (chrisspen at gmail dot com)

Measures download times for all resources on a webpage.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION))

import os
import sys
import re
import urllib
import urllib2
import urlparse
import time

from fake_useragent import UserAgent
ua = UserAgent()

JS_URLS = re.compile(r'<\s*script\s+src=[\'"]([^\'"]+)[\'"]', flags=re.DOTALL|re.IGNORECASE)
CSS_URLS = re.compile(r'<\s*link.*?href=[\'"]([^\'"]+)[\'"]', flags=re.DOTALL|re.IGNORECASE)
IMG_URLS = re.compile(r'<img\s+src=[\'"]([^\'"]+)[\'"]', flags=re.DOTALL|re.IGNORECASE)

HTML = 'HTML'
JS = 'Javascript'
CSS = 'CSS'
IMG = 'Image'

ASSET_PATTERNS = (
    (JS, JS_URLS),
    (CSS, CSS_URLS),
    (IMG, IMG_URLS),
)

class WebTimer(object):
    
    def __init__(self, url):
        self.url = url
        self.domain = None
        self.times = {} # {url:download_seconds}
        self.times_by_type = {} # {asset_type:download_seconds}
        self.html = {} # {url:html}
        self.link_types = {} # {type:set([url])}
        
    def measure(self, url, asset_type):
        
        if url.startswith('//'):
            url = 'http:' + url
        elif url.startswith('/'):
            url = 'http://' + self.domain + url
            
        if url not in self.html:
            t0 = time.time()
            # Randomize user-agent and ignore robots.txt to ensure server
            # isn't gaming load times.
            req = urllib2.Request(url, headers={ 'User-Agent': ua.random })
            html = urllib2.urlopen(req).read()
            td = time.time() - t0
            self.times[url] = td
            self.times_by_type.setdefault(asset_type, 0)
            self.times_by_type[asset_type] += td
            self.html[url] = html
        return self.html[url]
    
    @property
    def total_download_seconds(self):
        return sum(self.times.itervalues())
        
    def evaluate(self):
        self.domain = urlparse.urlparse(url).netloc
        pending = [(HTML, self.url)]
        i = 0
        while pending:
            i += 1
            next_type, next_url = pending.pop(0)
            total = len(pending) + i
            print ('\rMeasuring %i of %i %.02f%%: %s' \
                % (i, total, i/float(total)*100, next_url[:60])).ljust(80),
            sys.stdout.flush()
            html = self.measure(url=next_url, asset_type=next_type)
            if next_type == HTML:
                for name, pattern in ASSET_PATTERNS:
                    matches = pattern.findall(html)
                    self.link_types.setdefault(name, set())
                    self.link_types[name].update(matches)
                    for link in set(matches):
                        # Note, we double-check CSS links since our pattern
                        # catches non-CSS URLs.
                        if name == CSS and 'css' not in link.lower():
                            continue
                        if link not in self.html and link not in pending:
                            pending.append((name, link))

if __name__ == '__main__':
    url = sys.argv[1]
    wt = WebTimer(url=url)
    wt.evaluate()
    print
    print '-'*80
    print 'Download times by URL:'
    for url, download_time in sorted(wt.times.iteritems(), key=lambda o:o[1]):
        print download_time, url
    print '-'*80
    print 'Download times by asset type:'
    for asset_type, download_time in sorted(wt.times_by_type.iteritems(), key=lambda o:o[1]):
        print '%.02f %.02f%% %s' % (download_time, download_time/wt.total_download_seconds*100, asset_type)
    print '-'*80
    print 'Total download seconds:',wt.total_download_seconds
    