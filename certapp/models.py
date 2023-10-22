import uuid
from django.db import models

# Create your models here.
class Department(models.Model):
    dept_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"
 
class Course(models.Model):
    course_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.title}"
    
level_choices = [
    ('national diploma', 'national diploma'),
    ('higher national diploma', 'higher national diploma'),
]

class Holder(models.Model):
    holder_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    matric_no = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True, null=True, blank=True)
    picture = models.ImageField(default='auth/assets/images/default.jpg', upload_to='uploads/')
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    level = models.CharField(max_length=50, choices=level_choices, default='national diploma')
    grade = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"

class Certificate(models.Model):
    cert_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    serial_number = models.CharField(max_length=20, unique=True)
    holder = models.OneToOneField(Holder, on_delete=models.CASCADE)
    qr_code = models.TextField()
    
    def __str__(self):
        return f"{self.holder.first_name} - {self.serial_number}"
