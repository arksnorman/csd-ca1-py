"""Unit tests for BloodPressure model"""

import pytest
from models.blood_pressure import BloodPressure, BPCategory


class TestBloodPressureValidation:
    """Test validation methods"""

    def test_valid_systolic_range(self):
        """Test systolic validation with valid values"""
        bp = BloodPressure(systolic=120, diastolic=80)
        assert bp.validate_systolic() is True

    def test_systolic_below_min(self):
        """Test systolic below minimum"""
        bp = BloodPressure(systolic=69, diastolic=80)
        assert bp.validate_systolic() is False

    def test_systolic_above_max(self):
        """Test systolic above maximum"""
        bp = BloodPressure(systolic=191, diastolic=80)
        assert bp.validate_systolic() is False

    def test_valid_diastolic_range(self):
        """Test diastolic validation with valid values"""
        bp = BloodPressure(systolic=120, diastolic=80)
        assert bp.validate_diastolic() is True

    def test_diastolic_below_min(self):
        """Test diastolic below minimum"""
        bp = BloodPressure(systolic=120, diastolic=39)
        assert bp.validate_diastolic() is False

    def test_diastolic_above_max(self):
        """Test diastolic above maximum"""
        bp = BloodPressure(systolic=120, diastolic=101)
        assert bp.validate_diastolic() is False

    def test_is_valid_with_both_valid(self):
        """Test is_valid with both values valid"""
        bp = BloodPressure(systolic=120, diastolic=80)
        assert bp.is_valid() is True

    def test_is_valid_with_invalid_systolic(self):
        """Test is_valid with invalid systolic"""
        bp = BloodPressure(systolic=200, diastolic=80)
        assert bp.is_valid() is False

    def test_is_valid_with_invalid_diastolic(self):
        """Test is_valid with invalid diastolic"""
        bp = BloodPressure(systolic=120, diastolic=110)
        assert bp.is_valid() is False


class TestBloodPressureCategory:
    """Test BP category calculation"""

    def test_low_blood_pressure(self):
        """Test low blood pressure category"""
        bp = BloodPressure(systolic=85, diastolic=55)
        assert bp.category == BPCategory.LOW

    def test_low_blood_pressure_boundary(self):
        """Test low BP at boundary"""
        bp = BloodPressure(systolic=89, diastolic=59)
        assert bp.category == BPCategory.LOW

    def test_ideal_blood_pressure(self):
        """Test ideal blood pressure category"""
        bp = BloodPressure(systolic=110, diastolic=70)
        assert bp.category == BPCategory.IDEAL

    def test_ideal_blood_pressure_boundary(self):
        """Test ideal BP at upper boundary"""
        bp = BloodPressure(systolic=119, diastolic=79)
        assert bp.category == BPCategory.IDEAL

    def test_pre_high_blood_pressure_systolic(self):
        """Test pre-high BP based on systolic"""
        bp = BloodPressure(systolic=130, diastolic=75)
        assert bp.category == BPCategory.PRE_HIGH

    def test_pre_high_blood_pressure_diastolic(self):
        """Test pre-high BP based on diastolic"""
        bp = BloodPressure(systolic=115, diastolic=85)
        assert bp.category == BPCategory.PRE_HIGH

    def test_pre_high_blood_pressure_both(self):
        """Test pre-high BP with both elevated"""
        bp = BloodPressure(systolic=135, diastolic=88)
        assert bp.category == BPCategory.PRE_HIGH

    def test_high_blood_pressure_systolic(self):
        """Test high BP based on systolic"""
        bp = BloodPressure(systolic=145, diastolic=85)
        assert bp.category == BPCategory.HIGH

    def test_high_blood_pressure_diastolic(self):
        """Test high BP based on diastolic"""
        bp = BloodPressure(systolic=135, diastolic=95)
        assert bp.category == BPCategory.HIGH

    def test_high_blood_pressure_both(self):
        """Test high BP with both high"""
        bp = BloodPressure(systolic=160, diastolic=100)
        assert bp.category == BPCategory.HIGH


class TestBloodPressureEdgeCases:
    """Test edge cases and boundary values"""

    def test_minimum_valid_values(self):
        """Test minimum valid BP values"""
        bp = BloodPressure(systolic=70, diastolic=40)
        assert bp.is_valid() is True
        assert bp.category == BPCategory.LOW

    def test_maximum_valid_values(self):
        """Test maximum valid BP values"""
        bp = BloodPressure(systolic=190, diastolic=100)
        assert bp.is_valid() is True
        assert bp.category == BPCategory.HIGH

    def test_systolic_equals_diastolic(self):
        """Test when systolic equals diastolic (invalid in real life but valid range)"""
        bp = BloodPressure(systolic=80, diastolic=80)
        assert bp.is_valid() is True

    def test_category_boundary_90_60(self):
        """Test boundary between LOW and IDEAL"""
        bp_low = BloodPressure(systolic=89, diastolic=59)
        bp_ideal = BloodPressure(systolic=90, diastolic=60)
        assert bp_low.category == BPCategory.LOW
        assert bp_ideal.category == BPCategory.IDEAL

    def test_category_boundary_120_80(self):
        """Test boundary between IDEAL and PRE_HIGH"""
        bp_ideal = BloodPressure(systolic=119, diastolic=79)
        bp_pre_high = BloodPressure(systolic=120, diastolic=80)
        assert bp_ideal.category == BPCategory.IDEAL
        assert bp_pre_high.category == BPCategory.PRE_HIGH

    def test_category_boundary_140_90(self):
        """Test boundary between PRE_HIGH and HIGH"""
        bp_pre_high = BloodPressure(systolic=139, diastolic=89)
        bp_high = BloodPressure(systolic=140, diastolic=90)
        assert bp_pre_high.category == BPCategory.PRE_HIGH
        assert bp_high.category == BPCategory.HIGH
