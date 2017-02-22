import os
import json
import jinja2

from glob import glob

from .exceptions import AbstractTemplateError


class AbstractTemplate(object):
    def __init__(self, root=os.getcwd(), nodes='nodes', attrs='attrs'):
        self.root = root
        self.attrs = attrs
        self.nodes = nodes
        self.template = []

    def _any(self, iterable, attribute):
        """
        Custom Jinja 2 filter, return :func:`any()` on a list filtered
        by ``attribute``.

        :param iterable: Iterable
        :type iterable: iter
        :param attribute: Filter attribute
        :type attribute: str
        :return: Result of any()
        :rtype: bool
        """
        return bool(any([item for item in iterable if item[attribute]]))

    def _basename(self, fp):
        """
        Custom Jinja 2 filter returning a filename's basename.

        :param fp: Filename
        :type fp: str
        :return: Filename's basename
        :rtype: str
        """
        return os.path.basename(fp)

    def _get_loader(self, folder):
        """
        Given a ``folder`` containing Jinja2 templates, return a Jinja2 loader
        for that ``folder``.

        :param folder: Folder containing Jinja2 templates
        :type folder: str
        :return: Jinja2 loader
        :rtype: jinja2.FileSystemLoader
        """
        return jinja2.FileSystemLoader('{0}/{1}'.format(self.root,
                                                        getattr(self, folder)))

    def _get_env(self, folder):
        """
        Given a ``folder`` containing Jinja2 templates, return a Jinja2
        environment for that ``folder``.

        :param folder: Folder containing Jinja2 templates
        :type folder: str
        :return: Jinja2 environment
        :rtype: jinja2.Environment
        """
        env = jinja2.Environment(loader=self._get_loader(folder))
        env.filters['any'] = self._any
        env.filters['basename'] = self._basename
        return env

    def _get_attrs(self):
        """
        Compile and return the attribute templates

        :return: Attribute dictionary
        :rtype: dict
        """
        template = self._get_env('attrs').get_template('main.j2')
        attr_templates = glob('{0}/{1}/attrs_*.j2'.format(self.root,
                                                          self.attrs))
        render = template.render(attr_templates=attr_templates)
        try:
            return json.loads(render)
        except ValueError as e:
            print 'JSON error: {0}'.format(e)
            raise AbstractTemplateError(e)
        except jinja2.exceptions.UndefinedError as e:
            print 'Attribute error: {0}'.format(e)
            raise AbstractTemplateError(e)

    def render(self, template='main.j2', **kwargs):
        """
        Compile the main node ``template`` and store as an instance attribute

        :param template: Main template name
        :type template: str
        :param \**kwargs: Template data
        :type \**kwargs: dict
        """
        template = self._get_env('nodes').get_template(template)
        render = template.render(attrs=self._get_attrs(), **kwargs)
        try:
            self.template = json.loads(render)
        except ValueError as e:
            print 'JSON error: {0}'.format(e)
            raise AbstractTemplateError(e)
        except jinja2.exceptions.UndefinedError as e:
            print 'Attribute error: {0}'.format(e)
            raise AbstractTemplateError(e)

    def save(self, root='', name='template.json'):
        """
        Given a ``root`` folder and a ``name``, save the template JSON encoded
        to a file.

        :param root: Saving location
        :type root: str
        :param name: Filename
        :type name: str
        """
        if not self.template:
            raise AbstractTemplateError('Template does not yet exist')
        if not root:
            root = self.root
        with open('{0}/{1}'.format(root, name), 'w') as fp:
            json.dump(self.template, fp, indent=4)
