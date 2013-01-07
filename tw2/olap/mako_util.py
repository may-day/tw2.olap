import unicodedata
import tw2.core.mako_util as tw2_mu
import logging

log = logging.getLogger(__name__)

from markupsafe import Markup

__all__ = ["etree"]

def etree(context, tagname, attrs, content):

    starttag = ""
    endtag = ""

    if tagname:
        if attrs:
            starttag = "<%s %s>" % (tagname, tw2_mu.attrs(context, attrs=attrs))
        else:
            starttag = "<%s>" % tagname

        if tagname in ("input", "br", "hr", "img"):
            endtag = ""
        else:
            endtag = "</%s>" % tagname

    c = ""
    if isinstance(content, list):
        c = "".join([etree(context, *entry)  for entry in content])
    elif isinstance(content, tuple):
        c = etree(context, *content)
    elif content:
        #c = Markup(content)
        c = content

    element = starttag + c + endtag
    #log.debug("**** element=" + element)

        
    return  element
       
