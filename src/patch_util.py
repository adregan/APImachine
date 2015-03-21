''' Utility for making patch requests.
'''

class Patchy(object):
    def __init__(self, supported_ops=None):
        if not supported_ops:
            self.supported_ops = ['replace', 'add', 'remove']
        else:
            self.support_ops = supported_ops

    def load(self, patch_requests=[]):
        # Turns patch_requests into a list if they aren't already
        if not isinstance(patch_requests, (list)):
            self.patch_requests = [patch_requests]
        else:
            self.patch_requests = patch_requests
        return

    def validate(self):
        if not self.patch_requests:
            return {'message': 'Patch request is empty. Please send valid patch requests.'}
        key_errors = self._validate_patch_keys()
        if key_errors:
            return {'message': key_errors}
        op_errors = self._validate_ops()
        if op_errors:
            return {'message': op_errors}
        return None

    def _validate_patch_keys(self):
        op_errors = [
            {'index': i + 1, 'error': 'Missing key `op`'}
            for i, request in enumerate(self.patch_requests)
            if 'op' not in request.keys()
        ]
        path_errors = [
            {'index': i + 1, 'error': 'Missing key `path`'}
            for i, request in enumerate(self.patch_requests)
            if 'path' not in request.keys()
        ]
        value_errors = [
            {'index': i + 1, 'error': 'Missing key `value`'}
            for i, request in enumerate(self.patch_requests)
            if 'value' not in request.keys()
        ]

        combined_errors = op_errors + path_errors + value_errors

        key_errors = self._build_error_messages(combined_errors)

        return key_errors

    def _validate_ops(self):
        illegal_ops = [
            {
                'index': i + 1,
                'error': 'Unsupported op `{op}`'.format(op=request.get('op'))
            }
            for i, request in enumerate(self.patch_requests)
            if request.get('op') not in self.supported_ops
        ]

        op_errors = self._build_error_messages(illegal_ops)

        return op_errors

    def _build_error_messages(self, errors):
        def err_output(err):
            output = (
                '{error} in patch request {index} of {length}'
                .format(
                    error=err.get('error'),
                    index=err.get('index'),
                    length=len(self.patch_requests))
            )
            return output

        return [err_output(err) for err in errors]

    def clean(self):
        self.patch_requests = []

