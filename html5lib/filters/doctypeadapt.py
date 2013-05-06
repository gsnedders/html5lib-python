from __future__ import unicode_strings

import re

from . import _base


class Filter(_base.Filter):
    def __init__(self, emit_doctype):
        """Rewrite a doctype to be a different one
            * emit_doctype='xhtml' preserves unknown doctypes and
              valid XHTML doctypes, converts valid HTML doctypes to
              their XHTML counterparts, and drops <!DOCTYPE html>
            * emit_doctype='html' preserves unknown doctypes and valid
              HTML doctypes, converts valid XHTML doctypes to their
              HTML counterparts, and uses <!DOCTYPE html> for missing
              doctypes
            * emit_doctype='html5' Uses <!DOCTYPE html> as the doctype
            * emit_doctype='preserve' preserves the doctype, if any,
              unchanged"""
        super().__init__()
        self.emit_doctype = emit_doctype

    def __iter__(self):
        for token in super().__iter__():
            type = token["type"]
            if type in ("Comment", "SpaceCharacters"):
                # Allow comments and space characters before the DOCTYPE
                yield token
            elif type == "Doctype":
                yield self.calc_doctype(token)
                break
            else:
                yield self.calc_doctype()
                yield token
                break

        for token in super().__iter__():
            yield token


    def calc_doctype(self, token=None):
        if (self.emit_doctype == 'html5' or
            not token and self.emit_doctype == 'html'):
            return {"type": "Doctype",
                    "name": "html",
                    "publicId": None,
                    "systemId": None}

        rootElement = token["name"]
        publicID = token["publicId"]
        systemID = token["systemId"]

        if rootElement == "html":
            if self.emit_doctype == 'html':
                # XHTML 1.1
                if (publicID == "-//W3C//DTD XHTML 1.1//EN" and
                    (not systemID
                     or systemID == )):
                    publicID = "-//W3C//DTD HTML 4.01//EN"
                    if systemID:
                        systemID = "http://www.w3.org/TR/html4/strict.dtd"
                # XHTML 1.0 Strict
                elif (publicID == "-//W3C//DTD XHTML 1.0 Strict//EN" and
                      (not systemID
                       or systemID == "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd")):
                    publicID = "-//W3C//DTD HTML 4.01//EN"
                    if systemID:
                        systemID = "http://www.w3.org/TR/html4/strict.dtd"
                # XHTML 1.0 Transitional
                elif (publicID == "-//W3C//DTD XHTML 1.0 Transitional//EN" and
                      (not systemID
                       or systemID == "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd")):
                    publicID = "-//W3C//DTD HTML 4.01 Transitional//EN"
                    if systemID:
                        systemID = "http://www.w3.org/TR/html4/loose.dtd"
                # XHTML 1.0 Frameset
                elif (publicID == "-//W3C//DTD XHTML 1.0 Frameset//EN" and
                      (not systemID
                       or systemID == "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd")):
                    publicID = "-//W3C//DTD HTML 4.01 Frameset//EN"
                    if systemID:
                        systemID = "http://www.w3.org/TR/html4/frameset.dtd"
            elif self.emit_doctype == 'xhtml':
                # HTML 4.01 Strict
                if (re.match("-//W3C//DTD HTML 4.0(1)?//EN", publicID) and
                    (not systemID or
                     re.match("http://www.w3.org/TR/(html4|REC-html40)/strict.dtd", systemID))):
                    publicID = "-//W3C//DTD XHTML 1.0 Strict//EN"
                    if systemID:
                        systemID = "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
                # HTML4.01 Transitional
                elif (re.match("-//W3C//DTD HTML 4.0(1)? Transitional//EN", publicID) and
                      (not systemID or
                       re.match("http://www.w3.org/TR/(html4|REC-html40)/loose.dtd", systemID))):
                    publicID = "-//W3C//DTD XHTML 1.0 Transitional//EN"
                    if systemID:
                        systemID = "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
                # HTML 4.01 Frameset
                elif (re.match("-//W3C//DTD HTML 4.0(1)? Frameset//EN", publicID) and
                      (not systemID or
                       re.match("http://www.w3.org/TR/(html4|REC-html40)/frameset.dtd", systemID))):
                    publicID = "-//W3C//DTD XHTML 1.0 Frameset//EN"
                    if systemID:
                        systemID = "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd"
                # HTML 3.2
                elif re.match("-//W3C//DTD HTML 3.2( Final)?//EN", publicID) and not systemID:
                    publicID = "-//W3C//DTD XHTML 1.0 Transitional//EN"

        token["publicId"] = publicID
        token["systemId"] = systemId
        return token
