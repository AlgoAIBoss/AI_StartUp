from django import forms


class ImageForm(forms.Form):
    photo = forms.CharField(
        max_length=1000, required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter Image Link"}))
    
    
class SummaryForm(forms.Form):
    link = forms.CharField(
        max_length=1000, required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter Article Link"}))
    
    size = forms.CharField(
        max_length=1000, required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter Summary Size in lines (OPTIONAL)"}))
    
    textarea = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': "Enter Text"}))
    
    

class AudioForm(forms.Form):
    link = forms.CharField(
        max_length=1000, required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter Article Link"}))
    
    textarea = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': "Enter Text"}))
    
    
    
class ParaphForm(forms.Form):
    link = forms.CharField(
        max_length=1000, required=False, widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Enter Article Link"}))
    
    textarea = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': "Enter Text"}))