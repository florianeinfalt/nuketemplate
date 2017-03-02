# nuketemplate py.test configuration
import os
import json
import pytest

from collections import deque

from nuketemplate.template import AbstractTemplate


@pytest.fixture(scope='session')
def nuke():
    import nuke
    return nuke


@pytest.fixture(scope='session')
def api_():
    with open('{0}/{1}/api.json'.format(os.path.dirname(__file__),
                                        'test_template'), 'r') as fp:
        return json.load(fp)


@pytest.fixture(scope='session')
def uuid_():
    with open('{0}/{1}/uuid.json'.format(os.path.dirname(__file__),
                                         'test_template'), 'r') as fp:
        return json.load(fp)


@pytest.fixture(scope='session')
def template_data(api_, uuid_):
    data = {'components': ['background', 'shadow', 'lights', 'windows'],
            'options': ['base', 'grade', 'wheel'],
            'api_data': api_['options'],
            'uuid': uuid_}
    return data


@pytest.fixture(scope='session')
def template(template_data):
    template = AbstractTemplate(root='{0}/{1}'.format(
                                os.path.dirname(__file__),
                                'test_template'))
    return template


@pytest.fixture(scope='session')
def node_types():
    types = deque([
        ('Write', [('file_type', 'png'),
                   ('datatype', '8 bit'),
                   ('colorspace', 'sRGB')]),
        ('Premult', [('disable', True)]),
        ('Shuffle', []),
        ('Merge2', [('operation', 'under')]),
        ('Merge2', [('operation', 'under')]),
        ('Merge2', [('operation', 'over')]),
        ('Merge2', [('operation', 'over')]),
        ('Premult', []),
        ('NoOp', []),
        ('Unpremult', []),
        ('Merge2', [('operation', 'under'),
                    ('also_merge', 'all')]),
        ('Merge2', [('operation', 'under'),
                    ('also_merge', 'all')]),
        ('Merge2', [('operation', 'under'),
                    ('also_merge', 'all')])
    ])
    return types
