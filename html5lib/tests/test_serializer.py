from __future__ import absolute_import, division, unicode_literals

import os
import warnings
import json
import unittest

from difflib import unified_diff

from .support import get_data_files, TestData

try:
    unittest.TestCase.assertEqual
except AttributeError:
    unittest.TestCase.assertEqual = unittest.TestCase.assertEquals

import html5lib
from html5lib import html5parser, constants
from html5lib.serializer import HTMLSerializer, serialize
from html5lib.treewalkers._base import TreeWalker
from html5lib.constants import DataLossWarning

optionals_loaded = []

try:
    from lxml import etree
    optionals_loaded.append("lxml")
except ImportError:
    pass

default_namespace = constants.namespaces["html"]


class JsonWalker(TreeWalker):
    def __iter__(self):
        for token in self.tree:
            type = token[0]
            if type == "StartTag":
                if len(token) == 4:
                    namespace, name, attrib = token[1:4]
                else:
                    namespace = default_namespace
                    name, attrib = token[1:3]
                yield self.startTag(namespace, name, self._convertAttrib(attrib))
            elif type == "EndTag":
                if len(token) == 3:
                    namespace, name = token[1:3]
                else:
                    namespace = default_namespace
                    name = token[1]
                yield self.endTag(namespace, name)
            elif type == "EmptyTag":
                if len(token) == 4:
                    namespace, name, attrib = token[1:]
                else:
                    namespace = default_namespace
                    name, attrib = token[1:]
                for token in self.emptyTag(namespace, name, self._convertAttrib(attrib)):
                    yield token
            elif type == "Comment":
                yield self.comment(token[1])
            elif type in ("Characters", "SpaceCharacters"):
                for token in self.text(token[1]):
                    yield token
            elif type == "Doctype":
                if len(token) == 4:
                    yield self.doctype(token[1], token[2], token[3])
                elif len(token) == 3:
                    yield self.doctype(token[1], token[2])
                else:
                    yield self.doctype(token[1])
            else:
                raise ValueError("Unknown token type: " + type)

    def _convertAttrib(self, attribs):
        """html5lib tree-walkers use a dict of (namespace, name): value for
        attributes, but JSON cannot represent this. Convert from the format
        in the serializer tests (a list of dicts with "namespace", "name",
        and "value" as keys) to html5lib's tree-walker format."""
        attrs = {}
        for attrib in attribs:
            name = (attrib["namespace"], attrib["name"])
            assert(name not in attrs)
            attrs[name] = attrib["value"]
        return attrs


def serialize_html(input, options):
    options = dict([(str(k), v) for k, v in options.items()])
    stream = JsonWalker(input)
    serializer = HTMLSerializer(alphabetical_attributes=True, **options)
    return serializer.render(stream, options.get("encoding", None))


def runSerializerTest(input, expected, options):
    encoding = options.get("encoding", None)

    if encoding:
        encode = lambda x: x.encode(encoding)
        expected = list(map(encode, expected))

    result = serialize_html(input, options)
    if len(expected) == 1:
        assert expected[0] == result, "Expected:\n%s\nActual:\n%s\nOptions:\n%s" % (expected[0], result, str(options))
    elif result not in expected:
        assert False, "Expected: %s, Received: %s" % (expected, result)


def runRoundtripTest(input, options):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        p = html5parser.HTMLParser(strict=True)
        try:
            tree = p.parse(input)
        except html5parser.ParseError:
            return
        try:
            serialized = html5lib.serialize(tree)
        except DataLossWarning:
            # Amnesty for those who confess
            return
        p = html5parser.HTMLParser()
        tree2 = p.parse(serialized)
        expected = p.tree.testSerializer(tree)
        output = p.tree.testSerializer(tree2)
        diff = "".join(unified_diff([line + "\n" for line in expected.splitlines()],
                                    [line + "\n" for line in output.splitlines()],
                                    "Expected", "Received"))
        assert expected == output, "\n".join([
            "", "Input:", input,
            "", "Expected:", expected,
            "", "Serialization:", serialized,
            "", "Received:", output,
            "", "Diff:", diff
        ])


class EncodingTestCase(unittest.TestCase):
    def throwsWithLatin1(self, input):
        self.assertRaises(UnicodeEncodeError, serialize_html, input, {"encoding": "iso-8859-1"})

    def testDoctypeName(self):
        self.throwsWithLatin1([["Doctype", "\u0101"]])

    def testDoctypePublicId(self):
        self.throwsWithLatin1([["Doctype", "potato", "\u0101"]])

    def testDoctypeSystemId(self):
        self.throwsWithLatin1([["Doctype", "potato", "potato", "\u0101"]])

    def testCdataCharacters(self):
        runSerializerTest([["StartTag", "http://www.w3.org/1999/xhtml", "style", {}], ["Characters", "\u0101"]],
                          ["<style>&amacr;"], {"encoding": "iso-8859-1"})

    def testCharacters(self):
        runSerializerTest([["Characters", "\u0101"]],
                          ["&amacr;"], {"encoding": "iso-8859-1"})

    def testStartTagName(self):
        self.throwsWithLatin1([["StartTag", "http://www.w3.org/1999/xhtml", "\u0101", []]])

    def testEmptyTagName(self):
        self.throwsWithLatin1([["EmptyTag", "http://www.w3.org/1999/xhtml", "\u0101", []]])

    def testAttributeName(self):
        self.throwsWithLatin1([["StartTag", "http://www.w3.org/1999/xhtml", "span", [{"namespace": None, "name": "\u0101", "value": "potato"}]]])

    def testAttributeValue(self):
        runSerializerTest([["StartTag", "http://www.w3.org/1999/xhtml", "span",
                            [{"namespace": None, "name": "potato", "value": "\u0101"}]]],
                          ["<span potato=&amacr;>"], {"encoding": "iso-8859-1"})

    def testEndTagName(self):
        self.throwsWithLatin1([["EndTag", "http://www.w3.org/1999/xhtml", "\u0101"]])

    def testComment(self):
        self.throwsWithLatin1([["Comment", "\u0101"]])


if "lxml" in optionals_loaded:
    class LxmlTestCase(unittest.TestCase):
        def setUp(self):
            self.parser = etree.XMLParser(resolve_entities=False)
            self.treewalker = html5lib.getTreeWalker("lxml")
            self.serializer = HTMLSerializer()

        def testEntityReplacement(self):
            doc = """<!DOCTYPE html SYSTEM "about:legacy-compat"><html>&beta;</html>"""
            tree = etree.fromstring(doc, parser=self.parser).getroottree()
            result = serialize(tree, tree="lxml", omit_optional_tags=False)
            self.assertEqual("""<!DOCTYPE html SYSTEM "about:legacy-compat"><html>\u03B2</html>""", result)

        def testEntityXML(self):
            doc = """<!DOCTYPE html SYSTEM "about:legacy-compat"><html>&gt;</html>"""
            tree = etree.fromstring(doc, parser=self.parser).getroottree()
            result = serialize(tree, tree="lxml", omit_optional_tags=False)
            self.assertEqual("""<!DOCTYPE html SYSTEM "about:legacy-compat"><html>&gt;</html>""", result)

        def testEntityNoResolve(self):
            doc = """<!DOCTYPE html SYSTEM "about:legacy-compat"><html>&beta;</html>"""
            tree = etree.fromstring(doc, parser=self.parser).getroottree()
            result = serialize(tree, tree="lxml", omit_optional_tags=False,
                                          resolve_entities=False)
            self.assertEqual("""<!DOCTYPE html SYSTEM "about:legacy-compat"><html>&beta;</html>""", result)


def test_serializer():
    for filename in get_data_files('serializer', '*.test'):
        with open(filename) as fp:
            tests = json.load(fp)
            for index, test in enumerate(tests['tests']):
                yield runSerializerTest, test["input"], test["expected"], test.get("options", {})


def test_roundtrip():
    files = get_data_files('tree-construction')
    for filename in files:
        testName = os.path.basename(filename).replace(".dat", "")
        if testName in ("template",):
            continue

        tests = TestData(filename, "data")

        for index, test in enumerate(tests):
            (input, errors, innerHTML, expected) = [test[key] for key in ("data", "errors",
                                                                          "document-fragment",
                                                                          "document")]
            if innerHTML:
                continue
            yield runRoundtripTest, input, {}
