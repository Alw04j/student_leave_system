from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class Class(models.Model):
    UG_YEAR_CHOICES = [
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
    ]
    PG_YEAR_CHOICES = [
        ('1st', '1st'),
        ('2nd', '2nd'),
    ]

    LEVEL_CHOICES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
    ]

    COURSE_CHOICES = [
        # UG Courses
        ('BCA-AI', 'BCA (Artificial Intelligence)'),
        ('BBA-AV', 'BBA with Aviation'),
        ('BCOM-CO', 'B.Com. Model I Co-operation'),
        ('BCOM-FT', 'B.Com. Model I Finance & Taxation'),
        ('BSC-ECT', 'B.Sc. Electronics with Computer Technology (Honours)'),
        ('BSC-BT', 'B.Sc. Biotechnology'),
        ('BA-ENG', 'B.A. English Literature & Communication Studies Model III'),
        ('BSW', 'Bachelor of Social Work'),
        # PG Courses
        ('MSC-CS', 'M.Sc. Computer Science'),
        ('MA-HRM', 'MA Human Resource Management'),
        ('MCOM-FT', 'M.Com. Finance & Taxation'),
        ('MSC-ELX', 'M.Sc. Electronics'),
        ('MSC-BT', 'M.Sc. Biotechnology'),
        ('MA-ENG', 'M.A. English Literature'),
    ]

    BATCH_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
    ]

    year = models.CharField(max_length=3, choices=UG_YEAR_CHOICES, default='1st')
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='UG')
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, default='BCA-AI')
    batch = models.CharField(max_length=1, choices=BATCH_CHOICES, default='A')



    def clean(self):
        from django.core.exceptions import ValidationError
        pg_courses = [
            'MSC-CS', 'MA-HRM', 'MCOM-FT', 'MSC-ELX', 'MSC-BT', 'MA-ENG'
        ]
        ug_courses = [
            'BCA-AI', 'BBA-AV', 'BCOM-CO', 'BCOM-FT', 'BSC-ECT', 'BSC-BT', 'BA-ENG', 'BSW'
        ]
        if self.level == 'PG' and self.course in ug_courses:
            raise ValidationError(f"{self.get_course_display()} is a UG course and cannot be selected for PG level.")
        if self.level == 'UG' and self.course in pg_courses:
            raise ValidationError(f"{self.get_course_display()} is a PG course and cannot be selected for UG level.")

        # PG max year is 2nd only
        if self.level == 'PG' and self.year not in dict(Class.PG_YEAR_CHOICES):
            raise ValidationError("PG programmes can only be 1st or 2nd year.")

        # UG max year is up to 3rd only
        if self.level == 'UG' and self.year not in dict(Class.UG_YEAR_CHOICES):
            raise ValidationError("UG programmes can only be 1st, 2nd, or 3rd year.")

    def __str__(self):
        return f"{self.level} - {self.year} Year - {self.course} - Batch {self.batch}"


    class Meta:
        verbose_name_plural = "Classes"

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    review_msg = models.TextField(null=True, blank=True)
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewer', limit_choices_to={'is_teacher': True})
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        student_name = self.student.username if self.student else "Unknown"
        return f"{student_name} - {self.status}"
