import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser

from intranett.policy.tests import layer


def get_browser(layer, loggedIn=True):
    browser = Browser(layer['app'])
    if loggedIn:
        auth = 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD)
        browser.addHeader('Authorization', auth)
    return browser


class MigrateHelper(object):

    layer = None

    @property
    def portal(self):
        return self.layer['portal']

    @property
    def folder(self):
        return self.layer['portal']['test-folder']

    def loginAsPortalOwner(self):
        from plone.app.testing import setRoles as sr
        sr(self.layer['portal'], TEST_USER_ID, ['Manager'])


class IntranettTestCase(unittest.TestCase, MigrateHelper):

    layer = layer.INTRANETT_INTEGRATION


class IntranettFunctionalTestCase(unittest.TestCase, MigrateHelper):

    layer = layer.INTRANETT_FUNCTIONAL
