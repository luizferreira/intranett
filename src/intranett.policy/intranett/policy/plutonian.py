from Products.GenericSetup.interfaces import EXTENSION
from Products.GenericSetup.registry import _profile_registry
from Products.GenericSetup.registry import _import_step_registry
from Products.GenericSetup.zcml import _import_step_regs
import venusian
from zope.dottedname.resolve import resolve


class Configurator(object):

    def __init__(self, package):
        self.package_name, self.package = self.maybe_dotted(package)

    def scan(self, package=None, categories=('plutonian', )):
        if package is None:
            package = self.package
        scanner = venusian.Scanner(config=self)
        scanner.scan(package, categories=categories)

    def maybe_dotted(self, package):
        if isinstance(package, basestring):
            name = package
            package = resolve(name)
        else:
            name = package.__name__
        return (name, package)

    def add_import_step(self, name, handler, depends):
        _import_step_regs.append(name)
        _import_step_registry.registerStep(name, handler=handler,
            dependencies=depends, title=name)

    def register_profile(self, package_name=None, name='default'):
        if package_name is None:
            package_name = self.package_name
        title = '%s:%s' % (package_name, name)
        _profile_registry.registerProfile(name, title, description=u'',
            path='profiles/%s' % name, product=package_name,
            profile_type=EXTENSION)


class import_step(object):

    def __init__(self, depends=('toolset', 'types', 'workflow')):
        self.depends = depends

    def register(self, scanner, name, wrapped):
        config = scanner.config
        name = wrapped.__module__ + name
        config.add_import_step(name, wrapped, self.depends)

    def __call__(self, wrapped):
        venusian.attach(wrapped, self.register, category='plutonian')
        return wrapped
