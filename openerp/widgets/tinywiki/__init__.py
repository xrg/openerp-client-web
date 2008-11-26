import re, random, locale
from base64 import b64encode, b64decode

_image = re.compile(r'img:(.*)\.(.*)', re.UNICODE)
_internalLinks = re.compile(r'\[\[.*\]\]', re.UNICODE)

import wikimarkup

class WikiParser(wikimarkup.Parser):
	
	def parse(self, text):
		text = wikimarkup.to_unicode(text)
		text = self.strip(text)
		text = self.addImage(text)
		text = super(WikiParser, self).parse(text)
		text = self.addInternalLinks(text)
		return text
	
	def addImage(self, text):
		def image(path):
			file = path.group().replace('img:','')
			if file.startswith('http') or file.startswith('ftp') or file.startswith('http'):
				return "<img src='%s'/>" % (file)
			else:
				return "<img src='/wiki/getImage?file=%s'/>" % (file)
			
		bits = _image.sub(image, text) 
		return bits
	
	def addInternalLinks(self, text):
		from openerp import rpc
		proxy = rpc.RPCProxy('wiki.wiki')
		def link(path):
			link = path.group().replace('[','').replace('[','').replace(']','').replace(']','').split("|")
			mids = proxy.search([('name','ilike',link[0].strip())])
			if not mids:
				mids = [1]
			link_str = ""
			if len(link) == 2:
				link_str = "<a href='?model=wiki.wiki&amp;id=%s'>%s</a>" % (mids[0], link[1].strip())
			elif len(link) == 1:
				link_str = "<a href='?model=wiki.wiki&amp;id=%s'>%s</a>" % (mids[0], link[0].strip())
			
			return link_str
		
		bits = _internalLinks.sub(link, text) 
		return bits

def wiki2html(text, showToc=True):
	p = WikiParser(show_toc=showToc)
	return p.parse(text)
