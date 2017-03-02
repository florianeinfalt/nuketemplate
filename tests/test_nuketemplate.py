# nuketemplate tests
import os
import nuke
import pytest

from nuketemplate.build import NukeGraphBuilder
from nuketemplate.convert import AbstractTemplateConverter
from nuketemplate.exceptions import AbstractTemplateError


def test_template_invalid(template):
    with pytest.raises(AbstractTemplateError):
        template.save()


def test_template(template, template_data):
    template.render(**template_data)
    assert len(template.template) == 9
    assert all([isinstance(temp, dict) for temp in template.template])


def test_template_save(template, tmpdir):
    filename = '{0}/template.json'.format(tmpdir)
    template.save(filename=filename)
    assert os.path.isfile(filename)


@pytest.fixture(scope='module')
def converter(template):
    converter = AbstractTemplateConverter(template.template)
    return converter


def test_converter(converter):
    converter.convert()


def test_converter_to_png(converter, tmpdir):
    filename = '{0}/graph.png'.format(tmpdir)
    dot_filename = '{0}/graph.dot'.format(tmpdir)
    converter.to_png(filename)
    assert os.path.isfile(dot_filename)
    assert os.path.isfile(filename)


def test_builder(converter):
    builder = NukeGraphBuilder(converter.result)
    assert builder.build() == 69


def test_nodes(node_types):
    def check_upstream_type(node):
        if node_types:
            upstream_node = node_types.popleft()
            assert node.Class() == upstream_node[0]
            for attr, value in upstream_node[1]:
                assert node[attr].value() == value
            return check_upstream_type(node.input(0))
        else:
            return
    check_upstream_type(nuke.toNode('__render__'))
