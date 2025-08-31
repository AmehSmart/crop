from typing import List, Dict

class Crop:
    def __init__(self, name: str, family: str, recommended_soil: List[str]):
        self.name = name
        self.family = family
        self.recommended_soil = recommended_soil

class Soil:
    def __init__(self, soil_type: str, properties: Dict):
        self.soil_type = soil_type
        self.properties = properties

class FarmingTechnique:
    def __init__(self, name: str, description: str, suitable_soil: List[str]):
        self.name = name
        self.description = description
        self.suitable_soil = suitable_soil
