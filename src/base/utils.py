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


def check_ncsu_email(email):
    """Check if the given email belongs to NCSU email id."""
    parts = email.split("@")
    if parts[-1] != "ncsu.edu":
        return False
    return True

def calculate_compatibility(user_profile, other_profile):
    """Calculate the compatibility score between two user profiles."""
    score = 0
    total_weight = 0  # Start at zero

    # Check gender preference
    if user_profile.gender_preference == other_profile.gender:
        score += 1
        total_weight += 1
    elif user_profile.gender_preference == "No Preference":
        total_weight += 0.5  # Add partial weight if 'No Preference'

    # Check diet preference
    if user_profile.diet_preference == other_profile.diet:
        score += 1
        total_weight += 1
    elif user_profile.diet_preference == "No Preference":
        total_weight += 0.5

    # Check degree preference
    if user_profile.degree_preference == other_profile.degree:
        score += 1
        total_weight += 1
    elif user_profile.degree_preference == "No Preference":
        total_weight += 0.5

    # Check course preference
    if user_profile.course_preference == other_profile.course:
        score += 1
        total_weight += 1
    elif user_profile.course_preference == "No Preference":
        total_weight += 0.5

    # Check country preference
    if user_profile.country_preference == other_profile.country:
        score += 1
        total_weight += 1
    elif user_profile.country_preference == "No Preference":
        total_weight += 0.5

    # Return percentage based on actual score and total weight
    if (
        total_weight == 0
    ):  # Prevent division by zero if all preferences are 'No Preference'
        return 0

    return (score / total_weight) * 100