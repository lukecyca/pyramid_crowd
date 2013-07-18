from zope.interface import implementer
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Everyone, Authenticated
from crowd import CrowdServer

import logging
logger = logging.getLogger(__name__)


@implementer(IAuthenticationPolicy)
class CrowdAuthenticationPolicy(object):

    def __init__(self,
                 crowd_uri='https://crowd.example.com',
                 app_name='MyApp',
                 app_pass='Password',
                 cookie_name='crowd.token_key',
                 cookie_domain='.example.com',
                 cookie_path='/',
                 cookie_secure=True):

        self.crowd_uri = crowd_uri
        self.app_name = app_name
        self.app_pass = app_pass
        self.cookie_name = cookie_name
        self.cookie_domain = cookie_domain
        self.cookie_path = cookie_path
        self.cookie_secure = cookie_secure

        # Connect to crowd server
        self.crowd = CrowdServer(crowd_uri, app_name, app_pass)
        if self.crowd.auth_ping():
            logger.info("Established communication to Crowd server")

        else:
            logger.error("Could not establish communication to Crowd server")

    def authenticated_userid(self, request):
        token = request.cookies.get(self.cookie_name)
        if token:
            user_data = self.crowd.validate_session(token, request.remote_addr)
            if user_data:
                if user_data['user']['active']:
                    return user_data['user']['name']

                else:
                    logger.warning("User {0} is not active".format(user_data['user']['name']))

            else:
                logger.warning("Crowd SSO failed for {0}".format(request.remote_addr))

        # Crowd SSO failed
        return None

    def unauthenticated_userid(self, request):
        return self.authenticated_userid(request)

    def effective_principals(self, request):
        princs = [Everyone]

        username = self.authenticated_userid(request)
        if username:
            princs.extend([Authenticated, username])
            princs.extend(
                ['group:' + g for g in self.crowd.get_groups(username)]
            )

        return princs

    def _get_cookie(self, value, expired=False):
        cookie = '{}="{}"; Path={}; Domain={}'.format(
            self.cookie_name,
            value,
            self.cookie_path,
            self.cookie_domain,
        )

        if self.cookie_secure:
            cookie += '; Secure'

        if expired:
            cookie += '; Max-Age=0; Expires=Wed, 31-Dec-97 23:59:59 GMT'

        return cookie

    def remember(self, request, principal, password='', **kw):
        user_data = self.crowd.authenticate(principal, password, request.remote_addr)
        if user_data:
            logger.info("{0} logged in via password".format(principal))
            return [('Set-Cookie', self._get_cookie(user_data['token']))]

    def forget(self, request):
        token = request.cookies.get(self.cookie_name)
        if token:
            self.crowd.terminate_session(token)

        return [('Set-Cookie', self._get_cookie('', expired=True))]
