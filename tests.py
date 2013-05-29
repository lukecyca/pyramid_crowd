import unittest
from mock import patch
from pyramid_crowd import CrowdAuthenticationPolicy
from pyramid.testing import DummyRequest
from pyramid.security import Everyone, Authenticated


class CrowdAuthenticationPolicyTests(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('pyramid_crowd.CrowdServer')
        MockCrowd = self.patcher.start()
        self.crowd = MockCrowd.return_value
        self.crowd.auth_ping.return_value = True

    def tearDown(self):
        self.patcher.stop()

    def test_init(self):
        authn = CrowdAuthenticationPolicy()
        self.assertIs(authn.crowd, self.crowd)

    def test_authenticated_userid_none(self):
        """User does not have any cookie"""
        request = DummyRequest()
        authn = CrowdAuthenticationPolicy()
        self.assertIsNone(authn.authenticated_userid(request))
        self.assertIsNone(authn.unauthenticated_userid(request))

    def test_authenticated_userid_invalid(self):
        """User has an invalid cookie"""
        self.crowd.validate_session.return_value = None

        request = DummyRequest()
        request.cookies['crowd.token_key'] = 'crackedkey'
        request.remote_addr = '127.0.0.1'

        authn = CrowdAuthenticationPolicy()
        self.assertIsNone(authn.authenticated_userid(request))
        self.assertIsNone(authn.unauthenticated_userid(request))

    def test_authenticated_userid(self):
        """User has a valid cookie"""
        self.crowd.validate_session.return_value = {
            'user': {
                'active': True,
                'name': 'luke',
            }
        }

        request = DummyRequest()
        request.cookies['crowd.token_key'] = 'legitkey'
        request.remote_addr = '127.0.0.1'

        authn = CrowdAuthenticationPolicy()
        self.assertEquals(authn.authenticated_userid(request), 'luke')
        self.assertEquals(authn.unauthenticated_userid(request), 'luke')

    def test_effective_principals_none(self):
        """User does not have any cookie"""
        request = DummyRequest()
        authn = CrowdAuthenticationPolicy()
        self.assertEquals(
            set(authn.effective_principals(request)),
            set([Everyone])
        )

    def test_effective_principals_no_groups(self):
        """User has a valid cookie, but is not in any groups"""
        self.crowd.validate_session.return_value = {
            'user': {
                'active': True,
                'name': 'luke',
            }
        }
        self.crowd.get_groups.return_value = []

        request = DummyRequest()
        request.cookies['crowd.token_key'] = 'legitkey'
        request.remote_addr = '127.0.0.1'

        authn = CrowdAuthenticationPolicy()
        self.assertEquals(
            set(authn.effective_principals(request)),
            set(['luke', Authenticated, Everyone])
        )

    def test_effective_principals(self):
        """User has a valid cookie, and is in some groups"""
        self.crowd.validate_session.return_value = {
            'user': {
                'active': True,
                'name': 'luke',
            }
        }
        self.crowd.get_groups.return_value = ['admin', 'employees']

        request = DummyRequest()
        request.cookies['crowd.token_key'] = 'legitkey'
        request.remote_addr = '127.0.0.1'

        authn = CrowdAuthenticationPolicy()
        self.assertEquals(
            set(authn.effective_principals(request)),
            set(['luke', 'group:admin', 'group:employees', Authenticated, Everyone])
        )
