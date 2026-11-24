import os
from django import forms
from django.conf import settings
from .models import PlantLeafUpload

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


class LeafUploadForm(forms.ModelForm):
    """
    Form for uploading plant leaf images with size and format validation.
    """
    class Meta:
        model = PlantLeafUpload
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'file-input',
                'id': 'leaf-image-input',
                'accept': 'image/*',
                'required': True,
            })
        }
        labels = {
            'image': 'Select Plant Leaf Image',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("Please select an image file.")

        ext = os.path.splitext(image.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                f"Unsupported file format ({ext}). Please upload a valid JPG, JPEG, PNG, or WEBP image."
            )

        max_size_mb = getattr(settings, 'MAX_UPLOAD_SIZE_MB', 10)
        if image.size > max_size_mb * 1024 * 1024:
            raise forms.ValidationError(
                f"Image file size ({image.size / (1024 * 1024):.1f} MB) exceeds maximum allowed limit of {max_size_mb} MB."
            )

        return image


class UserRegisterForm(forms.ModelForm):
    """
    User registration form based on Django's User model with secure password handling.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your desired username',
            'autocomplete': 'username',
            'required': True,
        }),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email address (optional)',
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create a strong password',
            'autocomplete': 'new-password',
            'required': True,
        }),
        help_text="Your password must be at least 8 characters long."
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
            'required': True,
        })
    )

    class Meta:
        from django.contrib.auth.models import User
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        from django.contrib.auth.models import User
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with this username already exists. Please choose a different username.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', "Passwords do not match. Please enter both passwords identically.")
            elif len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """
    Login form for user authentication.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your username',
            'autocomplete': 'username',
            'required': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
            'required': True,
        })
    )


