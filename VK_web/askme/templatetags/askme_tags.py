# Copyright 2023 Dmitriy Permyakov <dimapermyakov55@gmail.com>
from django import template
from askme.models import Answer

register = template.Library()


@register.simple_tag()
def get_count_answer(question_id):
    count = Answer.objects.filter(question_id=question_id).count()
    return count
