from .models import Product


class LensListViewMixin(object):
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        context = super(LensListViewMixin, self).get_context_data(*args, **kwargs)
        lens_type_list = [value for key, value in Product.LENS_TYPE_CHOICES]
        context['type_list'] = lens_type_list
        print(lens_type_list)
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context
