# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL
now = timezone.localtime(timezone.now())

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ParkingLot(TimeStampedModel):
    name = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return f"Name: {self.name}" or ""

    def create_slots(self, count):
        "Create multiple slots for Parking with given count."
        for i in range(1, int(count)+1):
            Slot.objects.create(parking_id=self.id, slot_number=i)
        return self.slot_set.count()


class Slot(TimeStampedModel):
    slot_number = models.PositiveIntegerField(auto_created=True)
    is_available = models.BooleanField(default=True)
    parking = models.ForeignKey(ParkingLot, blank=True, null=True, on_delete=models.CASCADE)
    last_available = models.DateTimeField('Last available at', auto_now_add=True)

    def __str__(self) -> str:
        return f"Parking: {self.parking.name} Slot: {self.slot_number}" or str(self.id)


class Ticket(TimeStampedModel):
    slot = models.ForeignKey(Slot, null=True, blank=True, on_delete=models.CASCADE)
    vehicle_reg_number = models.CharField(max_length=32, null=True, blank=True)
    age_of_driver = models.IntegerField(default=0)
    issued_at = models.DateTimeField('Issued at', auto_now_add=True)
    contact_number = models.CharField(max_length=32, null=True, blank=True)
    status = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"Ticket Id: {self.id} Status: {self.status}" or str(self.id)


def upload_file(instance, file_data):
    """
    Stores the attachment in a "per primary_data/module-type/yyyy/mm/dd" folder.
    :param instance, filename
    :returns ex: primary_data/uploadprimarydata/2020/06/01/filename
    """
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return 'primary_data/{model}/{year}/{month}/{day}/{file_data}'.format(
        model=instance._meta.model_name,
        year=today.year, month=today.month,
        day=today.day, file_data=file_data
    )

def file_extension_validator(value):
    valid_extensions_file = ('csv')
    if value:
        file_name = value.name
        file_extension = file_name.split('.')[-1].lower()
        if file_extension in valid_extensions_file:
            if value.size > int(settings.MAX_UPLOAD_SIZE):
                raise ValidationError("Please keep the file size under 15 MB")
        else:
            raise ValidationError("Please upload file in CSV formats.")
    else:
        return True

class FileType:
    """Lookups for uploaded file type."""
    CSV = 1


class UploadPrimaryData(TimeStampedModel):
    '''
    User Upload file.
    '''
    FILE_TYPE_CHOICE = (
    (FileType.CSV,'CSV'),
    (None, 'Select file type')
    )
    file_data = models.FileField(upload_to=upload_file, blank=True, null=True, validators=[file_extension_validator])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    file_type = models.PositiveSmallIntegerField(choices=FILE_TYPE_CHOICE, default=FileType.CSV, blank=True)
    is_executed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.email)

    class Meta:
        db_table = 'user_upload'
        verbose_name_plural = 'UploadRequests'

    def get_absolute_url(self):
        return self.file_data.url

    def get_file_name(self):
        try:
            return self.file_data.name.split("/")[-1]
        except Exception:
            return ""
