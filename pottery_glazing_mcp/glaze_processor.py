"""
Pottery Glazing Chemistry Processor

Converts glaze chemistry specifications into visual image generation parameters.
"""

from typing import Dict, Tuple
import yaml
import os


class GlazeChemistryProcessor:
    """
    Processes glaze chemistry formulations and maps them to visual parameters.
    
    Coordinates between three domains:
    - Glaze chemistry (colorants, fluxes, atmosphere, temperature)
    - Visual intentions (saturation, gloss, flow, maturation)
    - Image generation parameters (specific prompt enhancements)
    """
    
    def __init__(self):
        """Initialize the processor with olog definitions."""
        self.olog = self._load_olog()
        
    def _load_olog(self) -> Dict:
        """Load the categorical structure olog."""
        # Load from package directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        olog_path = os.path.join(current_dir, "glazing_olog.yaml")
        
        with open(olog_path, 'r') as f:
            return yaml.safe_load(f)
    
    # ========== MORPHISM IMPLEMENTATIONS ==========
    # These implement the categorical morphisms from the olog
    
    def apply_atmosphere_morphism(
        self, 
        colorant: str, 
        atmosphere: str
    ) -> Tuple[float, float, float]:
        """
        Morphism: Atmosphere → ColorModulation
        
        Transforms colorant hue/saturation based on firing atmosphere.
        Returns: (optical_intensity, saturation_modifier, hue_shift)
        """
        base_saturation = self._get_colorant_base_saturation(colorant)
        
        if atmosphere.lower() == "reduction":
            # Reduction: increase saturation, darken value, add mystery
            optical_intensity = 8.5  # Dark, concentrated
            saturation_modifier = 1.3  # 30% more saturated
            hue_shift = self._get_reduction_hue_shift(colorant)
        elif atmosphere.lower() == "oxidation":
            # Oxidation: decrease saturation, lighten value, add clarity
            optical_intensity = 4.0  # Bright, transparent
            saturation_modifier = 0.7  # 30% less saturated
            hue_shift = self._get_oxidation_hue_shift(colorant)
        else:  # neutral
            optical_intensity = 5.5
            saturation_modifier = 1.0
            hue_shift = 0
        
        return (optical_intensity, saturation_modifier, hue_shift)
    
    def apply_flux_morphism(self, flux_type: str) -> Tuple[float, str]:
        """
        Morphism: FluxBehavior → SurfaceTexture
        
        Maps flux type to reflectivity and surface characteristics.
        Returns: (reflectivity_0_to_10, surface_description)
        """
        flux_profiles = {
            "boron": (9.5, "glossy, mirror-like, highly reflective"),
            "alkaline": (6.0, "satin, fluid, slight matte"),
            "alkaline_earth": (2.5, "matte, absorptive, grounded"),
            "lead": (8.0, "glassy, smooth, luminous"),  # deprecated but historically important
        }
        
        profile = flux_profiles.get(flux_type.lower(), (5.0, "balanced"))
        return profile
    
    def apply_temperature_morphism(self, cone: int) -> Tuple[float, float]:
        """
        Morphism: TemperatureRange → GlazeMaturation
        
        Maps firing temperature (cone number) to maturation and crystallinity.
        Returns: (maturation_level_0_to_10, crystalline_definition_0_to_10)
        """
        # Cone temperature effects
        if cone <= 2:  # Low fire
            maturation = 3.5
            crystallinity = 1.0
        elif cone <= 6:  # Mid fire (most common)
            maturation = 7.0
            crystallinity = 4.0
        else:  # High fire
            maturation = 9.5
            crystallinity = 8.0
        
        return (maturation, crystallinity)
    
    def apply_colorant_morphism(self, colorant: str) -> Dict[str, float]:
        """
        Morphism: ColorDevelopment → VisualEffect
        
        Maps colorant chemistry to characteristic visual qualities.
        Returns dict with hue_temperature (warm/cool), color_purity, characteristic_intensity
        """
        colorant_profiles = {
            "iron": {
                "hue_temperature": 8.0,  # Very warm (brown-red range)
                "color_purity": 6.0,  # Earthy, slightly muted
                "characteristic_intensity": 6.5,
                "description": "earthy, natural, warm depth"
            },
            "cobalt": {
                "hue_temperature": 1.5,  # Very cool (pure blue)
                "color_purity": 9.0,  # Pure, jewel-like
                "characteristic_intensity": 8.5,
                "description": "intense blue, pure, gem-like"
            },
            "copper": {
                "hue_temperature": 5.0,  # Neutral but atmosphere-responsive
                "color_purity": 8.0,  # Responsive, can be very pure
                "characteristic_intensity": 8.0,
                "description": "versatile, responds dramatically to atmosphere"
            },
            "chrome": {
                "hue_temperature": 2.0,  # Cool green
                "color_purity": 7.0,  # Stable, mineral-like
                "characteristic_intensity": 7.0,
                "description": "stable green, mineral quality"
            },
            "manganese": {
                "hue_temperature": 1.0,  # Cool purple-brown
                "color_purity": 5.0,  # Muted, soft
                "characteristic_intensity": 5.5,
                "description": "soft purple-brown, muted, organic"
            },
            "vanadium": {
                "hue_temperature": 7.0,  # Warm yellow-green
                "color_purity": 6.5,  # Slightly muted
                "characteristic_intensity": 6.0,
                "description": "warm yellow, slightly muted, rare"
            },
        }
        
        return colorant_profiles.get(colorant.lower(), {
            "hue_temperature": 5.0,
            "color_purity": 5.0,
            "characteristic_intensity": 5.0,
            "description": "unknown colorant, assumed neutral"
        })
    
    # ========== HELPER METHODS ==========
    
    def _get_colorant_base_saturation(self, colorant: str) -> float:
        """Get base saturation for a colorant before atmosphere modification."""
        base = {
            "iron": 6.5,
            "cobalt": 8.5,
            "copper": 8.0,
            "chrome": 7.0,
            "manganese": 5.5,
            "vanadium": 6.0,
        }
        return base.get(colorant.lower(), 6.0)
    
    def _get_reduction_hue_shift(self, colorant: str) -> float:
        """Get hue shift under reduction atmosphere."""
        shifts = {
            "copper": -15,      # Shift toward red
            "iron": -8,         # Shift toward black
            "cobalt": -5,       # Shift slightly purple
            "chrome": 0,        # Stable
            "manganese": 3,     # Slight shift
            "vanadium": -10,    # Shift toward yellow-brown
        }
        return shifts.get(colorant.lower(), 0)
    
    def _get_oxidation_hue_shift(self, colorant: str) -> float:
        """Get hue shift under oxidation atmosphere."""
        shifts = {
            "copper": 5,        # Shift toward blue
            "iron": 8,          # Shift toward yellow-brown
            "cobalt": 2,        # Slight shift toward pure blue
            "chrome": 0,        # Stable
            "manganese": -3,    # Slight shift
            "vanadium": 5,      # Shift toward yellow
        }
        return shifts.get(colorant.lower(), 0)
    
    # ========== COMPOSITE GLAZE ANALYSIS ==========
    
    def analyze_glaze_formulation(
        self,
        colorant: str,
        colorant_percentage: float,
        flux_type: str,
        atmosphere: str,
        cone: int,
        runs: bool = False,
    ) -> Dict[str, any]:
        """
        Composite morphism: analyze complete glaze formulation.
        
        Combines all individual morphisms to produce unified visual parameter set.
        
        Args:
            colorant: Type of metal oxide colorant
            colorant_percentage: Amount of colorant (0-100, but typically 5-15%)
            flux_type: Primary flux system (boron, alkaline, alkaline_earth, lead)
            atmosphere: Firing atmosphere (oxidation, reduction, neutral)
            cone: Cone temperature (06 to 13, represented as number)
            runs: Whether glaze is formulated to run
        
        Returns:
            Dictionary of visual parameters ready for image generation
        """
        # Apply individual morphisms
        opt_intensity, sat_mod, hue_shift = self.apply_atmosphere_morphism(colorant, atmosphere)
        reflectivity, surface_desc = self.apply_flux_morphism(flux_type)
        maturation, crystallinity = self.apply_temperature_morphism(cone)
        colorant_profile = self.apply_colorant_morphism(colorant)
        
        # Composite saturation: base saturation modified by atmosphere, maturation, and amount
        # Even small colorant amounts can produce saturated color in reduction
        base_sat = self._get_colorant_base_saturation(colorant)
        # Amount factor: typically 0.5-2% for cobalt, 5-15% for others
        # Normalize: typical range gives 1.0 multiplier at upper typical amount
        typical_amount = 8.0  # Reference amount
        amount_factor = 0.3 + (min(colorant_percentage / typical_amount, 1.5) * 0.7)
        
        # Atmosphere multiplier already encoded in sat_mod
        maturation_boost = (maturation / 10.0) * 0.3  # Up to 0.3 boost
        
        final_saturation = (base_sat * sat_mod * amount_factor) + (base_sat * maturation_boost)
        final_saturation = min(final_saturation, 10.0)  # Cap at 10
        
        # Flow behavior
        if runs:
            flow_intensity = reflectivity * 0.8  # Fluid fluxes run more
        else:
            flow_intensity = reflectivity * 0.2  # Matte fluxes don't run
        
        return {
            "glaze_name": f"{atmosphere.capitalize()} {colorant.capitalize()}",
            "visual_parameters": {
                "optical_intensity": round(opt_intensity, 1),
                "saturation": round(final_saturation, 1),
                "reflectivity": round(reflectivity, 1),
                "hue_temperature": round(colorant_profile["hue_temperature"], 1),
                "maturation_level": round(maturation, 1),
                "crystalline_definition": round(crystallinity, 1),
                "surface_flow": round(flow_intensity, 1),
            },
            "descriptive_qualities": {
                "atmosphere_effect": f"{atmosphere} firing",
                "surface_texture": surface_desc,
                "colorant_character": colorant_profile["description"],
                "overall_impression": self._generate_impression(
                    opt_intensity, final_saturation, reflectivity, maturation
                ),
            },
            "sensory_intention": {
                "feels_like": self._sensory_intention(
                    atmosphere, flux_type, colorant, opt_intensity, reflectivity
                ),
                "visual_mood": self._visual_mood(opt_intensity, final_saturation),
            }
        }
    
    def _generate_impression(
        self, 
        intensity: float, 
        saturation: float, 
        reflectivity: float, 
        maturation: float
    ) -> str:
        """Generate descriptive impression of the glaze."""
        if intensity > 7 and saturation > 7:
            mood = "deep and saturated"
        elif intensity < 4 and saturation < 5:
            mood = "bright and delicate"
        elif reflectivity > 8:
            mood = "luminous and reflective"
        elif reflectivity < 3:
            mood = "matte and earthy"
        else:
            mood = "balanced and intentional"
        
        maturity = "fully developed" if maturation > 8 else "well-matured" if maturation > 6 else "developing"
        
        return f"{mood}, {maturity}"
    
    def _sensory_intention(
        self, 
        atmosphere: str, 
        flux_type: str, 
        colorant: str,
        intensity: float,
        reflectivity: float
    ) -> str:
        """Describe what sensory intention this glaze embodies."""
        atmosphere_intent = {
            "reduction": "mysterious, concentrated, sultry",
            "oxidation": "clear, bright, direct",
            "neutral": "balanced, stable"
        }
        
        flux_intent = {
            "boron": "luminous and flowing",
            "alkaline": "fluid and dynamic",
            "alkaline_earth": "stable and grounded",
            "lead": "smooth and glassy"
        }
        
        return f"{atmosphere_intent.get(atmosphere.lower(), 'undefined')}; {flux_intent.get(flux_type.lower(), 'undefined')}"
    
    def _visual_mood(self, intensity: float, saturation: float) -> str:
        """Describe the visual mood."""
        if intensity > 7:
            intensity_mood = "dark"
        elif intensity < 4:
            intensity_mood = "light"
        else:
            intensity_mood = "medium"
        
        if saturation > 8:
            saturation_mood = "highly saturated"
        elif saturation < 4:
            saturation_mood = "muted"
        else:
            saturation_mood = "balanced"
        
        return f"{intensity_mood}, {saturation_mood}"