"""
Forms for Helios
"""

from django import forms
from django.conf import settings

from .fields import DateTimeLocalField
from .models import Election


class ElectionForm(forms.Form):
  short_name = forms.SlugField(max_length=40, help_text='keine Leerzeichen, wird Teil der URL deiner Wahl sein, z. B. vorstandswahl-2030')
  name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':60}), help_text='der Name deiner Wahl, z. B. Vorstandswahl 2030')
  description = forms.CharField(max_length=4000, widget=forms.Textarea(attrs={'cols': 70, 'wrap': 'soft'}), required=False)
  election_type = forms.ChoiceField(label="Typ", choices = Election.ELECTION_TYPES)
  use_voter_aliases = forms.BooleanField(required=False, initial=False, help_text='Wenn ausgewählt, werden Wähleridentitäten im Stimmverfolgungszentrum durch Aliase wie „V12“ ersetzt')
  #use_advanced_audit_features = forms.BooleanField(required=False, initial=True, help_text='disable this only if you want a simple election with reduced security but a simpler user interface')
  randomize_answer_order = forms.BooleanField(required=False, initial=False, help_text='Aktiviere dies, wenn die Antwortreihenfolge für jeden Wähler zufällig sein soll')
  private_p = forms.BooleanField(required=False, initial=False, label="Privat?", help_text='Eine private Wahl ist nur für registrierte Wähler sichtbar.')
  help_email = forms.CharField(required=False, initial="", label="E-Mail-Adresse für Hilfe", help_text='Eine E-Mail-Adresse, über die Wähler Hilfe anfragen können.')

  if settings.ALLOW_ELECTION_INFO_URL:
    election_info_url = forms.CharField(required=False, initial="", label="URL für Wahlinfos", help_text="die URL eines PDF-Dokuments mit zusätzlichen Wahlinformationen, z. B. Kandidatenbiografien und Statements")

  # times
  voting_starts_at = DateTimeLocalField(help_text = 'UTC-Datum und -Uhrzeit, zu der die Wahl beginnt',
                                   required=False)
  voting_ends_at = DateTimeLocalField(help_text = 'UTC-Datum und -Uhrzeit, zu der die Wahl endet',
                                   required=False)

class ElectionTimeExtensionForm(forms.Form):
  voting_extended_until = DateTimeLocalField(help_text = 'UTC-Datum und -Uhrzeit, bis zu der die Wahl verlängert wird',
                                   required=False)

class EmailVotersForm(forms.Form):
  subject = forms.CharField(max_length=80)
  body = forms.CharField(max_length=4000, widget=forms.Textarea)
  send_to = forms.ChoiceField(label="Senden an", initial="all", choices= [('all', 'alle Wahlberechtigte'), ('voted', 'Wahlberechtigte, die bereits abgestimmt haben'), ('not-voted', 'Wahlberechtigte, die noch nicht abgestimmt haben')])

class TallyNotificationEmailForm(forms.Form):
  subject = forms.CharField(max_length=80)
  body = forms.CharField(max_length=2000, widget=forms.Textarea, required=False)
  send_to = forms.ChoiceField(label="Senden an", choices= [('all', 'alle Wahlberechtigte'), ('voted', 'Wahlberechtigte, die bereits abgestimmt haben'), ('none', 'niemand -- bist du sicher?')])

class VoterPasswordForm(forms.Form):
  voter_id = forms.CharField(max_length=50, label="Wähler-ID")
  password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

class VoterPasswordResendForm(forms.Form):
  voter_id = forms.CharField(max_length=50, label="Wähler-ID", help_text="Gib die Wähler-ID ein, die dir für diese Wahl zugewiesen wurde")

