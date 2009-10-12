# form fields and widgets that are pretty generic and can be shared across modules
from django.forms.fields import Field, CharField, RegexField, TimeField, DEFAULT_TIME_INPUT_FORMATS, email_re, EMPTY_VALUES
from django.forms.widgets import Textarea
from django.forms.util import ValidationError
from django.utils.translation import ugettext as _

import logging

class ListField(CharField):
    """
    A Field that expects a string that represents a list of values, to be broken apart and then validated in pieces.
    """
    widget = Textarea
    split_strs = [',',';']
    
    def split(self, value):
        """
        Splits apart the value into a list.
        Splits on the strings defined in self.split_strs.
        Assumes that the list will also be split by spaces and all surrounding whitespace for each item will be stripped (should be fixed).
        """
        if not value:
            return value
        new_value = value[:]
        for splitter in self.split_strs:
            new_value = new_value.replace(splitter, ' ')
        # this use of split() takes care of stripping extra whitespace too
        return new_value.split()
        
    def clean(self, value):
        values = self.split(value)
        error_list = []
        for value in values:
            try:
                value = super(ListField, self).clean(value)
            except ValidationError, e:
                error_list.append(e)
        if error_list:
            raise ValidationError(error_list)
        return values
    
        
    
class RegexListField(ListField, RegexField):
    """
    A Field that expects a string that represents a list of values, all to be validated with the given regex.
    """
    
    def clean(self, value):
        Field.clean(self, value)
        if value in EMPTY_VALUES:
            return value
            
        values = self.split(value)
        error_list = []
        for value in values:
            try:
                value = RegexField.clean(self, value)
            except ValidationError, e:
                error_list.append(value)
        if error_list:
            logging.debug("err_list %s" % (error_list,))
            if len(error_list) == 1:
                message = "%s does not appear to be a valid email address" % error_list[0]
            else:
                message = "%s do not appear to be valid email addresses" % ', '.join(error_list)
            raise ValidationError(message)
        return values
            
            
class EmailListField(RegexListField):
    default_error_messages = {
        'invalid': _(u'There were invalid e-mail addresses.'),
    }
    
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
           RegexListField.__init__(self, email_re, max_length, min_length, *args,
                               **kwargs)
