from django import forms
from appointments.models import Appointment 

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, psychologist=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.psychologist = psychologist

    class Meta:
        model = Appointment
        fields = ['message', 'datetime']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'id': 'datetimepicker'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_datetime(self):
        dt = self.cleaned_data['datetime']

        if not self.psychologist:
            raise forms.ValidationError("Psihologul nu a fost setat.")

        exists = Appointment.objects.filter(
            psychologist=self.psychologist,
            datetime=dt
        ).exists()

        if exists:
            raise forms.ValidationError("Acest interval este deja rezervat.")

        return dt
    
class CancellationForm(forms.Form):
    cancellation_reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="Motivul anulării",
        required=True
    )