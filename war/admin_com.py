# coding: utf-8
from datetime import date

from django.contrib import admin
from django.utils.translation import ugettext_lazy


class DecadeBeginListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ugettext_lazy(u'事件发生年份')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = ' years'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (1937, ugettext_lazy(u'1937 年')),
            (1938, ugettext_lazy(u'1938 年')),
            (1939, ugettext_lazy(u'1939 年')),
            (1940, ugettext_lazy(u'1940 年')),
            (1941, ugettext_lazy(u'1941 年')),
            (1942, ugettext_lazy(u'1942 年')),
            (1943, ugettext_lazy(u'1943 年')),
            (1944, ugettext_lazy(u'1944 年')),
            (1945, ugettext_lazy(u'1945 年')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value():
            if int(self.value()) == 1937:
                return queryset.filter(begin_time__lte=date(int(self.value()), 12, 31))
            if int(self.value()) == 1945:
                return queryset.filter(begin_time__gte=date(int(self.value()), 1, 1))

            return queryset.filter(begin_time__gte=date(int(self.value()), 1, 1),
                                   begin_time__lte=date(int(self.value()), 12, 31))
