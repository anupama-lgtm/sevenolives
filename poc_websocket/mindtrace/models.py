from django.db import models


class Patient(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or self.external_id


class Protocol(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Assessment(models.Model):
    name = models.CharField(max_length=200, unique=True)
    psyexp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProtocolAssessment(models.Model):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='protocol_assessments')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='in_protocols')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('protocol', 'assessment')
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.protocol.name} -> {self.order}: {self.assessment.name}"


class Category(models.Model):
    key = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=200)
    fields_map = models.JSONField(default=dict, blank=True)
    summary_fields_map = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.label


class AssessmentMeta(models.Model):
    SCORING_CHOICES = [
        ('unknown', 'unknown'),
        ('binary', 'binary'),
        ('ordinal', 'ordinal'),
        ('svr', 'svr'),
        ('qab', 'qab'),
        ('demographics', 'demographics'),
        ('fluent_speech', 'fluent_speech'),
        ('subscale', 'subscale'),
        ('praxis', 'praxis'),
    ]
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='meta')
    scoring = models.CharField(max_length=32, choices=SCORING_CHOICES, default='unknown')
    categories = models.ManyToManyField(Category, related_name='assessments', blank=True)

    def __str__(self):
        return f"Meta({self.assessment.name})"


class AssessmentAlias(models.Model):
    term = models.CharField(max_length=200, unique=True)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='aliases')

    def __str__(self):
        return f"{self.term} -> {self.assessment.name}"


class Session(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='sessions')
    protocol = models.ForeignKey(Protocol, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    start_time = models.DateTimeField()
    site = models.CharField(max_length=200, blank=True)
    operator = models.CharField(max_length=200, blank=True)
    session_type = models.CharField(max_length=50, blank=True)
    app_version = models.CharField(max_length=50, blank=True)
    exp_version = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    frontmatter = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Session {self.id} - {self.patient} @ {self.start_time}"


class AssessmentRun(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='assessment_runs')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='runs')
    event = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    pagelink = models.TextField(blank=True)
    raw = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Run {self.id} - {self.assessment.name} ({self.session_id})"


class Metric(models.Model):
    run = models.ForeignKey(AssessmentRun, on_delete=models.CASCADE, related_name='metrics')
    key = models.CharField(max_length=200)
    value_int = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_text = models.TextField(blank=True)

    class Meta:
        unique_together = ('run', 'key', 'value_text')
        indexes = [
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return f"{self.key}={self.value_int or self.value_float or self.value_text}"
