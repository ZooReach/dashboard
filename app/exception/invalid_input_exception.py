class InvalidInput(Exception):
    status_code = 500

    def __init__(self, description):
        Exception.__init__(self)
        self.description = description

    def to_dict(self):
        rv = dict()
        rv['description'] = self.description
        return rv