class Controller(object):
    object = None
    model = None
    model_str = None

    def __init__(self, instance=None, model_str=None, model=None):
        self._object = None

        if instance is not None:
            self.object = instance

        if model_str is not None:
            self.model_str = model_str

        if model is not None:
            self.model = model

    def create_object(self, *args, **kwargs):
        pass

    def delete_object(self, *args, **kwargs):
        pass

    def permit_delete(self, *args, **kwargs):
        pass

    def search_data(self, *args, **kwargs):
        pass

    def update_object(self, *args, **kwargs):
        pass

    def validate_access(self, *args, **kwargs):
        pass
