from django import forms
from coordmanager.models import Coordinate


class ImportCoordinate(forms.ModelForm):
    """
    form used to validate the point data from CSV file
    """
    id = forms.IntegerField(min_value=0)

    class Meta:
        model = Coordinate
        fields = ['x', 'y']

    def save(self, commit=False):
        raise NotImplementedError('Save metod is not implemented')
