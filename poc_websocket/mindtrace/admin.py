from django.contrib import admin
from .models import (
    Patient,
    Protocol,
    Assessment,
    ProtocolAssessment,
    Category,
    AssessmentMeta,
    AssessmentAlias,
    Session,
    AssessmentRun,
    Metric,
)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "external_id", "name", "created_at", "updated_at")
    search_fields = ("external_id", "name")


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "psyexp")
    search_fields = ("name", "psyexp")


@admin.register(ProtocolAssessment)
class ProtocolAssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "protocol", "assessment", "order")
    list_filter = ("protocol",)
    search_fields = ("protocol__name", "assessment__name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "label")
    search_fields = ("key", "label")


@admin.register(AssessmentMeta)
class AssessmentMetaAdmin(admin.ModelAdmin):
    list_display = ("id", "assessment", "scoring")
    list_filter = ("scoring",)
    search_fields = ("assessment__name",)


@admin.register(AssessmentAlias)
class AssessmentAliasAdmin(admin.ModelAdmin):
    list_display = ("id", "term", "assessment")
    search_fields = ("term", "assessment__name")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "protocol", "start_time", "site", "operator", "session_type")
    list_filter = ("protocol", "site", "session_type")
    search_fields = ("patient__external_id", "patient__name", "operator")


@admin.register(AssessmentRun)
class AssessmentRunAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "assessment", "event", "start_time")
    list_filter = ("assessment",)
    search_fields = ("assessment__name", "session__patient__external_id")


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("id", "run", "key", "value_int", "value_float", "value_text")
    list_filter = ("key",)
    search_fields = ("key", "run__assessment__name")
