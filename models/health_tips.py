"""Health Tips Model - New Feature"""

from models.blood_pressure import BPCategory


class HealthTips:
    """Provides personalized health tips based on BP category"""

    TIPS = {
        BPCategory.LOW: [
            "Consider increasing salt intake slightly (consult your doctor)",
            "Stay well hydrated - drink plenty of water",
            "Eat small, frequent meals throughout the day",
            "Avoid sudden position changes - stand up slowly",
            "Consider compression stockings if recommended",
        ],
        BPCategory.IDEAL: [
            "Maintain a balanced diet rich in fruits and vegetables",
            "Exercise regularly - aim for 30 minutes daily",
            "Keep your weight in a healthy range",
            "Limit alcohol consumption",
            "Continue regular BP monitoring",
        ],
        BPCategory.PRE_HIGH: [
            "Reduce sodium intake - aim for less than 2,300mg/day",
            "Increase physical activity - at least 150 minutes weekly",
            "Maintain a healthy weight through diet and exercise",
            "Limit alcohol and quit smoking if applicable",
            "Monitor your blood pressure regularly at home",
        ],
        BPCategory.HIGH: [
            "Consult your healthcare provider immediately",
            "Follow prescribed medication regimen strictly",
            "Adopt the DASH diet - low sodium, rich in nutrients",
            "Exercise as recommended by your doctor",
            "Monitor blood pressure daily and keep a log",
        ],
    }

    @classmethod
    def get_tips(cls, category: BPCategory) -> list:
        """Get health tips for a specific BP category"""
        return cls.TIPS.get(category, []).copy()
