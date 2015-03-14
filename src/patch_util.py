''' Utility for making patch requests.
'''

class Patchy(object):
    def __init__(self, patch_requests):
        self.patch_requests = patch_requests
        # Turns patch_requests into a list if they aren't already
        if not isinstance(self.patch_requests, (list)):
            self.patch_requests = [self.patch_requests]

    def validate(self):
        return None