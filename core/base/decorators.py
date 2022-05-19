from django.apps import apps


def get_model(funcion_parametro):
    def funcion_interior(*args, **kwargs):
        self = args[0]
        if self.model is None:
            if self.model_str is not None:
                self.model_str = str(self.model_str)

            _model_str = self.model_str.split(sep=".", maxsplit=2)

            self.model = apps.get_model(_model_str[0], _model_str[1])

        return funcion_parametro(*args, **kwargs)

    return funcion_interior
