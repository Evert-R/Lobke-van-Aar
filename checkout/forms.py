from django import forms
from .models import orders
from shop.models import shipping
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, LayoutObject


class shippingForm(forms.Form):
    """
    Form to edit shipping details
    """
    shipping_options = forms.ModelChoiceField(
        queryset=shipping.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super(shippingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 er-form-padding'
        self.helper.field_class = 'col-8 er-form-padding'


class PaymentForm(forms.Form):
    """
    Form to handle the stripe payment
    """
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(2018, 2036)]

    credit_card_number = forms.CharField(
        label='Credit card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(
        label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(
        label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 er-form-padding'
        self.helper.field_class = 'col-8 er-form-padding'
        self.helper.add_input(
            Submit('commit', 'Place order', css_id='submit_payment_btn', css_class='er-green'))
