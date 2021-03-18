from django import forms
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from works.models import work_items, work_images
from shop.models import shop_items, work_types, work_sizes, materials, shop_message
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, LayoutObject


class EditWorksForm(ModelForm):
    """
    Form to add a work to the portfolio and shop
    """

    class Meta:
        model = work_items
        fields = ['main_image', 'position', 'category', 'title',
                  'under_title', 'free_text', 'work_item', 'shop_item', 'collection', 'sort_order']
        widgets = {
            'free_text': Textarea(attrs={'cols': 10, 'rows': 10}),
        }
        labels = {
            'free_text': _('Description'),
        }
        help_texts = {
            'position': _('Choose layout of the work details view'),
            'free_text': _('This text is displayed on the work details page'),
            'sort_order': _('Choose the view order on the work page'),
            'work_item': _('<br>Show on the work page?'),
            'shop_item': _('<br>Show in the shop and create a shop settings form?'),
            'collection': _('<br>Make this work a collection'),
        }

    def __init__(self, *args, **kwargs):
        super(EditWorksForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 er-form-padding'
        self.helper.field_class = 'col-8 er-form-padding'
        self.helper.add_input(
            Submit('submit', 'Submit work details', css_class='er-green'))


class EditShopWorksForm(ModelForm):
    """
    Form for adding shop settings to a work
    """

    class Meta:
        model = shop_items
        fields = ['price', 'on_sale', 'discount', 'stock', 'edition_count', 'work_type', 'material', 'work_size', 'frame',
                  'signed', 'personal_message', 'standard_text', 'personal_text', 'sort_order']
        widgets = {
            'personal_message': Textarea(attrs={'cols': 10, 'rows': 10}),
        }
        labels = {
            'discount': _('Discount'),
            'edition_count': _('Edition total'),
            'personal_message': _('Personal desription'),
        }
        help_texts = {
            'discount': _('%'),
            'edition_count': _('How many were made?'),
            'signed': _('Is this item signed?'),
            'standard_text': _('Generate a description for the shop'),
            'personal_text': _('Show the personal desription in the shop'),
            'personal_message': _('Add a personal description for the shop'),
            'sort_order': _('Overrides default (Latest first)'),
        }

    def __init__(self, *args, **kwargs):
        super(EditShopWorksForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 er-form-padding'
        self.helper.field_class = 'col-8 er-form-padding'
        self.helper.add_input(
            Submit('submit', 'Submit shop details', css_class='er-green'))


class AddExtraImagesForm(ModelForm):
    """
    Form for adding images to a work
    """

    class Meta:
        model = work_images
        fields = ['work_item', 'work_image']
        widgets = {
            'work_item': forms.HiddenInput()
        }
        labels = {
            'work_image': _('Add image'),
        }

    def __init__(self, *args, **kwargs):
        super(AddExtraImagesForm, self).__init__(*args, **kwargs)
        self.fields['work_item'].widget.attrs['readonly'] = True
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 er-form-padding'
        self.helper.field_class = 'col-8 er-form-padding'
        self.helper.add_input(
            Submit('submit', 'Submit extra image', css_class='er-green'))


class SetShopMessageForm(ModelForm):
    """
    Form for setting a message on the shop page
    """

    class Meta:
        model = shop_message
        fields = ['info', 'show']
        widgets = {
            'info': Textarea(attrs={'cols': 10, 'rows': 4}),
        }
        labels = {
            'info': _('Shop message'),
        }
        help_texts = {
            'info': _('Set a message on the front page of the shop')
        }

    def __init__(self, *args, **kwargs):
        super(SetShopMessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 er-form-padding'
        self.helper.field_class = 'col-8 er-form-padding'

