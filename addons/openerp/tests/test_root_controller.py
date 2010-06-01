from openerp.utils import rpc
from openobject.test import TestCase


class RootTest(TestCase):

    def test_index(self):
        self.getPage("/")
        self.assertStatus(200)

    def test_about(self):
        self.getPage("/about")
        self.assertStatus(200)

    def test_menu(self):
        self.getPage("/menu")
        self.assertStatus(200)
        self.assertInBody("new TreeGrid")
