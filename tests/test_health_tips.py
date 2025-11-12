"""Unit tests for Health Tips"""

from models.health_tips import HealthTips
from models.blood_pressure import BPCategory


class TestHealthTips:
    """Test Health Tips functionality"""

    def test_get_low_bp_tips(self):
        """Test getting tips for low blood pressure"""
        tips = HealthTips.get_tips(BPCategory.LOW)
        assert len(tips) == 5
        assert any("salt intake" in tip.lower() for tip in tips)
        assert isinstance(tips, list)

    def test_get_ideal_bp_tips(self):
        """Test getting tips for ideal blood pressure"""
        tips = HealthTips.get_tips(BPCategory.IDEAL)
        assert len(tips) == 5
        assert any("balanced diet" in tip.lower() for tip in tips)
        assert isinstance(tips, list)

    def test_get_pre_high_bp_tips(self):
        """Test getting tips for pre-high blood pressure"""
        tips = HealthTips.get_tips(BPCategory.PRE_HIGH)
        assert len(tips) == 5
        assert any("sodium intake" in tip.lower() for tip in tips)
        assert isinstance(tips, list)

    def test_get_high_bp_tips(self):
        """Test getting tips for high blood pressure"""
        tips = HealthTips.get_tips(BPCategory.HIGH)
        assert len(tips) == 5
        assert any("healthcare provider" in tip.lower() for tip in tips)
        assert isinstance(tips, list)

    def test_all_categories_have_tips(self):
        """Test that all BP categories have tips defined"""
        for category in BPCategory:
            tips = HealthTips.get_tips(category)
            assert len(tips) > 0
            assert isinstance(tips, list)

    def test_tips_are_strings(self):
        """Test that all tips are strings"""
        for category in BPCategory:
            tips = HealthTips.get_tips(category)
            for tip in tips:
                assert isinstance(tip, str)
                assert len(tip) > 0

    def test_tips_immutability(self):
        """Test that modifying returned tips doesn't affect original"""
        tips1 = HealthTips.get_tips(BPCategory.LOW)
        tips1.append("Modified tip")
        tips2 = HealthTips.get_tips(BPCategory.LOW)
        assert len(tips2) == 5
        assert "Modified tip" not in tips2
