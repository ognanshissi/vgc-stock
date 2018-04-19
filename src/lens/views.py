from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, FormView
from account.models import Profile
from .models import Stock, Product, Type, Entry, Exit
from .mixins import LensListViewMixin
from .forms import ProductForm, EntryForm, TypeForm, ExitForm


class StockListView(ListView):
    template_name = 'lens/index.html'
    context_object_name = 'all_stock'

    def get_context_data(self, *args, **kwargs):
        context = super(StockListView, self).get_context_data(*args, **kwargs)
        lens_type_list = [value for key, value in Product.LENS_TYPE_CHOICES]
        qs_sphere = Product.objects.values("sphere").distinct().order_by("sphere")
        qs_cylindre = Product.objects.values("cylindre").distinct().order_by("cylindre")

        context['sphere_list'] = qs_sphere
        context['cylindre_list'] = qs_cylindre
        print(context['cylindre_list'])
        context['type_list'] = lens_type_list
        return context

    def get_queryset(self):
        lens_type = self.request.GET.get('lens_type')

        if lens_type and lens_type != 'tous':
            qs = Stock.objects.filter(product__type__name__iexact=lens_type)
        else:
            qs = Stock.objects.all()
        return qs


class TypeListView(ListView):
    template_name = 'lens/types/index.html'
    queryset = Type.objects.all()


class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm
    template_name = 'lens/types/create.html'


class EntryListView(ListView):
    template_name = 'lens/entry/index.html'
    queryset = Entry.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(EntryListView, self).get_context_data(*args, **kwargs)
        lens_type_list = [value for key, value in Product.LENS_TYPE_CHOICES]
        context['type_list'] = lens_type_list
        return context

    def get_queryset(self):
        lens_type = self.request.GET.get('lens_type')

        if lens_type and lens_type != 'tous':
            qs = Entry.objects.filter(product__type__name__iexact=lens_type)
        else:
            qs = Entry.objects.all()
        return qs


class EntryCreateView(View):
    template_name = 'lens/entry/create.html'
    form = EntryForm()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        form = EntryForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            qs = Profile.objects.filter(user=request.user)
            if qs.exists() and qs.count() == 1:
                profile = qs.first()
                instance.provider = profile
            instance.save()
            print(instance)
            return redirect(reverse_lazy('lens:stock'))


class ExitListView(ListView):
    template_name = 'lens/exit/index.html'
    queryset = Exit.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ExitListView, self).get_context_data(*args, **kwargs)
        lens_type_list = [value for key, value in Product.LENS_TYPE_CHOICES]
        context['type_list'] = lens_type_list
        return context

    def get_queryset(self):
        lens_type = self.request.GET.get('lens_type')

        if lens_type and lens_type != 'tous':
            qs = Exit.objects.filter(product__type__name__iexact=lens_type).order_by('-pk')
        else:
            qs = Exit.objects.all().order_by('-pk')
        return qs


class ExitCreateView(FormView):
    template_name = 'lens/exit/create.html'
    form_class = ExitForm
    success_url = reverse_lazy('lens:exit-list')

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {'form': self.form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = ExitForm(request.POST)
    #     print(form)
    #     return redirect(reverse_lazy('lens:exit-create'))

    def form_valid(self, form):
        opts = {
            'request': self.request
        }
        form.save(**opts)
        return super(ExitCreateView, self).form_valid(form)


class ProductListView(ListView):
    template_name = 'lens/product/index.html'
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        lens_type_list = [value for key, value in Product.LENS_TYPE_CHOICES]
        context['type_list'] = lens_type_list
        return context

    def get_queryset(self):
        lens_type = self.request.GET.get('lens_type')

        if lens_type and lens_type != 'tous':
            qs = Product.objects.filter(type__name__iexact=lens_type)
        else:
            qs = Product.objects.all()
        return qs


class ProductCreateView(View):
    template_name = 'lens/product/create.html'
    form_class = ProductForm()
    context = {
        'form': form_class
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form_class = ProductForm(request.POST)
        if form_class.is_valid:
            instance = form_class.save(commit=False)
            # instance.provider = request.user
            instance.save()
            return redirect(reverse_lazy('lens:product-list'))


class SearchStockListView(ListView):
    template_name = 'lens/index.html'
    queryset = Product.objects.all()

    def get_queryset(self):
        print(self.kwargs)
        return Stock.objects.all()
