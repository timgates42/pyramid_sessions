# -*- coding: utf-8 -*-

"""
test_pyramid_sessions
----------------------------------

Tests for `pyramid_sessions` module.
"""
import unittest

from pyramid import testing
from pyramid.request import Request
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory
from pyramid.threadlocal import get_current_request

class Test_config(unittest.TestCase):
    def _makeOne(self, **kw):
        from pyramid.session import SignedCookieSessionFactory
        kw.setdefault('secret', 'secret')
        return SignedCookieSessionFactory(**kw)

    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)

    def test_includeme(self):
        self.config.include('pyramid_sessions')

    def test_add_session_factory(self):
        self.test_includeme()
        from pyramid_sessions.tests import TEST_SESSIONS
        for i in TEST_SESSIONS:
            self.config.add_session_factory(i, self._makeOne(cookie_name=i))

    def test_remove_session_factory(self):
        from pyramid_sessions.tests import TEST_SESSIONS
        from pyramid_sessions import ISessionManager
        self.test_add_session_factory()
        sm = self.config.registry.queryUtility(ISessionManager)
        for i in TEST_SESSIONS:
            sm.remove(i)

    def test_default_session(self):
        from pyramid_sessions import ISessionManager
        self.test_includeme()
        self.config.add_session_factory(id, self._makeOne(cookie_name=id),
            default=True)
        sm = self.config.registry.queryUtility(ISessionManager)
        sm(self.request).get()

    def test_invalid_default_session(self):
        from pyramid_sessions import ISessionManager
        self.test_includeme()
        sm = self.config.registry.queryUtility(ISessionManager)
        self.assertRaises(AttributeError, sm(self.request).get)

    def tearDown(self):
        testing.tearDown()


class Test_web_sessions(unittest.TestCase):

    def setUp(self):
        from webtest import TestApp
        from pyramid_sessions.tests import main_test_app
        self.test_app = TestApp(main_test_app({}))

    def test_get_session(self):
        from pyramid_sessions.tests import TEST_SESSIONS
        for i in TEST_SESSIONS:
            self.test_app.get('/'+i, status=200)

    def test_set_session_value(self):
        from pyramid_sessions.tests import TEST_SESSIONS
        for id in TEST_SESSIONS:
            self.test_app.get('/set/'+id, status=200)

    def test_get_session_value(self):
        self.test_set_session_value()
        from pyramid_sessions.tests import TEST_SESSIONS
        for id in TEST_SESSIONS:
            res = self.test_app.get('/get/'+id, status=200)
            self.assertEqual(res.body, id.encode())

    def test_get_default_session(self):
        id='default'
        self.test_app.get('/set/'+id, status=200)
        res = self.test_app.get('/get/'+id, status=200)
        self.assertEqual(res.body, id.encode())

    def test_get_invalid_session(self):
        id='invalid'
        self.assertRaises(KeyError, self.test_app.get, '/get/'+id, 
            status=200)

# vim:set ts=4 sts=4 sw=4 et tw=79:
