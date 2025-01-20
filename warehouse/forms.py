from django import forms
from .models import Film
from .models import Artist
from .models import AllMedia

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['film_name', 'film_type', 'iso', 'description', 'cover_image']
        widgets = {
            'film_name': forms.TextInput(attrs={'class': 'enter-box'}),
            'film_type': forms.TextInput(attrs={
                'class': 'enter-box',
                'placeholder': '135, 120, 4x5, ...'
            }),
            'iso': forms.NumberInput(attrs={
                'class': 'enter-box',
                'placeholder': '50, 100, 200, 400, ...'
            }),
            'description': forms.Textarea(attrs={'class': 'enter-box-large'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'upload-input'}),
        }


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            'first_name', 'last_name', 'middle_name', 'preferred_name',
            'birth_date', 'death_date', 'gender', 'description', 'cover_image'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AllMediaForm(forms.ModelForm):
    class Meta:
        model = AllMedia
        fields = ['media_type', 'title', 'author', 'date', 'location', 'description', 'media_src', 'media_src_2', 'is_active']

    def clean(self):
        cleaned_data = super().clean()

        # Check if media_src is present in request.FILES
        if not self.files.get('media_src'):
            raise forms.ValidationError({"media_src": "Basic image is required."})

        return cleaned_data