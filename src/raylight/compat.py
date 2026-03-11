from __future__ import annotations


def patch_comfy_model_config_pickle() -> bool:
    try:
        import comfy.supported_models_base as supported_models_base
    except Exception:
        return False

    base_cls = supported_models_base.BASE
    if getattr(base_cls, "_raylight_pickle_patch", False):
        return True

    original_getattr = getattr(base_cls, "__getattr__", None)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

    if original_getattr is not None:
        def _patched_getattr(self, name):
            if name.startswith("__") and name.endswith("__"):
                raise AttributeError(name)
            return original_getattr(self, name)

        base_cls.__getattr__ = _patched_getattr

    if "__getstate__" not in base_cls.__dict__:
        base_cls.__getstate__ = __getstate__
    if "__setstate__" not in base_cls.__dict__:
        base_cls.__setstate__ = __setstate__

    base_cls._raylight_pickle_patch = True
    return True
