from __future__ import absolute_import, division, unicode_literals

import codecs
import json
import string
import os
import gettext
_ = gettext.gettext

EOF = None

E = {
    "null-character":
        _("Null character in input stream, replaced with U+FFFD."),
    "invalid-codepoint":
        _("Invalid codepoint in stream."),
    "incorrectly-placed-solidus":
        _("Solidus (/) incorrectly placed in tag."),
    "incorrect-cr-newline-entity":
        _("Incorrect CR newline entity, replaced with LF."),
    "illegal-windows-1252-entity":
        _("Entity used with illegal number (windows-1252 reference)."),
    "cant-convert-numeric-entity":
        _("Numeric entity couldn't be converted to character "
          "(codepoint U+%(charAsInt)08x)."),
    "illegal-codepoint-for-numeric-entity":
        _("Numeric entity represents an illegal codepoint: "
          "U+%(charAsInt)08x."),
    "numeric-entity-without-semicolon":
        _("Numeric entity didn't end with ';'."),
    "expected-numeric-entity-but-got-eof":
        _("Numeric entity expected. Got end of file instead."),
    "expected-numeric-entity":
        _("Numeric entity expected but none found."),
    "named-entity-without-semicolon":
        _("Named entity didn't end with ';'."),
    "expected-named-entity":
        _("Named entity expected. Got none."),
    "attributes-in-end-tag":
        _("End tag contains unexpected attributes."),
    'self-closing-flag-on-end-tag':
        _("End tag contains unexpected self-closing flag."),
    "expected-tag-name-but-got-right-bracket":
        _("Expected tag name. Got '>' instead."),
    "expected-tag-name-but-got-question-mark":
        _("Expected tag name. Got '?' instead. (HTML doesn't "
          "support processing instructions.)"),
    "expected-tag-name":
        _("Expected tag name. Got something else instead"),
    "expected-closing-tag-but-got-right-bracket":
        _("Expected closing tag. Got '>' instead. Ignoring '</>'."),
    "expected-closing-tag-but-got-eof":
        _("Expected closing tag. Unexpected end of file."),
    "expected-closing-tag-but-got-char":
        _("Expected closing tag. Unexpected character '%(data)s' found."),
    "eof-in-tag-name":
        _("Unexpected end of file in the tag name."),
    "expected-attribute-name-but-got-eof":
        _("Unexpected end of file. Expected attribute name instead."),
    "eof-in-attribute-name":
        _("Unexpected end of file in attribute name."),
    "invalid-character-in-attribute-name":
        _("Invalid character in attribute name"),
    "duplicate-attribute":
        _("Dropped duplicate attribute on tag."),
    "expected-end-of-tag-name-but-got-eof":
        _("Unexpected end of file. Expected = or end of tag."),
    "expected-attribute-value-but-got-eof":
        _("Unexpected end of file. Expected attribute value."),
    "expected-attribute-value-but-got-right-bracket":
        _("Expected attribute value. Got '>' instead."),
    'equals-in-unquoted-attribute-value':
        _("Unexpected = in unquoted attribute"),
    'unexpected-character-in-unquoted-attribute-value':
        _("Unexpected character in unquoted attribute"),
    "invalid-character-after-attribute-name":
        _("Unexpected character after attribute name."),
    "unexpected-character-after-attribute-value":
        _("Unexpected character after attribute value."),
    "eof-in-attribute-value-double-quote":
        _("Unexpected end of file in attribute value (\")."),
    "eof-in-attribute-value-single-quote":
        _("Unexpected end of file in attribute value (')."),
    "eof-in-attribute-value-no-quotes":
        _("Unexpected end of file in attribute value."),
    "unexpected-EOF-after-solidus-in-tag":
        _("Unexpected end of file in tag. Expected >"),
    "unexpected-character-after-solidus-in-tag":
        _("Unexpected character after / in tag. Expected >"),
    "expected-dashes-or-doctype":
        _("Expected '--' or 'DOCTYPE'. Not found."),
    "unexpected-bang-after-double-dash-in-comment":
        _("Unexpected ! after -- in comment"),
    "unexpected-space-after-double-dash-in-comment":
        _("Unexpected space after -- in comment"),
    "incorrect-comment":
        _("Incorrect comment."),
    "eof-in-comment":
        _("Unexpected end of file in comment."),
    "eof-in-comment-end-dash":
        _("Unexpected end of file in comment (-)"),
    "unexpected-dash-after-double-dash-in-comment":
        _("Unexpected '-' after '--' found in comment."),
    "eof-in-comment-double-dash":
        _("Unexpected end of file in comment (--)."),
    "eof-in-comment-end-space-state":
        _("Unexpected end of file in comment."),
    "eof-in-comment-end-bang-state":
        _("Unexpected end of file in comment."),
    "unexpected-char-in-comment":
        _("Unexpected character in comment found."),
    "need-space-after-doctype":
        _("No space after literal string 'DOCTYPE'."),
    "expected-doctype-name-but-got-right-bracket":
        _("Unexpected > character. Expected DOCTYPE name."),
    "expected-doctype-name-but-got-eof":
        _("Unexpected end of file. Expected DOCTYPE name."),
    "eof-in-doctype-name":
        _("Unexpected end of file in DOCTYPE name."),
    "eof-in-doctype":
        _("Unexpected end of file in DOCTYPE."),
    "expected-space-or-right-bracket-in-doctype":
        _("Expected space or '>'. Got '%(data)s'"),
    "unexpected-end-of-doctype":
        _("Unexpected end of DOCTYPE."),
    "unexpected-char-in-doctype":
        _("Unexpected character in DOCTYPE."),
    "eof-in-innerhtml":
        _("XXX innerHTML EOF"),
    "unexpected-doctype":
        _("Unexpected DOCTYPE. Ignored."),
    "non-html-root":
        _("html needs to be the first start tag."),
    "expected-doctype-but-got-eof":
        _("Unexpected End of file. Expected DOCTYPE."),
    "unknown-doctype":
        _("Erroneous DOCTYPE."),
    "expected-doctype-but-got-chars":
        _("Unexpected non-space characters. Expected DOCTYPE."),
    "expected-doctype-but-got-start-tag":
        _("Unexpected start tag (%(name)s). Expected DOCTYPE."),
    "expected-doctype-but-got-end-tag":
        _("Unexpected end tag (%(name)s). Expected DOCTYPE."),
    "end-tag-after-implied-root":
        _("Unexpected end tag (%(name)s) after the (implied) root element."),
    "expected-named-closing-tag-but-got-eof":
        _("Unexpected end of file. Expected end tag (%(name)s)."),
    "two-heads-are-not-better-than-one":
        _("Unexpected start tag head in existing head. Ignored."),
    "unexpected-end-tag":
        _("Unexpected end tag (%(name)s). Ignored."),
    "unexpected-start-tag-out-of-my-head":
        _("Unexpected start tag (%(name)s) that can be in head. Moved."),
    "unexpected-start-tag":
        _("Unexpected start tag (%(name)s)."),
    "missing-end-tag":
        _("Missing end tag (%(name)s)."),
    "missing-end-tags":
        _("Missing end tags (%(name)s)."),
    "unexpected-start-tag-implies-end-tag":
        _("Unexpected start tag (%(startName)s) "
          "implies end tag (%(endName)s)."),
    "unexpected-start-tag-treated-as":
        _("Unexpected start tag (%(originalName)s). Treated as %(newName)s."),
    "deprecated-tag":
        _("Unexpected start tag %(name)s. Don't use it!"),
    "unexpected-start-tag-ignored":
        _("Unexpected start tag %(name)s. Ignored."),
    "expected-one-end-tag-but-got-another":
        _("Unexpected end tag (%(gotName)s). "
          "Missing end tag (%(expectedName)s)."),
    "end-tag-too-early":
        _("End tag (%(name)s) seen too early. Expected other end tag."),
    "end-tag-too-early-named":
        _("Unexpected end tag (%(gotName)s). Expected end tag (%(expectedName)s)."),
    "end-tag-too-early-ignored":
        _("End tag (%(name)s) seen too early. Ignored."),
    "adoption-agency-1.1":
        _("End tag (%(name)s) violates step 1, "
          "paragraph 1 of the adoption agency algorithm."),
    "adoption-agency-1.2":
        _("End tag (%(name)s) violates step 1, "
          "paragraph 2 of the adoption agency algorithm."),
    "adoption-agency-1.3":
        _("End tag (%(name)s) violates step 1, "
          "paragraph 3 of the adoption agency algorithm."),
    "adoption-agency-4.4":
        _("End tag (%(name)s) violates step 4, "
          "paragraph 4 of the adoption agency algorithm."),
    "unexpected-end-tag-treated-as":
        _("Unexpected end tag (%(originalName)s). Treated as %(newName)s."),
    "no-end-tag":
        _("This element (%(name)s) has no end tag."),
    "unexpected-implied-end-tag-in-table":
        _("Unexpected implied end tag (%(name)s) in the table phase."),
    "unexpected-implied-end-tag-in-table-body":
        _("Unexpected implied end tag (%(name)s) in the table body phase."),
    "unexpected-char-implies-table-voodoo":
        _("Unexpected non-space characters in "
          "table context caused voodoo mode."),
    "unexpected-hidden-input-in-table":
        _("Unexpected input with type hidden in table context."),
    "unexpected-form-in-table":
        _("Unexpected form in table context."),
    "unexpected-start-tag-implies-table-voodoo":
        _("Unexpected start tag (%(name)s) in "
          "table context caused voodoo mode."),
    "unexpected-end-tag-implies-table-voodoo":
        _("Unexpected end tag (%(name)s) in "
          "table context caused voodoo mode."),
    "unexpected-cell-in-table-body":
        _("Unexpected table cell start tag (%(name)s) "
          "in the table body phase."),
    "unexpected-cell-end-tag":
        _("Got table cell end tag (%(name)s) "
          "while required end tags are missing."),
    "unexpected-end-tag-in-table-body":
        _("Unexpected end tag (%(name)s) in the table body phase. Ignored."),
    "unexpected-implied-end-tag-in-table-row":
        _("Unexpected implied end tag (%(name)s) in the table row phase."),
    "unexpected-end-tag-in-table-row":
        _("Unexpected end tag (%(name)s) in the table row phase. Ignored."),
    "unexpected-select-in-select":
        _("Unexpected select start tag in the select phase "
          "treated as select end tag."),
    "unexpected-input-in-select":
        _("Unexpected input start tag in the select phase."),
    "unexpected-start-tag-in-select":
        _("Unexpected start tag token (%(name)s in the select phase. "
          "Ignored."),
    "unexpected-end-tag-in-select":
        _("Unexpected end tag (%(name)s) in the select phase. Ignored."),
    "unexpected-table-element-start-tag-in-select-in-table":
        _("Unexpected table element start tag (%(name)s) in the select in table phase."),
    "unexpected-table-element-end-tag-in-select-in-table":
        _("Unexpected table element end tag (%(name)s) in the select in table phase."),
    "unexpected-char-after-body":
        _("Unexpected non-space characters in the after body phase."),
    "unexpected-start-tag-after-body":
        _("Unexpected start tag token (%(name)s)"
          " in the after body phase."),
    "unexpected-end-tag-after-body":
        _("Unexpected end tag token (%(name)s)"
          " in the after body phase."),
    "unexpected-char-in-frameset":
        _("Unexpected characters in the frameset phase. Characters ignored."),
    "unexpected-start-tag-in-frameset":
        _("Unexpected start tag token (%(name)s)"
          " in the frameset phase. Ignored."),
    "unexpected-frameset-in-frameset-innerhtml":
        _("Unexpected end tag token (frameset) "
          "in the frameset phase (innerHTML)."),
    "unexpected-end-tag-in-frameset":
        _("Unexpected end tag token (%(name)s)"
          " in the frameset phase. Ignored."),
    "unexpected-char-after-frameset":
        _("Unexpected non-space characters in the "
          "after frameset phase. Ignored."),
    "unexpected-start-tag-after-frameset":
        _("Unexpected start tag (%(name)s)"
          " in the after frameset phase. Ignored."),
    "unexpected-end-tag-after-frameset":
        _("Unexpected end tag (%(name)s)"
          " in the after frameset phase. Ignored."),
    "unexpected-end-tag-after-body-innerhtml":
        _("Unexpected end tag after body(innerHtml)"),
    "expected-eof-but-got-char":
        _("Unexpected non-space characters. Expected end of file."),
    "expected-eof-but-got-start-tag":
        _("Unexpected start tag (%(name)s)"
          ". Expected end of file."),
    "expected-eof-but-got-end-tag":
        _("Unexpected end tag (%(name)s)"
          ". Expected end of file."),
    "eof-in-table":
        _("Unexpected end of file. Expected table content."),
    "eof-in-select":
        _("Unexpected end of file. Expected select content."),
    "eof-in-frameset":
        _("Unexpected end of file. Expected frameset content."),
    "eof-in-script-in-script":
        _("Unexpected end of file. Expected script content."),
    "eof-in-foreign-lands":
        _("Unexpected end of file. Expected foreign content"),
    "non-void-element-with-trailing-solidus":
        _("Trailing solidus not allowed on element %(name)s"),
    "unexpected-html-element-in-foreign-content":
        _("Element %(name)s not allowed in a non-html context"),
    "unexpected-end-tag-before-html":
        _("Unexpected end tag (%(name)s) before html."),
    "XXX-undefined-error":
        _("Undefined error (this sucks and should be fixed)"),
}

namespaces = {
    "html": "http://www.w3.org/1999/xhtml",
    "mathml": "http://www.w3.org/1998/Math/MathML",
    "svg": "http://www.w3.org/2000/svg",
    "xlink": "http://www.w3.org/1999/xlink",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xmlns": "http://www.w3.org/2000/xmlns/"
}

scopingElements = frozenset((
    (namespaces["html"], "applet"),
    (namespaces["html"], "caption"),
    (namespaces["html"], "html"),
    (namespaces["html"], "marquee"),
    (namespaces["html"], "object"),
    (namespaces["html"], "table"),
    (namespaces["html"], "td"),
    (namespaces["html"], "th"),
    (namespaces["mathml"], "mi"),
    (namespaces["mathml"], "mo"),
    (namespaces["mathml"], "mn"),
    (namespaces["mathml"], "ms"),
    (namespaces["mathml"], "mtext"),
    (namespaces["mathml"], "annotation-xml"),
    (namespaces["svg"], "foreignObject"),
    (namespaces["svg"], "desc"),
    (namespaces["svg"], "title"),
))

formattingElements = frozenset((
    (namespaces["html"], "a"),
    (namespaces["html"], "b"),
    (namespaces["html"], "big"),
    (namespaces["html"], "code"),
    (namespaces["html"], "em"),
    (namespaces["html"], "font"),
    (namespaces["html"], "i"),
    (namespaces["html"], "nobr"),
    (namespaces["html"], "s"),
    (namespaces["html"], "small"),
    (namespaces["html"], "strike"),
    (namespaces["html"], "strong"),
    (namespaces["html"], "tt"),
    (namespaces["html"], "u")
))

specialElements = frozenset((
    (namespaces["html"], "address"),
    (namespaces["html"], "applet"),
    (namespaces["html"], "area"),
    (namespaces["html"], "article"),
    (namespaces["html"], "aside"),
    (namespaces["html"], "base"),
    (namespaces["html"], "basefont"),
    (namespaces["html"], "bgsound"),
    (namespaces["html"], "blockquote"),
    (namespaces["html"], "body"),
    (namespaces["html"], "br"),
    (namespaces["html"], "button"),
    (namespaces["html"], "caption"),
    (namespaces["html"], "center"),
    (namespaces["html"], "col"),
    (namespaces["html"], "colgroup"),
    (namespaces["html"], "command"),
    (namespaces["html"], "dd"),
    (namespaces["html"], "details"),
    (namespaces["html"], "dir"),
    (namespaces["html"], "div"),
    (namespaces["html"], "dl"),
    (namespaces["html"], "dt"),
    (namespaces["html"], "embed"),
    (namespaces["html"], "fieldset"),
    (namespaces["html"], "figure"),
    (namespaces["html"], "footer"),
    (namespaces["html"], "form"),
    (namespaces["html"], "frame"),
    (namespaces["html"], "frameset"),
    (namespaces["html"], "h1"),
    (namespaces["html"], "h2"),
    (namespaces["html"], "h3"),
    (namespaces["html"], "h4"),
    (namespaces["html"], "h5"),
    (namespaces["html"], "h6"),
    (namespaces["html"], "head"),
    (namespaces["html"], "header"),
    (namespaces["html"], "hr"),
    (namespaces["html"], "html"),
    (namespaces["html"], "iframe"),
    # Note that image is commented out in the spec as "this isn't an
    # element that can end up on the stack, so it doesn't matter,"
    (namespaces["html"], "image"),
    (namespaces["html"], "img"),
    (namespaces["html"], "input"),
    (namespaces["html"], "isindex"),
    (namespaces["html"], "li"),
    (namespaces["html"], "link"),
    (namespaces["html"], "listing"),
    (namespaces["html"], "marquee"),
    (namespaces["html"], "menu"),
    (namespaces["html"], "meta"),
    (namespaces["html"], "nav"),
    (namespaces["html"], "noembed"),
    (namespaces["html"], "noframes"),
    (namespaces["html"], "noscript"),
    (namespaces["html"], "object"),
    (namespaces["html"], "ol"),
    (namespaces["html"], "p"),
    (namespaces["html"], "param"),
    (namespaces["html"], "plaintext"),
    (namespaces["html"], "pre"),
    (namespaces["html"], "script"),
    (namespaces["html"], "section"),
    (namespaces["html"], "select"),
    (namespaces["html"], "style"),
    (namespaces["html"], "table"),
    (namespaces["html"], "tbody"),
    (namespaces["html"], "td"),
    (namespaces["html"], "textarea"),
    (namespaces["html"], "tfoot"),
    (namespaces["html"], "th"),
    (namespaces["html"], "thead"),
    (namespaces["html"], "title"),
    (namespaces["html"], "tr"),
    (namespaces["html"], "ul"),
    (namespaces["html"], "wbr"),
    (namespaces["html"], "xmp"),
    (namespaces["svg"], "foreignObject")
))

htmlIntegrationPointElements = frozenset((
    (namespaces["mathml"], "annotaion-xml"),
    (namespaces["svg"], "foreignObject"),
    (namespaces["svg"], "desc"),
    (namespaces["svg"], "title")
))

mathmlTextIntegrationPointElements = frozenset((
    (namespaces["mathml"], "mi"),
    (namespaces["mathml"], "mo"),
    (namespaces["mathml"], "mn"),
    (namespaces["mathml"], "ms"),
    (namespaces["mathml"], "mtext")
))

spaceCharacters = frozenset((
    "\t",
    "\n",
    "\u000C",
    " ",
    "\r"
))

tableInsertModeElements = frozenset((
    "table",
    "tbody",
    "tfoot",
    "thead",
    "tr"
))

asciiLowercase = frozenset(string.ascii_lowercase)
asciiUppercase = frozenset(string.ascii_uppercase)
asciiLetters = frozenset(string.ascii_letters)
digits = frozenset(string.digits)
hexDigits = frozenset(string.hexdigits)

asciiUpper2Lower = dict([(ord(c), ord(c.lower()))
                         for c in string.ascii_uppercase])

# Heading elements need to be ordered
headingElements = (
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6"
)

voidElements = frozenset((
    "base",
    "command",
    "event-source",
    "link",
    "meta",
    "hr",
    "br",
    "img",
    "embed",
    "param",
    "area",
    "col",
    "input",
    "source",
    "track"
))

cdataElements = frozenset(('title', 'textarea'))

rcdataElements = frozenset((
    'style',
    'script',
    'xmp',
    'iframe',
    'noembed',
    'noframes',
    'noscript'
))

booleanAttributes = {
    "": frozenset(("irrelevant",)),
    "style": frozenset(("scoped",)),
    "img": frozenset(("ismap",)),
    "audio": frozenset(("autoplay", "controls")),
    "video": frozenset(("autoplay", "controls")),
    "script": frozenset(("defer", "async")),
    "details": frozenset(("open",)),
    "datagrid": frozenset(("multiple", "disabled")),
    "command": frozenset(("hidden", "disabled", "checked", "default")),
    "hr": frozenset(("noshade")),
    "menu": frozenset(("autosubmit",)),
    "fieldset": frozenset(("disabled", "readonly")),
    "option": frozenset(("disabled", "readonly", "selected")),
    "optgroup": frozenset(("disabled", "readonly")),
    "button": frozenset(("disabled", "autofocus")),
    "input": frozenset(("disabled", "readonly", "required", "autofocus", "checked", "ismap")),
    "select": frozenset(("disabled", "readonly", "autofocus", "multiple")),
    "output": frozenset(("disabled", "readonly")),
}

# entitiesWindows1252 has to be _ordered_ and needs to have an index. It
# therefore can't be a frozenset.
entitiesWindows1252 = (
    8364,   # 0x80  0x20AC  EURO SIGN
    65533,  # 0x81          UNDEFINED
    8218,   # 0x82  0x201A  SINGLE LOW-9 QUOTATION MARK
    402,    # 0x83  0x0192  LATIN SMALL LETTER F WITH HOOK
    8222,   # 0x84  0x201E  DOUBLE LOW-9 QUOTATION MARK
    8230,   # 0x85  0x2026  HORIZONTAL ELLIPSIS
    8224,   # 0x86  0x2020  DAGGER
    8225,   # 0x87  0x2021  DOUBLE DAGGER
    710,    # 0x88  0x02C6  MODIFIER LETTER CIRCUMFLEX ACCENT
    8240,   # 0x89  0x2030  PER MILLE SIGN
    352,    # 0x8A  0x0160  LATIN CAPITAL LETTER S WITH CARON
    8249,   # 0x8B  0x2039  SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    338,    # 0x8C  0x0152  LATIN CAPITAL LIGATURE OE
    65533,  # 0x8D          UNDEFINED
    381,    # 0x8E  0x017D  LATIN CAPITAL LETTER Z WITH CARON
    65533,  # 0x8F          UNDEFINED
    65533,  # 0x90          UNDEFINED
    8216,   # 0x91  0x2018  LEFT SINGLE QUOTATION MARK
    8217,   # 0x92  0x2019  RIGHT SINGLE QUOTATION MARK
    8220,   # 0x93  0x201C  LEFT DOUBLE QUOTATION MARK
    8221,   # 0x94  0x201D  RIGHT DOUBLE QUOTATION MARK
    8226,   # 0x95  0x2022  BULLET
    8211,   # 0x96  0x2013  EN DASH
    8212,   # 0x97  0x2014  EM DASH
    732,    # 0x98  0x02DC  SMALL TILDE
    8482,   # 0x99  0x2122  TRADE MARK SIGN
    353,    # 0x9A  0x0161  LATIN SMALL LETTER S WITH CARON
    8250,   # 0x9B  0x203A  SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    339,    # 0x9C  0x0153  LATIN SMALL LIGATURE OE
    65533,  # 0x9D          UNDEFINED
    382,    # 0x9E  0x017E  LATIN SMALL LETTER Z WITH CARON
    376     # 0x9F  0x0178  LATIN CAPITAL LETTER Y WITH DIAERESIS
)

xmlEntities = frozenset(('lt;', 'gt;', 'amp;', 'apos;', 'quot;'))

entities_file = os.path.join(os.path.dirname(__file__), "data", "entities.json")
with codecs.open(entities_file, "r", "utf8") as fp:
    entities = dict([(name[1:], reprs["characters"]) for name, reprs in
                     json.load(fp).items()])

replacementCharacters = {
    0x0: "\uFFFD",
    0x0d: "\u000D",
    0x80: "\u20AC",
    0x81: "\u0081",
    0x81: "\u0081",
    0x82: "\u201A",
    0x83: "\u0192",
    0x84: "\u201E",
    0x85: "\u2026",
    0x86: "\u2020",
    0x87: "\u2021",
    0x88: "\u02C6",
    0x89: "\u2030",
    0x8A: "\u0160",
    0x8B: "\u2039",
    0x8C: "\u0152",
    0x8D: "\u008D",
    0x8E: "\u017D",
    0x8F: "\u008F",
    0x90: "\u0090",
    0x91: "\u2018",
    0x92: "\u2019",
    0x93: "\u201C",
    0x94: "\u201D",
    0x95: "\u2022",
    0x96: "\u2013",
    0x97: "\u2014",
    0x98: "\u02DC",
    0x99: "\u2122",
    0x9A: "\u0161",
    0x9B: "\u203A",
    0x9C: "\u0153",
    0x9D: "\u009D",
    0x9E: "\u017E",
    0x9F: "\u0178",
}

encodings = {
    '437': 'cp437',
    '850': 'cp850',
    '852': 'cp852',
    '855': 'cp855',
    '857': 'cp857',
    '860': 'cp860',
    '861': 'cp861',
    '862': 'cp862',
    '863': 'cp863',
    '865': 'cp865',
    '866': 'cp866',
    '869': 'cp869',
    'ansix341968': 'ascii',
    'ansix341986': 'ascii',
    'arabic': 'iso8859-6',
    'ascii': 'ascii',
    'asmo708': 'iso8859-6',
    'big5': 'big5',
    'big5hkscs': 'big5hkscs',
    'chinese': 'gbk',
    'cp037': 'cp037',
    'cp1026': 'cp1026',
    'cp154': 'ptcp154',
    'cp367': 'ascii',
    'cp424': 'cp424',
    'cp437': 'cp437',
    'cp500': 'cp500',
    'cp775': 'cp775',
    'cp819': 'windows-1252',
    'cp850': 'cp850',
    'cp852': 'cp852',
    'cp855': 'cp855',
    'cp857': 'cp857',
    'cp860': 'cp860',
    'cp861': 'cp861',
    'cp862': 'cp862',
    'cp863': 'cp863',
    'cp864': 'cp864',
    'cp865': 'cp865',
    'cp866': 'cp866',
    'cp869': 'cp869',
    'cp936': 'gbk',
    'cpgr': 'cp869',
    'cpis': 'cp861',
    'csascii': 'ascii',
    'csbig5': 'big5',
    'cseuckr': 'cp949',
    'cseucpkdfmtjapanese': 'euc_jp',
    'csgb2312': 'gbk',
    'cshproman8': 'hp-roman8',
    'csibm037': 'cp037',
    'csibm1026': 'cp1026',
    'csibm424': 'cp424',
    'csibm500': 'cp500',
    'csibm855': 'cp855',
    'csibm857': 'cp857',
    'csibm860': 'cp860',
    'csibm861': 'cp861',
    'csibm863': 'cp863',
    'csibm864': 'cp864',
    'csibm865': 'cp865',
    'csibm866': 'cp866',
    'csibm869': 'cp869',
    'csiso2022jp': 'iso2022_jp',
    'csiso2022jp2': 'iso2022_jp_2',
    'csiso2022kr': 'iso2022_kr',
    'csiso58gb231280': 'gbk',
    'csisolatin1': 'windows-1252',
    'csisolatin2': 'iso8859-2',
    'csisolatin3': 'iso8859-3',
    'csisolatin4': 'iso8859-4',
    'csisolatin5': 'windows-1254',
    'csisolatin6': 'iso8859-10',
    'csisolatinarabic': 'iso8859-6',
    'csisolatincyrillic': 'iso8859-5',
    'csisolatingreek': 'iso8859-7',
    'csisolatinhebrew': 'iso8859-8',
    'cskoi8r': 'koi8-r',
    'csksc56011987': 'cp949',
    'cspc775baltic': 'cp775',
    'cspc850multilingual': 'cp850',
    'cspc862latinhebrew': 'cp862',
    'cspc8codepage437': 'cp437',
    'cspcp852': 'cp852',
    'csptcp154': 'ptcp154',
    'csshiftjis': 'shift_jis',
    'csunicode11utf7': 'utf-7',
    'cyrillic': 'iso8859-5',
    'cyrillicasian': 'ptcp154',
    'ebcdiccpbe': 'cp500',
    'ebcdiccpca': 'cp037',
    'ebcdiccpch': 'cp500',
    'ebcdiccphe': 'cp424',
    'ebcdiccpnl': 'cp037',
    'ebcdiccpus': 'cp037',
    'ebcdiccpwt': 'cp037',
    'ecma114': 'iso8859-6',
    'ecma118': 'iso8859-7',
    'elot928': 'iso8859-7',
    'eucjp': 'euc_jp',
    'euckr': 'cp949',
    'extendedunixcodepackedformatforjapanese': 'euc_jp',
    'gb18030': 'gb18030',
    'gb2312': 'gbk',
    'gb231280': 'gbk',
    'gbk': 'gbk',
    'greek': 'iso8859-7',
    'greek8': 'iso8859-7',
    'hebrew': 'iso8859-8',
    'hproman8': 'hp-roman8',
    'hzgb2312': 'hz',
    'ibm037': 'cp037',
    'ibm1026': 'cp1026',
    'ibm367': 'ascii',
    'ibm424': 'cp424',
    'ibm437': 'cp437',
    'ibm500': 'cp500',
    'ibm775': 'cp775',
    'ibm819': 'windows-1252',
    'ibm850': 'cp850',
    'ibm852': 'cp852',
    'ibm855': 'cp855',
    'ibm857': 'cp857',
    'ibm860': 'cp860',
    'ibm861': 'cp861',
    'ibm862': 'cp862',
    'ibm863': 'cp863',
    'ibm864': 'cp864',
    'ibm865': 'cp865',
    'ibm866': 'cp866',
    'ibm869': 'cp869',
    'iso2022jp': 'iso2022_jp',
    'iso2022jp2': 'iso2022_jp_2',
    'iso2022kr': 'iso2022_kr',
    'iso646irv1991': 'ascii',
    'iso646us': 'ascii',
    'iso88591': 'windows-1252',
    'iso885910': 'iso8859-10',
    'iso8859101992': 'iso8859-10',
    'iso885911987': 'windows-1252',
    'iso885913': 'iso8859-13',
    'iso885914': 'iso8859-14',
    'iso8859141998': 'iso8859-14',
    'iso885915': 'iso8859-15',
    'iso885916': 'iso8859-16',
    'iso8859162001': 'iso8859-16',
    'iso88592': 'iso8859-2',
    'iso885921987': 'iso8859-2',
    'iso88593': 'iso8859-3',
    'iso885931988': 'iso8859-3',
    'iso88594': 'iso8859-4',
    'iso885941988': 'iso8859-4',
    'iso88595': 'iso8859-5',
    'iso885951988': 'iso8859-5',
    'iso88596': 'iso8859-6',
    'iso885961987': 'iso8859-6',
    'iso88597': 'iso8859-7',
    'iso885971987': 'iso8859-7',
    'iso88598': 'iso8859-8',
    'iso885981988': 'iso8859-8',
    'iso88599': 'windows-1254',
    'iso885991989': 'windows-1254',
    'isoceltic': 'iso8859-14',
    'isoir100': 'windows-1252',
    'isoir101': 'iso8859-2',
    'isoir109': 'iso8859-3',
    'isoir110': 'iso8859-4',
    'isoir126': 'iso8859-7',
    'isoir127': 'iso8859-6',
    'isoir138': 'iso8859-8',
    'isoir144': 'iso8859-5',
    'isoir148': 'windows-1254',
    'isoir149': 'cp949',
    'isoir157': 'iso8859-10',
    'isoir199': 'iso8859-14',
    'isoir226': 'iso8859-16',
    'isoir58': 'gbk',
    'isoir6': 'ascii',
    'koi8r': 'koi8-r',
    'koi8u': 'koi8-u',
    'korean': 'cp949',
    'ksc5601': 'cp949',
    'ksc56011987': 'cp949',
    'ksc56011989': 'cp949',
    'l1': 'windows-1252',
    'l10': 'iso8859-16',
    'l2': 'iso8859-2',
    'l3': 'iso8859-3',
    'l4': 'iso8859-4',
    'l5': 'windows-1254',
    'l6': 'iso8859-10',
    'l8': 'iso8859-14',
    'latin1': 'windows-1252',
    'latin10': 'iso8859-16',
    'latin2': 'iso8859-2',
    'latin3': 'iso8859-3',
    'latin4': 'iso8859-4',
    'latin5': 'windows-1254',
    'latin6': 'iso8859-10',
    'latin8': 'iso8859-14',
    'latin9': 'iso8859-15',
    'ms936': 'gbk',
    'mskanji': 'shift_jis',
    'pt154': 'ptcp154',
    'ptcp154': 'ptcp154',
    'r8': 'hp-roman8',
    'roman8': 'hp-roman8',
    'shiftjis': 'shift_jis',
    'tis620': 'cp874',
    'unicode11utf7': 'utf-7',
    'us': 'ascii',
    'usascii': 'ascii',
    'utf16': 'utf-16',
    'utf16be': 'utf-16-be',
    'utf16le': 'utf-16-le',
    'utf8': 'utf-8',
    'windows1250': 'cp1250',
    'windows1251': 'cp1251',
    'windows1252': 'cp1252',
    'windows1253': 'cp1253',
    'windows1254': 'cp1254',
    'windows1255': 'cp1255',
    'windows1256': 'cp1256',
    'windows1257': 'cp1257',
    'windows1258': 'cp1258',
    'windows936': 'gbk',
    'x-x-big5': 'big5'}

tokenTypes = {
    "Doctype": 0,
    "Characters": 1,
    "SpaceCharacters": 2,
    "StartTag": 3,
    "EndTag": 4,
    "EmptyTag": 5,
    "Comment": 6,
    "ParseError": 7
}

tagTokenTypes = frozenset((tokenTypes["StartTag"], tokenTypes["EndTag"],
                           tokenTypes["EmptyTag"]))


prefixes = dict([(v, k) for k, v in namespaces.items()])
prefixes["http://www.w3.org/1998/Math/MathML"] = "math"


class DataLossWarning(UserWarning):
    pass


class ReparseException(Exception):
    pass
