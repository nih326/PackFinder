#
# Created on Fri Nov 22 2024
#
# The MIT License (MIT)
# Copyright (c) 2024 Niharika Maruvanahalli Suresh , Diya Shetty, Sanjana Nanjangud Shreenivas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import django_filters
from base.models import Profile


class ProfileFilter(django_filters.FilterSet):
    """Filter to filter the queryset for profiles"""

    class Meta:
        model = Profile
        fields = ["gender", "degree", "course", "diet", "country"]

        # @property
        # def qs(self):
        #     profiles = super().qs

        #     return profiles.filter(visibility=True)
