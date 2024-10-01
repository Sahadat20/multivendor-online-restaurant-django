from django import forms 
from .models import Category

class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']