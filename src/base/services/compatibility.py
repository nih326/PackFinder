class RoommateCompatibilityCalculator:
    """Class to calculate roommate compatibility based on user preferences."""

    def calculate_match(self, user_profile, other_profile):
        """
        Calculate compatibility score between two profiles.
        :param user_profile: Profile of the current user
        :param other_profile: Profile of the other user
        :return: A dictionary containing the total score and a breakdown of scores
        """

        score = 0
        max_score = 0
        breakdown = {}

        # Importance weights
        importance_weights = {
            1: 1,  # Not Important
            2: 2,  # Somewhat Important
            3: 3,  # Very Important
        }

        # Define compatibility criteria
        criteria = [
            ('cleanliness', 'cleanliness_importance'),
            ('noise_preference', 'noise_importance'),
            ('guest_preference', 'guest_importance'),
            ('sleep_schedule', 'sleep_schedule_importance'),
        ]

        # Evaluate each criterion
        for criterion, importance_field in criteria:
            user_value = getattr(user_profile, criterion, None)
            other_value = getattr(other_profile, criterion, None)
            importance = getattr(user_profile, importance_field, 1)

            max_score += importance_weights[importance]
            if user_value == other_value:
                score += importance_weights[importance]

            breakdown[criterion] = {
                'user_value': user_value,
                'other_value': other_value,
                'match': user_value == other_value,
                'weight': importance_weights[importance],
            }

        # Calculate compatibility percentage
        total_score = (score / max_score) * 100 if max_score > 0 else 0
        return {
            'total_score': round(total_score, 2),
            'breakdown': breakdown,
        }
