from enum import Enum


class BPCategory(Enum):
    """Blood Pressure Categories"""

    LOW = "Low Blood Pressure"
    IDEAL = "Ideal Blood Pressure"
    PRE_HIGH = "Pre-High Blood Pressure"
    HIGH = "High Blood Pressure"


class BloodPressure:
    """Blood Pressure model with validation and category calculation"""

    SYSTOLIC_MIN = 70
    SYSTOLIC_MAX = 190
    DIASTOLIC_MIN = 40
    DIASTOLIC_MAX = 100

    def __init__(self, systolic: int, diastolic: int):
        """
        Initialize BloodPressure with systolic and diastolic values

        Args:
            systolic: Systolic pressure in mmHG
            diastolic: Diastolic pressure in mmHG
        """
        self.systolic = systolic
        self.diastolic = diastolic

    @property
    def category(self) -> BPCategory:
        """
        Calculate and return the blood pressure category based on medical guidelines.

        Categories:
        - Low: Systolic < 90 AND Diastolic < 60
        - Ideal: Systolic < 120 AND Diastolic < 80
        - Pre-High: Systolic 120-139 OR Diastolic 80-89
        - High: Systolic >= 140 OR Diastolic >= 90

        Returns:
            BPCategory: The blood pressure category based on systolic and diastolic values
        """
        # High Blood Pressure (check first - highest priority)
        if self.systolic >= 140 or self.diastolic >= 90:
            return BPCategory.HIGH

        # Low Blood Pressure
        elif self.systolic < 90 and self.diastolic < 60:
            return BPCategory.LOW

        # Ideal Blood Pressure
        elif self.systolic < 120 and self.diastolic < 80:
            return BPCategory.IDEAL

        # Pre-High Blood Pressure
        else:
            return BPCategory.PRE_HIGH

    def validate_systolic(self) -> bool:
        """Check if systolic value is in valid range"""
        return self.SYSTOLIC_MIN <= self.systolic <= self.SYSTOLIC_MAX

    def validate_diastolic(self) -> bool:
        """Check if diastolic value is in valid range"""
        return self.DIASTOLIC_MIN <= self.diastolic <= self.DIASTOLIC_MAX

    def is_valid(self) -> bool:
        """Check if both values are valid"""
        return self.validate_systolic() and self.validate_diastolic()
