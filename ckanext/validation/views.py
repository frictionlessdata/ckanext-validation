# encoding: utf-8

from flask import Blueprint

from ckantoolkit import (
    c, NotAuthorized, ObjectNotFound,
    abort, _, render, get_action)

validation = Blueprint("service_proxy", __name__)


def validation_read(self, id, resource_id):

    try:
        validation = get_action(u'resource_validation_show')(
            {u'user': c.user},
            {u'resource_id': resource_id})

        resource = get_action(u'resource_show')(
            {u'user': c.user},
            {u'id': resource_id})

        dataset = get_action(u'package_show')(
            {u'user': c.user},
            {u'id': resource[u'package_id']})

        # Needed for core resource templates
        c.package = c.pkg_dict = dataset
        c.resource = resource

        return render(u'validation/validation_read.html', extra_vars={
            u'validation': validation,
            u'resource': resource,
            u'dataset': dataset,
        })

    except NotAuthorized:
        abort(403, _(u'Unauthorized to read this validation report'))
    except ObjectNotFound:

        abort(404, _(u'No validation report exists for this resource'))


validation.add_url_rule(
    '/dataset/{id}/resource/{resource_id}/validation',
    view_func=validation_read
)
