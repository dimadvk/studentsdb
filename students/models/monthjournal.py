from django.db import models
from django.utils.translation import ugettext_lazy as _

class MonthJournal(models.Model):
    """Student Monthly Journal"""

    class Meta:
        verbose_name = _(u'month journal')
        verbose_name_plural = _(u'month journals')

    student = models.ForeignKey(
        'Student',
        verbose_name=_(u'student'),
        blank=False,
        unique_for_month='date')

    date = models.DateField(
        verbose_name=_(u'date'),
        blank=False)

    def __unicode__(self):
        return u'%s: %d, %d' % (self.student.last_name, self.date.month, self.date.year)

    local_vars = locals()
    for num in range(1, 32):
        local_vars.update({'present_day'+str(num) : models.BooleanField(default=False)})
  #  present_day1 = models.BooleanField(default=False)
  #  present_day2 = models.BooleanField(default=False)
  #  present_day3 = models.BooleanField(default=False)
  #  present_day4 = models.BooleanField(default=False)
  #  present_day5 = models.BooleanField(default=False)
  #  present_day6 = models.BooleanField(default=False)
  #  present_day7 = models.BooleanField(default=False)
  #  present_day8 = models.BooleanField(default=False)
  #  present_day9 = models.BooleanField(default=False)
  #  present_day10 = models.BooleanField(default=False)
  #  present_day11 = models.BooleanField(default=False)
  #  present_day12 = models.BooleanField(default=False)
  #  present_day13 = models.BooleanField(default=False)
  #  present_day14 = models.BooleanField(default=False)
  #  present_day15 = models.BooleanField(default=False)
  #  present_day16 = models.BooleanField(default=False)
  #  present_day17 = models.BooleanField(default=False)
  #  present_day18 = models.BooleanField(default=False)
  #  present_day19 = models.BooleanField(default=False)
  #  present_day20 = models.BooleanField(default=False)
  #  present_day21 = models.BooleanField(default=False)
  #  present_day22 = models.BooleanField(default=False)
  #  present_day23 = models.BooleanField(default=False)
  #  present_day24 = models.BooleanField(default=False)
  #  present_day25 = models.BooleanField(default=False)
  #  present_day26 = models.BooleanField(default=False)
  #  present_day27 = models.BooleanField(default=False)
  #  present_day28 = models.BooleanField(default=False)
  #  present_day29 = models.BooleanField(default=False)
  #  present_day30 = models.BooleanField(default=False)
  #  present_day31 = models.BooleanField(default=False)


