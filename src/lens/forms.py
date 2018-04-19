from django import forms
from .models import Product, Type, Entry, Stock, Exit
from account.models import Profile


class ProductForm(forms.ModelForm):

    TYPES = Type.objects.all()

    type = forms.ModelChoiceField(
        queryset=TYPES,
        empty_label="Choisissez un type de lentille",
        required=True
        )

    sphere = forms.FloatField(label="Sphere", required=False, widget=forms.NumberInput({
        'class': 'form-control'
    }))

    cylindre = forms.FloatField(label="Cylindre", required=False, widget=forms.NumberInput({
        'class': 'form-control'
    }))

    axe = forms.FloatField(label='Axe', required=False, widget=forms.NumberInput({
        'class': 'form-control',
        'placeholder': 'Ex.: 100'
    }))

    addition = forms.IntegerField(label='Addition', required=False, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': '0.00'
    }))

    class Meta:
        model = Product
        fields = ['type', 'sphere', 'cylindre', 'axe', 'addition']


class EntryForm(forms.ModelForm):

    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, empty_label='Choisissez la lentille')

    qty = forms.FloatField(label="Quantité", required=True, widget=forms.NumberInput({
        'class': 'form-control'
    }))

    class Meta:
        model = Entry
        fields = ['product', 'qty']


class ExitForm(forms.ModelForm):
    qs = Product.objects.filter(in_stock=True)
    product = forms.ModelChoiceField(empty_label='Choisissez un produit', queryset=qs)
    qty = forms.FloatField(label='Quantité', widget=forms.NumberInput({
        'class': 'form-control'
    }))

    class Meta:
        model = Exit
        fields = [
            'product',
            'qty'
        ]

    def clean_qty(self, *args, **kwargs):
        product = self.cleaned_data.get('product')
        qty = self.cleaned_data.get('qty')

        # get qty of the product in stock
        qs = Stock.objects.filter(product_id=product)
        if qs.exists() and qs.count() == 1:
            stck = qs.first()
            if stck.qty < qty:
                raise forms.ValidationError(
                    "La quantité en stock est inferieur a {}, vous avez {} paire de {} en stock".format(qty, stck.qty, stck.product.reference))
        return qty

    def save(self, commit=True, request=None):
        exit = super(ExitForm, self).save(commit=False)
        qs = Profile.objects.filter(user=request.user)
        if qs.exists() and qs.count() == 1:
            user_ = qs.first()
            print(user_)
            exit.provider = user_
        if commit:
            exit.save()
        return exit


class TypeForm(forms.ModelForm):

    name = forms.CharField(label="libelé du type", widget=forms.TextInput({
        'class': 'form-control'
    }))
    code = forms.CharField(widget=forms.TextInput({
        'class': 'form-control'
    }))

    class Meta:
        model = Type
        fields = ['name', 'code']