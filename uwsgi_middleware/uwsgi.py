# Copyright 2021 SAP SE
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import uwsgi
import webob.dec

from oslo_middleware import base
from oslo_middleware.request_id import ENV_REQUEST_ID, GLOBAL_REQ_ID


class Uwsgi(base.ConfigurableMiddleware):
    """Middleware that populates uwsgi variables with openstack request-ids and keystone informations."""

    @webob.dec.wsgify
    def __call__(self, req):
        req_id = req.environ.get(ENV_REQUEST_ID, '-')
        global_req_id = req.environ.get(GLOBAL_REQ_ID, '-')

        proj_id = req.environ.get('HTTP_X_PROJECT_NAME', req.environ.get('HTTP_X_PROJECT_ID', '-'))
        user_id = req.environ.get('HTTP_X_USER_NAME', req.environ.get('HTTP_X_USER_ID', '-'))
        user_project_id = req.environ.get('HTTP_X_USER_DOMAIN_NAME', req.environ.get('HTTP_X_USER_DOMAIN_ID', '-'))

        uwsgi.set_logvar('request_id', req_id)
        uwsgi.set_logvar('global_request_id', global_req_id)
        uwsgi.set_logvar('user_id', user_id),
        uwsgi.set_logvar('user_project_id', user_project_id)
        uwsgi.set_logvar('project_id', proj_id)
        return req.get_response(self.application)