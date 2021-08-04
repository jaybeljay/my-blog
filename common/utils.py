from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug


class StaffCheckMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):        
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
