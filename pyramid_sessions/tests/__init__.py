# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory

TEST_SESSIONS = ('session1', 'session2', 'session3', 'session4')

def main_test_app(global_config, **settings):
    """Test app for pyramid_sessions testing.
    """
    config = Configurator(settings=settings)
    config.add_route('sessions', '/{session}')
    config.add_route('set_sessions', '/set/{session}')
    config.add_route('get_sessions', '/get/{session}')
    config.add_view(view_test_session, route_name='sessions')
    config.add_view(view_test_set_session, route_name='set_sessions')
    config.add_view(view_test_get_session, route_name='get_sessions')
    #_setup = settings.setdefault('_setup', True)
    #if _setup is False:
    #    return config.make_wsgi_app()
    config.include('pyramid_sessions')
    for i in TEST_SESSIONS:
        config.add_session_factory(i,
            SignedCookieSessionFactory('secret', cookie_name=i))
    config.add_session_factory('default',
            SignedCookieSessionFactory('secret', cookie_name='default'),
            default=True)
    return config.make_wsgi_app()

def view_test_session(request):
    session_id = request.matchdict['session']
    session = request.sessions.get(session_id)
    return Response()

def view_test_set_session(request):
    session_id = request.matchdict['session']
    session = request.sessions.get(session_id)
    session['state'] = session_id
    return Response()

def view_test_get_session(request):
    session_id = request.matchdict['session']
    if session_id == 'default':
        session = request.sessions.get()
    else:
        session = request.sessions.get(session_id)
    return Response(session['state'])

# vim:set ts=4 sts=4 sw=4 et tw=79: 
