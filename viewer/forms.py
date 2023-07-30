from django.forms import DateField, Select, NumberInput, IntegerField, Form, SelectDateWidget, ChoiceField, ModelForm, \
    DateInput
from viewer.models import City, Reservations, Hotel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone


class SignUpForm(UserCreationForm):
    pass

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class SearchForm(Form):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        get_city = City.objects.all()
        self.fields['from_location'] = ChoiceField(
            choices=[(city.id, f'{city.name} - {", ".join([airport.name for airport in city.airport_set.all()])}')
                     for city in get_city
                     ],
            widget=Select(attrs={'class': 'form-control'}),
            label='From'
        )
        self.fields['to_location'] = ChoiceField(
            choices=[(city.id, f'{city.name} - {", ".join([airport.name for airport in city.airport_set.all()])}')
                     for city in get_city
                     ],
            widget=Select(attrs={'class': 'form-control'}),
            label='To'
        )

    date_of_departure = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))
    return_date = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))
    number_of_adults = IntegerField(min_value=1, widget=NumberInput(attrs={'class': 'form-control'}),
                                    label='Nr. of Adults', initial=1)
    number_of_children = IntegerField(min_value=0, widget=NumberInput(attrs={'class': 'form-control'}),
                                      label='Nr. of Children', initial=0)

    def clean(self):
        cleaned_data = super().clean()
        date_of_departure = cleaned_data.get('date_of_departure')
        return_date = cleaned_data.get('return_date')

        if date_of_departure and date_of_departure < timezone.localdate():
            self.add_error('date_of_departure', 'Departure date cannot be in the past.')
        if return_date and return_date < timezone.localdate():
            self.add_error('return_date', 'Return date cannot be in the past.')

        if date_of_departure and return_date:
            if return_date < date_of_departure:
                self.add_error('return_date', 'Return date cannot be before departure date.')


class ReservationForm(ModelForm):
    date_of_departure = DateField(
        required=True,
        widget=DateInput(attrs={'class': 'form-control'}),
        label='Date of Departure'
    )
    return_date = DateField(
        required=True,
        widget=DateInput(attrs={'class': 'form-control'}),
        label='Return Date'
    )

    class Meta:
        model = Reservations
        fields = [
            'from_location',
            'to_location',
            'date_of_departure',
            'return_date',
            'number_of_adults',
            'number_of_children',
            'hotel',
            'hotel_price',
            'airport_price',
        ]
        widgets = {
            'from_location': Select(attrs={'class': 'form-control'}),
            'to_location': Select(attrs={'class': 'form-control', 'id': 'id_to_location'}),
            'date_of_departure': DateInput(attrs={'class': 'form-control'}),
            'return_date': DateInput(attrs={'class': 'form-control'}),
            'number_of_adults': NumberInput(attrs={'class': 'form-control'}),
            'number_of_children': NumberInput(attrs={'class': 'form-control'}),
            'hotel': Select(attrs={'class': 'form-control', 'id': 'id_hotel'}),
            'hotel_price': NumberInput(attrs={'class': 'form-control', 'id': 'id_hotel_price', 'readonly': 'readonly'}),
            'airport_price': NumberInput(
                attrs={'class': 'form-control', 'id': 'id_airport_price', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        to_location_id = self.data.get('to_location')

        if to_location_id:
            self.fields['hotel'].queryset = Hotel.objects.filter(belong_to_city_id=to_location_id)
        else:
            self.fields['hotel'].queryset = Hotel.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('date_of_departure')
        return_date = cleaned_data.get('return_date')

        if departure_date and departure_date < timezone.now().date():
            self.add_error('date_of_departure', 'Departure date should be in the future.')

        if return_date and return_date < departure_date:
            self.add_error('return_date', 'Return date should be after the departure date.')
