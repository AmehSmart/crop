"""
data.py - Contains agricultural data for crops, soils, and techniques.
"""
from classes import Crop, Soil, FarmingTechnique

# Crops: name, family, recommended soils
CROPS = [
    Crop("Wheat", "cereal", ["Loamy", "Clay"]),
    Crop("Maize", "cereal", ["Loamy", "Sandy"]),
    Crop("Rice", "cereal", ["Clay", "Silty"]),
    Crop("Barley", "cereal", ["Loamy", "Clay"]),
    Crop("Soybean", "legume", ["Loamy", "Sandy"]),
    Crop("Peanut", "legume", ["Sandy", "Loamy"]),
    Crop("Lentil", "legume", ["Loamy", "Sandy"]),
    Crop("Chickpea", "legume", ["Loamy", "Sandy"]),
    Crop("Potato", "root", ["Sandy", "Loamy"]),
    Crop("Cassava", "root", ["Sandy", "Loamy"]),
    Crop("Yam", "root", ["Sandy", "Loamy"]),
    Crop("Carrot", "root", ["Sandy", "Loamy"]),
    Crop("Tomato", "vegetable", ["Loamy", "Sandy"]),
    Crop("Onion", "vegetable", ["Sandy", "Loamy"]),
    Crop("Cabbage", "vegetable", ["Loamy", "Clay"]),
    Crop("Mustard", "vegetable", ["Loamy", "Clay"]),
    Crop("Sunflower", "oilseed", ["Loamy", "Sandy"]),
    Crop("Cotton", "fiber", ["Sandy", "Loamy"]),
]

# Soils: type, properties
SOILS = [
    Soil("Sandy", {"drainage": "fast", "fertility": "low"}),
    Soil("Clay", {"drainage": "slow", "fertility": "high"}),
    Soil("Silty", {"drainage": "moderate", "fertility": "high"}),
    Soil("Peaty", {"drainage": "variable", "fertility": "high", "organic": True}),
    Soil("Chalky", {"drainage": "fast", "fertility": "low", "pH": "alkaline"}),
    Soil("Loamy", {"drainage": "good", "fertility": "high"}),
]

# Modern farming techniques
TECHNIQUES = [
    FarmingTechnique("Drip Irrigation", "Delivers water directly to roots, reducing waste.", ["Sandy", "Loamy", "Clay"]),
    FarmingTechnique("Intercropping", "Two or more crops together for yield + pest control.", ["Loamy", "Sandy", "Clay"]),
    FarmingTechnique("Precision Farming", "Use data/tech to optimize inputs.", ["All"]),
    FarmingTechnique("Cover Cropping", "Cover soil to add fertility and prevent erosion.", ["Loamy", "Sandy", "Peaty"]),
    FarmingTechnique("Mulching", "Surface layer to retain moisture and reduce weeds.", ["Sandy", "Loamy"]),
    FarmingTechnique("Crop Rotation", "Alternate crops to break pest cycles and balance nutrients.", ["All"]),
]
