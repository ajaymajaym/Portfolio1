from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    # Honeypot field: real users never see or fill this (hidden via CSS).
    # If it arrives populated, the submission is treated as spam.
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Your full name', 'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'you@example.com', 'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+91 98765 43210', 'autocomplete': 'tel',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': "What's this about?",
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Write your message here...', 'rows': 6,
            }),
        }

    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if len(message) < 10:
            raise forms.ValidationError("Your message is too short — please add a bit more detail.")
        return message

    def clean_full_name(self):
        name = self.cleaned_data['full_name'].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def is_spam(self):
        """True if the honeypot field was filled in — a strong signal of a bot."""
        return bool(self.cleaned_data.get('website'))
