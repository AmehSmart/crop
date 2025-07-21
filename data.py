"""
data.py - Contains real agricultural data for crops, soils, and techniques.
"""
from classes import Crop, Soil, FarmingTechnique

# Real crop data: name, family, recommended soils
CROPS = [
    Crop("Wheat", "Poaceae", ["Loamy", "Clay"]),
    Crop("Maize", "Poaceae", ["Loamy", "Sandy"]),
    Crop("Rice", "Poaceae", ["Clay", "Silty"]),
    Crop("Soybean", "Fabaceae", ["Loamy", "Sandy"]),
    Crop("Peanut", "Fabaceae", ["Sandy", "Loamy"]),
    Crop("Potato", "Solanaceae", ["Sandy", "Loamy"]),
    Crop("Tomato", "Solanaceae", ["Loamy", "Sandy"]),
    Crop("Cotton", "Malvaceae", ["Sandy", "Loamy"]),
    Crop("Sunflower", "Asteraceae", ["Loamy", "Sandy"]),
    Crop("Cabbage", "Brassicaceae", ["Loamy", "Clay"]),
    Crop("Carrot", "Apiaceae", ["Sandy", "Loamy"]),
    Crop("Onion", "Amaryllidaceae", ["Sandy", "Loamy"]),
    Crop("Barley", "Poaceae", ["Loamy", "Clay"]),
    Crop("Lentil", "Fabaceae", ["Loamy", "Sandy"]),
    Crop("Chickpea", "Fabaceae", ["Loamy", "Sandy"]),
    Crop("Mustard", "Brassicaceae", ["Loamy", "Clay"]),
]

# Real soil data: type, properties
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
    FarmingTechnique("Drip Irrigation", "Delivers water directly to plant roots, reducing waste.", ["Sandy", "Loamy", "Clay"]),
    FarmingTechnique("Intercropping", "Growing two or more crops together for better yield and pest control.", ["Loamy", "Sandy", "Clay"]),
    FarmingTechnique("Precision Farming", "Uses data and technology to optimize field-level management.", ["All"]),
    FarmingTechnique("Cover Cropping", "Planting crops to cover soil, improve fertility, and prevent erosion.", ["Loamy", "Sandy", "Peaty"]),
    FarmingTechnique("Crop Rotation", "Alternating crops to improve soil health and reduce pests.", ["All"]),
    FarmingTechnique("Mulching", "Applying a layer of material to soil surface to retain moisture.", ["Sandy", "Loamy"]),
]
