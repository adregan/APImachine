''' Utility for making patch requests.
'''

class Patchy(object):
    def __init__(self, patch_requests):
        self.patch_requests = patch_requests
        # Turns patch_requests into a list if they aren't already
        if not isinstance(self.patch_requests, (list)):
            self.patch_requests = [self.patch_requests]

    def validate(self):
        key_errors = self._validate_patch_keys()
        print(key_errors)
        return None

    def _validate_patch_keys(self):
        op_errors = [
            {'index': i + 1, 'error': 'missing key `op`'}
            for i, request in enumerate(self.patch_requests)
            if 'op' not in request.keys()
        ]
        path_errors = [
            {'index': i + 1, 'error': 'missing key `path`'}
            for i, request in enumerate(self.patch_requests)
            if 'path' not in request.keys()
        ]
        value_errors = [
            {'index': i + 1, 'error': 'missing key `value`'}
            for i, request in enumerate(self.patch_requests)
            if 'value' not in request.keys()
        ]

        combined_errors = op_errors + path_errors + value_errors

        key_errors = self._build_error_messages(combined_errors)

        return key_errors

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
