# coding=utf-8
"""Utility fields."""
import logging
logger = logging.getLogger(__name__)

# System imports
import logging

# Django imports
from django import forms

logger = logging.getLogger(__name__)
AUTO_BOOTSTRAP = False

class InstanceForm (forms.Form):
    def __init__ (self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super(InstanceForm, self).__init__(*args, **kwargs)

        if self.instance:
            # Prefill fields
            initial = {}
            for field in self.fields:
                val = getattr(self.instance, field, None)
                if val:
                    initial[field] = val
            self.initial = initial

class WidgetMix (object):
    AVAILABLE_MIXINS = { u"autofocus", u"placeholder", u"type", u"bootstrap",
                         u"pattern", u"step", u"required" }

    def __init__ (self, *args, **kwargs):
        self.mixin = kwargs.pop("mixin", [])
        self.attrs_mixin()

        # Fucking widgets
        widget = kwargs.pop("widget", super(WidgetMix, self).widget)
        if isinstance(widget, type):
            self.widget = widget(attrs=self.attrs)
        super(WidgetMix, self).__init__(*args, **kwargs)

    def widget_attrs (self, widget):
        attrs = super(WidgetMix, self).widget_attrs(widget)
        attrs.update(self.attrs)
        logger.info(attrs)
        return attrs

    def parse_mix (self, m):
        if isinstance(m, basestring):
            name, attrs = m, []
        else:
            name, attrs = m[0], m[1:]
        if name not in self.AVAILABLE_MIXINS:
            raise LookupError(u"Unavailable mixin described: {0}".format(name))
        return name, attrs

    def attrs_mixin (self):
        self.attrs = {}
        if AUTO_BOOTSTRAP:
            self.mixin = [u"bootstrap"] + self.mixin

        for mix in self.mixin:
            name, attrs = self.parse_mix(mix)
            fn = getattr(self, name)
            fn(*attrs)

    def bootstrap (self, *disable):
        self.attrs[u"class"] = u"form-control" if not disable else u""

    def autofocus (self):
        self.attrs[u"autofocus"] = u"autofocus"

    def placeholder (self, text=None):
        text = text or self.verbose_name
        self.attrs[u"placeholder"] = text

    def type (self, field_type):
        self.attrs[u"type"] = field_type

    def step (self, inc):
        self.attrs[u"step"] = inc

    def required (self, *disable):
        self.attrs[u"required"] = u"required" if not disable else u""

    def pattern (self, expression):
        self.attrs[u"pattern"] = expression

class IntegerField (WidgetMix, forms.IntegerField):
    def __init__ (self, *args, **kwargs):
        mixin = kwargs.pop("mixin", [])
        kwargs["mixin"] = [ ("type", "number"), ("step", 1) ] + mixin
        super(IntegerField, self).__init__(*args, **kwargs)

class FloatField (WidgetMix, forms.FloatField):
    def __init__ (self, *args, **kwargs):
        mixin = kwargs.pop("mixin", [])
        kwargs["mixin"] = [("type", "number")] + mixin
        super(FloatField, self).__init__(*args, **kwargs)

class CharField (WidgetMix, forms.CharField):
    def __init__ (self, *args, **kwargs):
        kwargs.setdefault("max_length", 255)
        super(CharField, self).__init__(*args, **kwargs)

class EmailField (WidgetMix, forms.EmailField):
    def __init__ (self, *args, **kwargs):
        mixin = kwargs.pop("mixin", [])
        kwargs["mixin"] = [("type", "email")] + mixin
        super(EmailField, self).__init__(*args, **kwargs)

class PasswordField (CharField):
    def __init__ (self, *args, **kwargs):
        mixin = kwargs.pop("mixin", [])
        kwargs["mixin"] = [("type", "password")] + mixin
        kwargs.setdefault("widget", forms.PasswordInput)
        super(PasswordField, self).__init__(*args, **kwargs)

class TextField (CharField):
    def __init__ (self, *args, **kwargs):
        kwargs.setdefault("widget", forms.Textarea)
        kwargs.setdefault("max_length", 255)
        super(TextField, self).__init__(*args, **kwargs)

class DateTimeField (WidgetMix, forms.DateTimeField):
    def __init__ (self, *args, **kwargs):
        kwargs["mixin"] = [("type", "datetime")] + kwargs.pop("mixin", [])
        super(DateTimeField, self).__init__(*args, **kwargs)

class DateField (WidgetMix, forms.DateField):
    def __init__ (self, *args, **kwargs):
        mixin = kwargs.pop("mixin", [])
        kwargs["mixin"] = [("type", "date")] + mixin
        super(DateField, self).__init__(*args, **kwargs)

def FieldFactory (Parent, **d_args):
    class FactoryField (WidgetMix, Parent):
        def __init__ (self, *args, **kwargs):
            kwargs["mixin"] = d_args.pop("mixin", []) + kwargs.pop("mixin", [])
            d_args.update(kwargs)
            super(FactoryField, self).__init__(*args, **d_args)
    return FactoryField

ModelMultipleChoiceField = FieldFactory(forms.ModelMultipleChoiceField,
                                        widget=forms.CheckboxSelectMultiple,
                                        mixin=[("bootstrap", False)])
