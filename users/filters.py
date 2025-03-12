import django_filters

from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    payment_date = django_filters.DateFromToRangeFilter()
    paid_course = django_filters.NumberFilter(field_name="paid_course__id")
    paid_lesson = django_filters.NumberFilter(field_name="paid_lesson__id")
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHODS)

    class Meta:
        model = Payment
        fields = ["payment_date", "paid_course", "paid_lesson", "payment_method"]
