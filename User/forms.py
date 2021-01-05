from django import forms
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.forms import UserCreationForm
import datetime
from User.models import UserRole, CustomUser, MARITAL_CHOICES, BLOOD_CHOICES
from People.models import Company, Department
from django.db.models import Q


class UserRoleForm(forms.ModelForm):
    user_role = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'user_role'}))

    class Meta:
        model = UserRole
        fields = "__all__"


class CustomUserCretaionForm(UserCreationForm):

    user_role = forms.ModelChoiceField(queryset=UserRole.objects.all(
    ), required=True, widget=forms.Select(
        attrs={'class': 'form-control user_role', 'id': 'user_role'}))

    company = forms.ModelChoiceField(queryset=Company.objects.all(
    ), required=True, widget=forms.Select(attrs={'class': 'form-control company', 'id': 'company_name'}))

    department = forms.ModelChoiceField(queryset=Department.objects.all(
    ), required=True, widget=forms.Select(attrs={'class': 'form-control department', 'id': 'department_name'}))

    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username'}))

    full_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'full_name'}))

    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'email'}))

    contact_no = forms.IntegerField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'contact_no'}))

    blood_group = forms.ChoiceField(required=False, choices=BLOOD_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'blood_group'}))

    marital_status = forms.ChoiceField(required=True, choices=MARITAL_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'marital_status'}))

    dob = forms.DateField(required=True, widget=forms.TextInput(
        attrs={'type': 'date', 'class': 'form-control', 'id': 'dob'}))

    job_title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'job_title'}))

    work_location = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'work_location'}))

    nid = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'nid'}))

    passport = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'passport'}))

    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password1'}))

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password2'}))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        def get_label(obj):
            permission_name = str(obj).split('|')[2].strip()
            model_name = permission_name.split(' ')[2].strip()
            return '%s | %s' % (model_name.title(), permission_name)

        # User = get_user_model()
        #content_type = ContentType.objects.filter(Q(model='userrole') | Q(model='department'))
        self.fields['user_permissions'].queryset = Permission.objects.filter().exclude(Q(content_type_id=1) | Q(
            content_type_id=2) | Q(content_type_id=3) | Q(content_type_id=6) | Q(content_type_id=5))
        self.fields['user_permissions'].widget.attrs.update(
            {'class': 'permission-select'})
        self.fields['user_permissions'].help_text = None
        self.fields['user_permissions'].label = "Label"
        self.fields['user_permissions'].label_from_instance = get_label

    def save(self, commit=True):
        user_instance = super(UserCreationForm, self).save(commit)
        user_instance.save()
        user_instance.user_permissions.set(
            self.cleaned_data.get('user_permissions'))
        return user_instance

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'full_name', 'contact_no', 'user_role', 'profile_pic', 'marital_status',
                  'blood_group', 'dob', 'job_title', 'work_location', 'nid', 'passport', 'company', 'department', 'last_login', 'user_permissions']
        widgets = {
            'user_permissions': forms.CheckboxSelectMultiple(attrs={'style': 'width: 30px; height: 15px;'})
        }
