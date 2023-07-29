from django.forms import DateField, Select, NumberInput, IntegerField, Form, SelectDateWidget, ChoiceField
from viewer.models import Airport, City
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


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

    # class AddTrip(forms.ModelForm):
    #     class Meta:
    #         model = Trip
    #         fields = (
    #             'from_city',
    #             'from_airport',
    #             'to_city',
    #             'to_airport',
    #             'departure_date',
    #             'return_date',
    #             'nr_adults',
    #             'places_for_children'
    #         )

    # class AddNewTrip(forms.ModelForm):
    #
    #     class Meta:
    #         model = Trip
    #         fields = ('from_city', 'from_airport',
    #                   'to_city', 'to_airport',
    #                   'deperture_date', 'return_date',
    #                   'nr_adults', 'places_for_children'
    #                   )

    # class Trip(Model):
    #     Board_TYPES = [
    #         ('BB', 'Bed and Breakfast'),
    #         ('HB', 'Half Board'),
    #         ('FB', 'Full Board'),
    #         ('AI', 'All Inclusive')
    #     ]
    #     from_city = ForeignKey(City, related_name='departure_trips', on_delete=RESTRICT)
    #     from_airport = ForeignKey(Airport, related_name='departure_trips', on_delete=RESTRICT)
    #     to_city = ForeignKey(City, related_name='arrival_trips', on_delete=RESTRICT)
    #     to_airport = ForeignKey(Airport, related_name='arrival_trips', on_delete=RESTRICT)
    #     departure_date = DateField()
    #     return_date = DateField()
    #     board_type = CharField(max_length=2, choices=Board_TYPES)
    #     nr_adults = IntegerField()
    #     places_for_children = IntegerField()

    # def date_check(self):
    #     if self.return_date <= self.departure_date:
    #         raise ValidationError('Error')


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

        if date_of_departure and return_date:
            if return_date < date_of_departure:
                raise ValidationError({
                    'return_date': ValidationError(
                        _('Return date cannot be before departure date.'),
                        code='invalid'
                    ),
                })
