pyramid_crowd
=============

Pyramid authentication policy for [Atlassian Crowd](https://www.atlassian.com/software/crowd/) Single Sign-On (SSO)

[![Build Status](https://travis-ci.org/lukecyca/pyramid_crowd.png?branch=master)](https://travis-ci.org/lukecyca/pyramid_crowd)

Installation
------------

    pip install git+git://github.com/lukecyca/pyramid_crowd.git

Basic Usage
-----------

In the main application configuration for your pyramid app, add
`CrowdAuthenticationPolicy` as your authentication policy. Here's
an example:

    from pyramid_crowd import CrowdAuthenticationPolicy

    authn = CrowdAuthenticationPolicy(
        crowd_uri='https://crowd.example.com',
        app_name='MyApp',
        app_pass='Password',
        cookie_name='crowd.token_key',
        cookie_domain='.example.com',
        cookie_path='/',
        cookie_secure=True,
    )

    config.set_authentication_policy(authn)

Anyone accessing your app with a valid cookie called `crowd.token_key`
will now automatically be authenticated. You can call [`authenticated_userid(request)`](http://pyramid.readthedocs.org/en/latest/api/security.html#pyramid.security.authenticated_userid)
in your code and get their username, and you can call [`effective_principals(request)`](http://pyramid.readthedocs.org/en/latest/api/security.html#pyramid.security.effective_principals)
to get the full list of groups they're in.

Each group will be denoted by a principal prepended by `group:`, so a
group called `admin` would be denoted by `group:admin`.

If you are using [`ACLAuthorizationPolicy`](http://pyramid.readthedocs.org/en/latest/narr/security.html),
you can specify ACLs to assign access based on usernames and group
principals.

If you are using another Crowd-enabled apps to have users log
in and out, then this is all you need. If you want to provide login
and logout functionality in your own app, read on!


Login
-----

Users who don't already have a valid crowd token probably want to
provide a username and password in a typical login form. The handler
for that form could look like this:

    from pyramid.security import remember
    from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized

    @view_config(route_name='login', request_method='POST')
    def login(request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        headers = remember(request, username, password)
        if headers:
            return HTTPFound(location='/', headers=headers)

        else:
            return HTTPUnauthorized('Authentication Failed')

If they're successful, they will get a `crowd.token_key` cookie
which will be valid for subsequent requests to your app, as well as
all other Crowd-enabled apps.

Logout
------

You may also want to provide a _Logout_ button which POSTs to `/logout`.
The handler might look like:

    from pyramid.security import forget

    @view_config(route_name='logout', request_method='POST')
    def logout(request):
        headers = forget(request)
        return HTTPFound(location='/', headers=headers)

This will tell the Crowd server to invalidate their crowd token, and
will instruct their browser to delete the `crowd.token_key` cookie.
They will effectively be logged out of all Crowd-enabled apps.


License
-------
*BSD 2-Clause License*

Copyright (c) 2013, Luke Cyca
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.
