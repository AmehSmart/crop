"""
logic.py - Crop rotation, soil, fertilizer and technique recommendations.
"""

class CropRotationLogic:
    # A simple mapping for family lookup by crop name (lowercase)
    CROP_FAMILIES = {
        "wheat": "cereal", "maize": "cereal", "rice": "cereal", "barley": "cereal",
        "soybean": "legume", "peanut": "legume", "lentil": "legume", "chickpea": "legume",
        "potato": "root", "cassava": "root", "yam": "root", "carrot": "root",
        "tomato": "vegetable", "onion": "vegetable", "cabbage": "vegetable", "mustard": "vegetable",
        "sunflower": "oilseed", "cotton": "fiber"
    }

    def check_rotation(self, previous_crop: str, current_crop: str):
        prev_family = self.CROP_FAMILIES.get(previous_crop.lower())
        curr_family = self.CROP_FAMILIES.get(current_crop.lower())

        if not prev_family or not curr_family:
            return f"❓ Unknown crop: {previous_crop if not prev_family else ''} {current_crop if not curr_family else ''}".strip(), []

        if prev_family == curr_family:
            # suggest alternatives from other families
            alternatives = [name.title() for name, fam in self.CROP_FAMILIES.items() if fam != prev_family]
            msg = f"⚠️ Avoid planting {current_crop} after {previous_crop} (same family: {prev_family}). Choose an alternative."
            return msg, alternatives
        else:
            return f"✅ Good rotation: {current_crop} after {previous_crop}.", []


class SoilRecommendationSystem:
    FERTILIZER_RECOMMENDATIONS = {
        "cereal": "NPK 15:15:15 (~200 kg/ha) + Urea top-dress.",
        "legume": "Low N required; apply SSP (P source).",
        "root": "Higher K demand: MOP + well-decomposed compost.",
        "vegetable": "Balanced NPK 20:10:10 + organic compost.",
        "oilseed": "Balanced NPK + Boron supplement.",
        "fiber": "Nitrogen and Potassium priority; moderate Phosphorus.",
    }

    @staticmethod
    def recommend_fertilizer(crop_name: str):
        family = CropRotationLogic.CROP_FAMILIES.get(crop_name.lower())
        if family:
            return SoilRecommendationSystem.FERTILIZER_RECOMMENDATIONS.get(family, "Use balanced NPK and compost.")
        return "No fertilizer recommendation found."

    @staticmethod
    def recommend_soil_management(soil, crops):
        # Very lightweight rule-of-thumb advice using soil properties
        fert = soil.properties.get("fertility")
        drainage = soil.properties.get("drainage")

        tips = []
        if fert == "low":
            tips.append("Incorporate compost/manure to boost fertility.")
        elif fert == "high":
            tips.append("Maintain fertility with residues/cover crops.")

        if drainage == "fast":
            tips.append("Use mulch and drip to reduce water loss.")
        elif drainage == "slow":
            tips.append("Create raised beds/ridges and avoid over-irrigation.")

        if not tips:
            tips.append("General soil care: add organic matter and monitor moisture.")
        return " ".join(tips)


class TechniqueSuggestion:
    TECHS_BY_FAMILY = {
        "cereal": ["Drip irrigation", "Precision planting"],
        "legume": ["Intercropping with cereals", "Mulching"],
        "root": ["Ridging", "Soil moisture monitoring"],
        "vegetable": ["Fertigation system", "Greenhouse/shade-net (if possible)"],
        "oilseed": ["Integrated pest management", "Rotate with legumes"],
        "fiber": ["Irrigation scheduling", "Regular soil testing"],
    }

    @staticmethod
    def suggest_for_crop(crop_name: str):
        fam = CropRotationLogic.CROP_FAMILIES.get(crop_name.lower())
        return TechniqueSuggestion.TECHS_BY_FAMILY.get(fam, ["No specific techniques available."])
