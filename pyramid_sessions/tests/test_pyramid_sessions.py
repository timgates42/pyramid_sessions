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
    def _makeOne(self, request, **kw):
        from pyramid.session import SignedCookieSessionFactory
        kw.setdefault('secret', 'secret')
        return SignedCookieSessionFactory(**kw)(request)

    def setUp(self):
        self.request = testing.DummyRequest()
        #self.request = Request({})
        self.config = testing.setUp(request=self.request)

    def test_includeme(self):
        self.config.include('pyramid_sessions')

    def test_add_session_factory(self):
        self.test_includeme()
        session1 = 'session1'
        session2 = 'session2'
        sec = 'secret'
        self.config.add_session_factory('session1', 
                SignedCookieSessionFactory(sec, cookie_name='session1'))
        self.config.add_session_factory('session2',
                SignedCookieSessionFactory(sec, cookie_name='session2'))

    def tearDown(self):
        testing.tearDown()

class Test_sessions(unittest.TestCase):

    def setUp(self):
        from webtest import TestApp
        from pyramid_sessions.tests import main_test_app
        self.test_app = TestApp(main_test_app({}))

    def test_get_session(self):
        from pyramid_sessions.tests import TEST_SESSIONS
        for i in TEST_SESSIONS:
            try:
                self.test_app.get('/'+i, status=200)
            except Exception as e:
                raise self.failureException(e)

    def test_set_session_value(self):
        from pyramid_sessions.tests import TEST_SESSIONS
        for id in TEST_SESSIONS:
            try:
                self.test_app.get('/set/'+id, status=200)
            except Exception as e:
                raise self.failureException(e)

    def test_get_session_value(self):
        self.test_set_session_value()
        from pyramid_sessions.tests import TEST_SESSIONS
        for id in TEST_SESSIONS:
            try:
                res = self.test_app.get('/get/'+id, status=200)
                self.assertEqual(res.body, id.encode())
            except Exception as e:
                raise self.failureException(e)
        
# vim:set ts=4 sts=4 sw=4 et tw=79:
