from django import forms


class NewCollectionForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea)
	owner = forms.CharField()


class NewSpectrumForm(forms.Form):
	instrument = forms.CharField(max_length=10)
	path = forms.CharField(widget=forms.Textarea)
	image_path = forms.CharField(widget=forms.Textarea)
	x_pixel = forms.IntegerField()
	y_pixel = forms.IntegerField()
	wavelength = forms.CharField(widget=forms.Textarea)
	reflectance = forms.CharField(widget=forms.Textarea)
	mineral_id = forms.IntegerField()
	latitude = forms.DecimalField(max_digits=9, decimal_places=6)
	longitude = forms.DecimalField(max_digits=9, decimal_places=6)