"""
Test suite for pottery glazing chemistry processor.

Tests the morphism implementations and composite glaze analysis.
"""

import pytest
import json
from pottery_glazing_mcp.glaze_processor import GlazeChemistryProcessor


@pytest.fixture
def processor():
    """Provide initialized processor for tests."""
    return GlazeChemistryProcessor()


class TestAtmosphereMorphism:
    """Test atmosphere → color modulation morphism."""
    
    def test_reduction_intensifies_color(self, processor):
        """Reduction should increase optical intensity and saturation."""
        intensity, sat_mod, hue_shift = processor.apply_atmosphere_morphism(
            "copper", "reduction"
        )
        
        assert intensity > 7.0, "Reduction should create dark intensity"
        assert sat_mod > 1.0, "Reduction should increase saturation"
        assert hue_shift < 0, "Copper under reduction should shift toward red"
    
    def test_oxidation_lightens_color(self, processor):
        """Oxidation should decrease optical intensity."""
        intensity, sat_mod, hue_shift = processor.apply_atmosphere_morphism(
            "copper", "oxidation"
        )
        
        assert intensity < 5.0, "Oxidation should create lighter intensity"
        assert sat_mod < 1.0, "Oxidation should decrease saturation"
        assert hue_shift > 0, "Copper under oxidation should shift toward blue"
    
    def test_neutral_atmosphere_balanced(self, processor):
        """Neutral atmosphere should produce balanced parameters."""
        intensity, sat_mod, hue_shift = processor.apply_atmosphere_morphism(
            "iron", "neutral"
        )
        
        assert 5.0 < intensity < 6.5, "Neutral should be balanced"
        assert sat_mod == 1.0, "Neutral should have no saturation modifier"


class TestFluxMorphism:
    """Test flux behavior → surface texture morphism."""
    
    def test_boron_creates_gloss(self, processor):
        """Boron should create high reflectivity."""
        reflectivity, description = processor.apply_flux_morphism("boron")
        
        assert reflectivity > 9.0, "Boron should be highly reflective"
        assert "gloss" in description.lower() or "mirror" in description.lower()
    
    def test_alkaline_earth_creates_matte(self, processor):
        """Alkaline earth should create low reflectivity."""
        reflectivity, description = processor.apply_flux_morphism("alkaline_earth")
        
        assert reflectivity < 3.0, "Alkaline earth should be matte"
        assert "matte" in description.lower() or "absorb" in description.lower()
    
    def test_alkaline_creates_satin(self, processor):
        """Alkaline flux should create medium reflectivity."""
        reflectivity, description = processor.apply_flux_morphism("alkaline")
        
        assert 5.0 < reflectivity < 7.0, "Alkaline should be satin"


class TestTemperatureMorphism:
    """Test temperature → glaze maturation morphism."""
    
    def test_low_fire_immature(self, processor):
        """Low fire should produce lower maturation."""
        maturation, crystallinity = processor.apply_temperature_morphism(2)
        
        assert maturation < 5.0, "Low fire should be immature"
        assert crystallinity < 3.0, "Low fire should have minimal crystallinity"
    
    def test_mid_fire_balanced(self, processor):
        """Mid fire should produce balanced maturation."""
        maturation, crystallinity = processor.apply_temperature_morphism(6)
        
        assert 6.5 < maturation < 7.5, "Mid fire should be well-matured"
        assert 3.0 < crystallinity < 5.0, "Mid fire should have moderate crystallinity"
    
    def test_high_fire_mature(self, processor):
        """High fire should produce full maturation."""
        maturation, crystallinity = processor.apply_temperature_morphism(13)
        
        assert maturation > 9.0, "High fire should be fully mature"
        assert crystallinity > 7.0, "High fire should develop crystals"


class TestColorantMorphism:
    """Test colorant chemistry → visual effect morphism."""
    
    def test_cobalt_pure_cool(self, processor):
        """Cobalt should be pure, cool, intense."""
        profile = processor.apply_colorant_morphism("cobalt")
        
        assert profile["hue_temperature"] < 3.0, "Cobalt should be cool"
        assert profile["color_purity"] > 8.5, "Cobalt should be pure"
        assert profile["characteristic_intensity"] > 8.0, "Cobalt should be intense"
    
    def test_iron_warm_earthy(self, processor):
        """Iron should be warm and earthy."""
        profile = processor.apply_colorant_morphism("iron")
        
        assert profile["hue_temperature"] > 7.0, "Iron should be warm"
        assert "earth" in profile["description"].lower()
    
    def test_chrome_stable_green(self, processor):
        """Chrome should be stable and mineral-like."""
        profile = processor.apply_colorant_morphism("chrome")
        
        assert profile["hue_temperature"] < 3.0, "Chrome should be cool"
        assert "mineral" in profile["description"].lower() or "stable" in profile["description"].lower()


class TestCompositeGlazeAnalysis:
    """Test composite morphism: full glaze analysis."""
    
    def test_reduction_cobalt_boron_high_fire(self, processor):
        """Analyze a classic deep blue reduction glaze."""
        result = processor.analyze_glaze_formulation(
            colorant="cobalt",
            colorant_percentage=2.0,  # Typical cobalt amount for saturated blue
            flux_type="boron",
            atmosphere="reduction",
            cone=10,
            runs=False
        )
        
        # Should produce: deep, intense, glossy blue
        params = result["visual_parameters"]
        assert params["optical_intensity"] > 7.0, "Should be dark"
        assert params["saturation"] > 7.5, "Should be highly saturated"
        assert params["reflectivity"] > 9.0, "Should be glossy"
        assert params["hue_temperature"] < 3.0, "Should be cool"
        assert "mystery" in result["sensory_intention"]["feels_like"].lower() or \
               "concentrated" in result["sensory_intention"]["feels_like"].lower()
    
    def test_oxidation_iron_alkaline_earth_mid_fire(self, processor):
        """Analyze an earthy matte iron glaze."""
        result = processor.analyze_glaze_formulation(
            colorant="iron",
            colorant_percentage=8.0,
            flux_type="alkaline_earth",
            atmosphere="oxidation",
            cone=6,
            runs=False
        )
        
        # Should produce: earthy, matte, warm brown
        params = result["visual_parameters"]
        assert params["reflectivity"] < 4.0, "Should be matte"
        assert params["hue_temperature"] > 7.0, "Should be warm"
        assert "earth" in result["descriptive_qualities"]["colorant_character"].lower()
    
    def test_running_glaze_increases_flow(self, processor):
        """Glaze marked as running should have higher flow intensity."""
        non_running = processor.analyze_glaze_formulation(
            colorant="cobalt",
            colorant_percentage=2.0,
            flux_type="boron",
            atmosphere="oxidation",
            cone=6,
            runs=False
        )
        
        running = processor.analyze_glaze_formulation(
            colorant="cobalt",
            colorant_percentage=2.0,
            flux_type="boron",
            atmosphere="oxidation",
            cone=6,
            runs=True
        )
        
        assert running["visual_parameters"]["surface_flow"] > \
               non_running["visual_parameters"]["surface_flow"], \
               "Running glaze should have higher flow"
    
    def test_saturation_scales_with_colorant_amount(self, processor):
        """More colorant should produce higher saturation."""
        low_amount = processor.analyze_glaze_formulation(
            colorant="cobalt",
            colorant_percentage=0.5,
            flux_type="boron",
            atmosphere="oxidation",
            cone=6,
        )
        
        high_amount = processor.analyze_glaze_formulation(
            colorant="cobalt",
            colorant_percentage=2.0,
            flux_type="boron",
            atmosphere="oxidation",
            cone=6,
        )
        
        assert high_amount["visual_parameters"]["saturation"] > \
               low_amount["visual_parameters"]["saturation"], \
               "More colorant should increase saturation"
    
    def test_temperature_increases_maturation(self, processor):
        """Higher firing temperature should increase maturation."""
        mid_fire = processor.analyze_glaze_formulation(
            colorant="cobalt",
            colorant_percentage=1.0,
            flux_type="boron",
            atmosphere="oxidation",
            cone=6,
        )
        
        high_fire = processor.analyze_glaze_formulation(
            colorant="cobalt",
            colorant_percentage=1.0,
            flux_type="boron",
            atmosphere="oxidation",
            cone=10,
        )
        
        assert high_fire["visual_parameters"]["maturation_level"] > \
               mid_fire["visual_parameters"]["maturation_level"], \
               "Higher cone should increase maturation"


class TestParameterRanges:
    """Test that all parameters stay within valid ranges."""
    
    def test_optical_intensity_in_range(self, processor):
        """Optical intensity should always be 0-10."""
        for colorant in ["iron", "cobalt", "copper"]:
            for atm in ["oxidation", "reduction"]:
                intensity, _, _ = processor.apply_atmosphere_morphism(colorant, atm)
                assert 0 <= intensity <= 10, f"{colorant} {atm} intensity out of range"
    
    def test_saturation_capped_at_10(self, processor):
        """Saturation should never exceed 10."""
        result = processor.analyze_glaze_formulation(
            colorant="cobalt",
            colorant_percentage=15.0,  # Unrealistic amount
            flux_type="boron",
            atmosphere="reduction",
            cone=13,
        )
        assert result["visual_parameters"]["saturation"] <= 10.0


class TestJSONSerialization:
    """Test that results are JSON-serializable."""
    
    def test_analysis_is_json_serializable(self, processor):
        """Analysis results should serialize to JSON without error."""
        result = processor.analyze_glaze_formulation(
            colorant="copper",
            colorant_percentage=8.0,
            flux_type="alkaline",
            atmosphere="reduction",
            cone=10,
        )
        
        # Should not raise
        json_str = json.dumps(result)
        parsed = json.loads(json_str)
        
        assert parsed["visual_parameters"]["optical_intensity"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
