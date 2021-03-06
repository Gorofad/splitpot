#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys

sys.path.append('controller/')
sys.path.append('utils/')
from User import *

from DatabaseParser import *


class TestDatabaseParser(unittest.TestCase):

    def setUp(self):
        """
        Called before *each* testcase. We want to operate on a fresh database
        """

        clear()

    def testRegister(self):  # just check if we don't get an runtime error
        register()
        self.assertTrue(True)

    def testForgot(self):  # just check if we don't get a an runtime error
        forgot()
        self.assertTrue(True)

    def testDoRegister_MissingData(self):  # TODO check actual output / that no mail is sent
        doRegister('user@blub.de')
        self.assertFalse(userExists('user@blub.de'))
        doRegister('user@blub.de', 'a')  # nick too short
        self.assertFalse(userExists('user@blub.de'))
        doRegister('user@bla.de', 'user', '1')
        self.assertFalse(userExists('user@bla.de'))
        doRegister('user@bla.de', 'user', '1', '1')  # pwd too short
        self.assertFalse(userExists('user@bla.de'))
        doRegister('user@bla.de', 'user', '123456', '123455')  # wrong pwd repition
        self.assertFalse(userExists('user@bla.de'))

    def testDoRegister(self):
        doRegister('user@blub.de', '123456', '123456')
        self.assertFalse(userExists('user@blub.de'))


  # TODO test requestForgot
  # TODO test doForgot

if __name__ == '__main__':
    unittest.main()
