from django import forms


class EditIdentityForm(forms.Form):
    """
        An identity update form
    """
    name = forms.CharField(label='Name', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    repository_identifier = forms.CharField(label='Repository Identifier', required=True,
                                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    enable_harvesting = forms.BooleanField(label='Enable Harvesting ?',
                                           widget=forms.CheckboxInput(attrs={'class': 'cmn-toggle cmn-toggle-round',
                                                                             'visibility': 'hidden'}),
                                           required=False, initial=False)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
