import time
from marshmallow import fields
from marshmallow.exceptions import ValidationError


class SelfNestedField(fields.Field):
    """A field to make namespaced schemas. It allows to have
    a field whose contents are the dump of the same object with
    other schema"""

    # Required because the target attribute will probably not exist
    _CHECK_ATTRIBUTE = False

    def __init__(self, target_schema, *args, **kwargs):
        self.target_schema = target_schema
        super(SelfNestedField, self).__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj):
        ret, errors = self.target_schema.dump(obj)
        if errors:
            raise ValidationError(errors, data=ret)
        return ret


class JSTimestampField(fields.Field):
    """A field to serialize datetime objects into javascript
    compatible timestamps (like time.time()) * 1000"""

    def _serialize(self, value, attr, obj):
        if value is not None:
            return int(time.mktime(value.timetuple()) * 1000)