# -*- coding: utf-8 -*-

from zope.interface import Interface

class SessionManager(object):
    def __init__(self, *args, **kwargs):
        self.sessions = {}
        self._default_session = None

    def __call__(self, request):
        self.request = request
        return self

    def _init_factory(self, factory):
        """Initialize the factory with the request."""
        return factory(self.request)

    @property
    def default_session(self):
        if self._default_session is None:
            raise AttributeError('A default session is not set.')
        return self._default_session

    def add(self, name, session, default=False):
        """
        Add a session factory to the `default` is optional (look into adding
        this to the default `request.session` in the future)
        """
        self.sessions[name] = session
        if default:
            self._default_session = session

    def get(self, name=None):
        """
        Return session factory object if found. Returns the default session
        if `name` is ommitted.
        """
        if not name:
            return self._init_factory(self.default_session)
        elif name in self.sessions:
            return self._init_factory(self.sessions[name])
        else:
            raise KeyError('Session factory \'{0}\' does not'
                ' exist.'.format(name))

    def remove(self, name):
        """
        Remove session factory from the `sessions` dictionary store. The
        default exception will be raised if `name` (key) doesn't exist.
        """
        del self.sessions[name]
        
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
