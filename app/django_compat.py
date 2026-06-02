from django.template.context import BaseContext


def patch_template_context_copy():
    original_copy = getattr(BaseContext.__copy__, '_shopnest_original', None)
    if original_copy is not None:
        return

    def fixed_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    fixed_copy._shopnest_original = BaseContext.__copy__
    BaseContext.__copy__ = fixed_copy
