# -*- coding: utf-8 -*-

__version__ = '0.0.1'

from .session_manager import SessionManager

from zope.interface import Interface

class ISessionManager(Interface):
    pass

def sessions(request, *args, **kwargs):
    """Fetch the SessionManager instance and attached the latest request."""
    sm = request.registry.queryUtility(ISessionManager)
    return sm(request)

def add_session_factory(config, name, factory, default=False):
    """Add a session factory to the SessionManager instance."""
    sm = config.registry.queryUtility(ISessionManager)
    sm.add(name, factory, default=default)

def includeme(config):
    """
    Pyramid specific lookup function. Add the following to your pyramid
    `main` method::
        config.include('pyramid_sessions')
    """
    config.registry.registerUtility(SessionManager(), ISessionManager)
    config.add_directive('add_session_factory', add_session_factory)
    config.add_request_method(sessions, reify=True)

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
