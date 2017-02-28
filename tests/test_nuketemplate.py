# nuketemplate tests
from nuketemplate.convert import AbstractTemplateConverter


def test_template(template, template_data):
    template.render(**template_data)
    assert len(template.template) == 9
    assert all([isinstance(temp, dict) for temp in template.template])


def test_converter(template):
    converter = AbstractTemplateConverter(template.template)
    converter.convert()


def test_builder(converter):
    pass
