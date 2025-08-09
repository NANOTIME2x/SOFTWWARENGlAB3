import re
from django import template
from django.utils.safestring import mark_safe
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def highlight(text, word):
    if not text or not word:
        return text
    # بحث غير حساس لحالة الأحرف مع تمييز الكلمات المطابقة
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    highlighted = pattern.sub(lambda m: f'<mark>{m.group(0)}</mark>', text)
    return mark_safe(highlighted)

@register.filter
def relative_date_ar(value):
    if not isinstance(value, datetime):
        return value

    now = timezone.now()
    diff = now - value
    seconds = diff.total_seconds()

    def arabic_time_unit(unit, count):
        if count == 0:
            return ""
        elif count == 1:
            return f"1 {unit}"
        elif count == 2:
            return f"2 {unit}ان"
        elif 3 <= count <= 10:
            return f"{count} {unit}ات"
        else:
            return f"{count} {unit}"

    if seconds >= 0:
        # الماضي
        if seconds < 60:
            return f"منذ {int(seconds)} ثانية"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"منذ {arabic_time_unit('دقيقة', minutes)}"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"منذ {arabic_time_unit('ساعة', hours)}"
        elif seconds < 2592000:
            days = int(seconds // 86400)
            return f"منذ {arabic_time_unit('يوم', days)}"
        elif seconds < 31104000:
            months = int(seconds // 2592000)
            return f"منذ {arabic_time_unit('شهر', months)}"
        else:
            years = int(seconds // 31104000)
            return f"منذ {arabic_time_unit('سنة', years)}"
    else:
        # المستقبل
        seconds = abs(seconds)
        if seconds < 60:
            return f"بعد {int(seconds)} ثانية"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"بعد {arabic_time_unit('دقيقة', minutes)}"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"بعد {arabic_time_unit('ساعة', hours)}"
        elif seconds < 2592000:
            days = int(seconds // 86400)
            return f"بعد {arabic_time_unit('يوم', days)}"
        elif seconds < 31104000:
            months = int(seconds // 2592000)
            return f"بعد {arabic_time_unit('شهر', months)}"
        else:
            years = int(seconds // 31104000)
            return f"بعد {arabic_time_unit('سنة', years)}"
