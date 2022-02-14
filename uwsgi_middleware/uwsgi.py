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

import six
from oslo_log import log
from oslo_middleware import base
from oslo_middleware.request_id import ENV_REQUEST_ID, GLOBAL_REQ_ID

LOG = log.getLogger(__name__)
ENABLED = False

try:
    import uwsgi

    LOG.info("uWSGI %s detected, uwsgi-middleware activated", str(uwsgi.version))
    ENABLED = True
except ImportError:
    LOG.warning("No uWSGI environment detected, uwsgi-middleware disabled")


class Uwsgi(base.ConfigurableMiddleware):
    """Middleware that populates uwsgi variables with openstack request-ids and keystone informations."""

    def process_request(self, req):
        if not ENABLED:
            return None

        env = {
            'user_id': req.environ.get('HTTP_X_USER_ID'),
            'project': req.environ.get('HTTP_X_PROJECT_ID'),
            'domain': req.environ.get('HTTP_X_DOMAIN_ID'),
            'user_domain': req.environ.get('HTTP_X_USER_DOMAIN_ID'),
            'project_domain': req.environ.get('HTTP_X_PROJECT_DOMAIN_ID'),
            'request_id': req.environ.get(ENV_REQUEST_ID),
            'global_request_id': req.environ.get(GLOBAL_REQ_ID)
        }

        for env_var, env_val in six.iteritems(env):
            if env_val:
                uwsgi.set_logvar(env_var, env_val)

        return req.get_response(self.application)