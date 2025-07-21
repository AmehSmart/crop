"""
logic.py - Implements crop rotation, soil/fertilizer recommendation, and technique suggestion logic.
"""
from classes import Crop, Soil, FarmingTechnique
from typing import List

class CropRotationLogic:
    @staticmethod
    def suggest_next_crops(previous_crop: Crop, all_crops: List[Crop]) -> List[Crop]:
        # Prevent same family, suggest alternatives
        return [crop for crop in all_crops if crop.family != previous_crop.family]

class SoilRecommendationSystem:
    @staticmethod
    def recommend_soil_management(soil: Soil, crop_history: List[Crop]) -> str:
        # Dummy logic for now
        return f"Use organic fertilizer for {soil.soil_type} soil."

class TechniqueSuggestion:
    @staticmethod
    def suggest_techniques(soil: Soil, crop: Crop) -> List[FarmingTechnique]:
        # Dummy logic for now
        return [
            FarmingTechnique("Drip Irrigation", "Efficient water delivery.", [soil.soil_type]),
            FarmingTechnique("Intercropping", "Grow two or more crops together.", [soil.soil_type]),
            FarmingTechnique("Precision Farming", "Use data for optimized farming.", [soil.soil_type])
        ]
