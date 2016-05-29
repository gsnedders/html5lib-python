from __future__ import absolute_import, division, unicode_literals

import pytest

from . import support  # noqa

from html5lib.constants import namespaces


@pytest.fixture(params=support.treeTypes.items())
def treeBuilder(request):
    treeName, treeAPIs = request.param
    if treeAPIs is None:
        pytest.skip("Treebuilder not loaded")
    elif "adapter" in treeAPIs:
        pytest.skip("Tree type requires adapter")
    return treeAPIs["builder"]


def _Element(builder, local, namespace=None):
    token = {
        "name": local,
        "data": {}
    }
    if namespace is not None:
        token["namespace"] = namespace
    return builder.createElement(token)


def test_append(treeBuilder):
    # set everything up
    builder = treeBuilder(True)
    parent = _Element(builder, "div", namespaces["html"])
    child = _Element(builder, "span", namespaces["html"])
    assert parent.parent is None
    assert not parent.hasContent()
    assert child.parent is None

    # append the child
    parent.appendChild(child)
    assert parent.hasContent()
    assert child.parent == parent


def test_insertText(treeBuilder):
    # set everything up
    builder = treeBuilder(True)
    parent = _Element(builder, "div", namespaces["html"])
    assert parent.parent is None
    assert not parent.hasContent()

    # do the insertText
    parent.insertText("foo")
    assert parent.hasContent()


def test_insertText_before(treeBuilder):
    # set everything up
    builder = treeBuilder(True)
    parent = _Element(builder, "div", namespaces["html"])
    ref_child = _Element(builder, "foo", namespaces["html"])
    assert parent.parent is None
    assert not parent.hasContent()
    assert ref_child.parent is None

    # add the ref child
    parent.appendChild(ref_child)
    assert parent.hasContent()
    assert ref_child.parent == parent

    # do the insertText
    parent.insertText("bar", ref_child)
    assert parent.hasContent()
    assert ref_child.parent == parent


def test_insertBefore(treeBuilder):
    # set everything up
    builder = treeBuilder(True)
    parent = _Element(builder, "div", namespaces["html"])
    child = _Element(builder, "span", namespaces["html"])
    ref_child = _Element(builder, "foo", namespaces["html"])
    assert parent.parent is None
    assert not parent.hasContent()
    assert ref_child.parent is None
    assert child.parent is None

    # add the ref child
    parent.appendChild(ref_child)
    assert parent.hasContent()
    assert ref_child.parent == parent

    # do the insertBefore
    parent.insertBefore(child, ref_child)
    assert parent.hasContent()
    assert ref_child.parent == parent
    assert child.parent == parent


def test_removeChild(treeBuilder):
    # set everything up
    builder = treeBuilder(True)
    parent = _Element(builder, "div", namespaces["html"])
    child = _Element(builder, "span", namespaces["html"])
    assert parent.parent is None
    assert not parent.hasContent()
    assert child.parent is None

    # append the child
    parent.appendChild(child)
    assert parent.hasContent()
    assert child.parent == parent

    # and remove it
    parent.removeChild(child)
    assert not parent.hasContent()
    assert child.parent is None


def test_reparentChildren(treeBuilder):
    # set everything up
    builder = treeBuilder(True)
    parent = _Element(builder, "div", namespaces["html"])
    new_parent = _Element(builder, "div", namespaces["html"])
    child = _Element(builder, "span", namespaces["html"])
    assert not parent.hasContent()
    assert not new_parent.hasContent()

    # append the child
    parent.appendChild(child)
    assert parent.hasContent()
    assert child.parent == parent

    # and reparent
    parent.reparentChildren(new_parent)
    assert not parent.hasContent()
    assert new_parent.hasContent()
    assert child.parent == new_parent


def test_cloneNode(treeBuilder):
    # set everything up
    builder = treeBuilder(True)
    parent = _Element(builder, "div", namespaces["html"])
    child = _Element(builder, "span", namespaces["html"])
    assert not parent.hasContent()

    # append the child
    parent.appendChild(child)
    assert parent.hasContent()
    assert child.parent == parent

    # and clone the parent
    new_parent = parent.cloneNode()
    assert parent.hasContent()
    assert not new_parent.hasContent()
    assert child.parent == parent


def test_tb_constructor(treeBuilder):
    builder = treeBuilder(True)
    assert builder.defaultNamespace == namespaces["html"]
    assert builder.openElements == []
    assert builder.activeFormattingElements == []
    assert builder.headPointer is None
    assert builder.formPointer is None
    assert builder.insertFromTable == False
