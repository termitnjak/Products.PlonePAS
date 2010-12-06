import unittest

from Products.CMFCore.utils import getToolByName

from OFS.Image import Image
from Products.PloneTestCase.ptc import default_user
from Products.PlonePAS.interfaces.plugins import IPortraitManagerPlugin
from Products.PlonePAS.tests import base
from Products.PlonePAS.tests import dummy


class PortraitsTest(base.TestCase):

    def afterSetUp(self):
        self.memberdata = self.portal.portal_memberdata
        self.membership = self.portal.portal_membership
        self.pas=getToolByName(self.portal, "acl_users")
        for plugin in self.pas.plugins.getAllPlugins('IPortraitManagerPlugin')['active']:
            if plugin!='portraits':
                self.pas.plugins.deactivatePlugin(IPortraitManagerPlugin, plugin)

    def testPluginActivated(self):
        plugins = self.pas.plugins.getAllPlugins('IPortraitManagerPlugin')['active']
        self.assertEqual(plugins, ('portraits',))
        
    def test_setPortrait(self):
        plugin = self.pas['portraits']
        self.assertEqual(len(plugin.portraits), 0)
        plugin.setPortrait(Image(id=default_user, file=dummy.File(), title=''), default_user)
        self.assertEqual(plugin.getPortrait(default_user).getId(), default_user)
        self.assertEqual(plugin._getPortrait(default_user).meta_type, 'Image')
        self.assertEqual(len(plugin.portraits), 1)
        
    def testDeletePortrait(self):
        plugin = self.pas['portraits']
        self.assertEqual(len(plugin.portraits), 0)
        plugin.setPortrait(Image(id=default_user, file=dummy.File(), title=''), default_user)
        self.assertEqual(len(plugin.portraits), 1)
        plugin.deletePortrait(default_user)
        self.assertEqual(len(plugin.portraits), 0)
        self.assertEqual(plugin.getPortrait(default_user), None)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PortraitsTest))
    return suite
