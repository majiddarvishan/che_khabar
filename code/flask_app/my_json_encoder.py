import decimal
import flask.json

class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            # return float(obj)
            return int(obj)
        return super(MyJSONEncoder, self).default(obj)