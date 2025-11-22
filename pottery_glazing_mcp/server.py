"""
Pottery Glazing Chemistry MCP Server

Exposes glaze chemistry analysis and image prompt enhancement as MCP tools.
"""

import json
from mcp import Server
from pottery_glazing_mcp.glaze_processor import GlazeChemistryProcessor

# Initialize processor
processor = GlazeChemistryProcessor()

# Initialize MCP server
mcp = Server("pottery-glazing-chemistry")


@mcp.tool()
def analyze_glaze_formulation(
    colorant: str,
    colorant_percentage: float,
    flux_type: str,
    atmosphere: str,
    cone: int,
    runs: bool = False,
) -> str:
    """
    Analyze a pottery glaze formulation and extract visual parameters for image generation.
    
    This tool implements the composite morphism from the pottery glazing olog:
    ColorDevelopment × FluxBehavior × FiringAtmosphere × TemperatureRange → GlazeEffect
    
    Args:
        colorant: Metal oxide colorant type. Options: iron, cobalt, copper, chrome, manganese, vanadium
        colorant_percentage: Percentage of colorant in formulation (typically 5-15%)
        flux_type: Primary flux system. Options: boron, alkaline, alkaline_earth, lead
        atmosphere: Kiln atmosphere. Options: oxidation, reduction, neutral
        cone: Firing temperature as cone number (06 to 13, use number only, e.g., 6 or 10)
        runs: Whether the glaze is formulated to run and pool (affects flow parameters)
    
    Returns:
        JSON string with visual parameters, descriptive qualities, and sensory intentions
        ready for image generation prompt enhancement.
    
    Example:
        Analyzing a reduction copper glaze with boron flux at cone 10:
        - Returns optical_intensity: 8.5 (dark, concentrated)
        - Returns saturation: ~8.0 (deep color)
        - Returns reflectivity: 9.5 (glossy boron surface)
        - Sensory: "mysterious, concentrated, sultry; luminous and flowing"
    """
    try:
        result = processor.analyze_glaze_formulation(
            colorant=colorant,
            colorant_percentage=colorant_percentage,
            flux_type=flux_type,
            atmosphere=atmosphere,
            cone=cone,
            runs=runs
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def enhance_image_prompt_from_glaze(
    base_prompt: str,
    colorant: str,
    flux_type: str,
    atmosphere: str,
    cone: int,
) -> str:
    """
    Enhance an image generation prompt with pottery glaze visual characteristics.
    
    Takes a base image prompt and weaves in the visual sensibilities of a specific
    glaze formulation. The enhancement preserves the original subject while infusing
    the aesthetic qualities of the pottery glaze.
    
    Args:
        base_prompt: Original image generation prompt (e.g., "a ceramic vase on a shelf")
        colorant: Metal oxide colorant (iron, cobalt, copper, chrome, manganese, vanadium)
        flux_type: Flux system (boron, alkaline, alkaline_earth, lead)
        atmosphere: Firing atmosphere (oxidation, reduction, neutral)
        cone: Firing cone number
    
    Returns:
        Enhanced prompt incorporating glaze visual qualities without making the image
        "about" glazes—just infused with their aesthetic sensibility.
    
    Example:
        Input: "a ceramic vase on a shelf"
        Glaze: Reduction cobalt, boron flux, cone 10
        Output might include: "...glossy luminous surface with deep saturated blue,
        mysterious concentrated quality, mirror-like reflectivity..."
    """
    try:
        glaze_analysis = processor.analyze_glaze_formulation(
            colorant=colorant,
            colorant_percentage=10.0,  # Assume typical amount
            flux_type=flux_type,
            atmosphere=atmosphere,
            cone=cone,
            runs=False
        )
        
        visual_params = glaze_analysis["visual_parameters"]
        descriptive = glaze_analysis["descriptive_qualities"]
        sensory = glaze_analysis["sensory_intention"]
        
        # Build enhancement based on glaze characteristics
        enhancement_parts = []
        
        # Optical quality
        if visual_params["optical_intensity"] > 7:
            enhancement_parts.append("dark, concentrated optical quality")
        elif visual_params["optical_intensity"] < 4:
            enhancement_parts.append("bright, transparent, luminous quality")
        else:
            enhancement_parts.append("balanced, medium-value optical quality")
        
        # Surface finish
        if visual_params["reflectivity"] > 8:
            enhancement_parts.append("glossy mirror-like surface with strong light reflection")
        elif visual_params["reflectivity"] < 3:
            enhancement_parts.append("matte absorptive surface with diffuse light")
        else:
            enhancement_parts.append("satin semi-gloss surface")
        
        # Color saturation
        if visual_params["saturation"] > 8:
            enhancement_parts.append("intensely saturated, vivid coloration")
        elif visual_params["saturation"] < 4:
            enhancement_parts.append("subtly tinted, muted coloration")
        else:
            enhancement_parts.append("balanced, clear coloration")
        
        # Hue quality
        hue_temp = visual_params["hue_temperature"]
        if hue_temp > 7:
            enhancement_parts.append("warm-toned, earthy character")
        elif hue_temp < 3:
            enhancement_parts.append("cool-toned, pure character")
        else:
            enhancement_parts.append("neutral balanced coloration")
        
        # Maturation
        if visual_params["maturation_level"] > 8:
            enhancement_parts.append("fully matured, intentional finish")
        else:
            enhancement_parts.append("developing, slightly softer edges")
        
        # Sensory intention phrase
        enhancement_parts.append(f"feels {sensory['feels_like']}")
        
        # Assemble into coherent enhancement
        enhancement_text = "; ".join(enhancement_parts)
        
        enhanced_prompt = f"{base_prompt} [glaze aesthetic: {enhancement_text}]"
        
        return json.dumps({
            "original_prompt": base_prompt,
            "glaze_analysis": glaze_analysis,
            "enhancement_text": enhancement_text,
            "enhanced_prompt": enhanced_prompt,
            "usage_note": "Use 'enhanced_prompt' directly with image generators, or extract 'enhancement_text' to blend manually"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def list_available_colorants() -> str:
    """
    List all available pottery glaze colorants and their visual characteristics.
    
    Returns a comprehensive list of supported metal oxide colorants with their
    characteristic visual properties, atmosphere responses, and typical usage notes.
    """
    colorants = {
        "iron": {
            "description": "Iron oxide (Fe₂O₃/Fe₃O₄)",
            "visual_character": "earthy, warm, natural-feeling",
            "under_oxidation": "yellows, browns, reds",
            "under_reduction": "blacks, dark greens, blacks with brown edges",
            "typical_percentage": "5-8%",
            "warmth_score": 8.0,
            "note": "Most versatile, historically important colorant"
        },
        "cobalt": {
            "description": "Cobalt oxide (CoO)",
            "visual_character": "pure intense blue, jewel-like",
            "under_oxidation": "clear, pure blues",
            "under_reduction": "deep purples, darker blues with mystery",
            "typical_percentage": "0.5-2%",
            "warmth_score": 1.5,
            "note": "Strongest colorant, potent even in small amounts"
        },
        "copper": {
            "description": "Copper oxide (CuO/Cu₂O)",
            "visual_character": "versatile, atmosphere-responsive",
            "under_oxidation": "greens, blue-greens, turquoise",
            "under_reduction": "deep reds, black-reds, copper metallic",
            "typical_percentage": "5-10%",
            "warmth_score": 5.0,
            "note": "Most atmosphere-sensitive, dramatic shifts possible"
        },
        "chrome": {
            "description": "Chromium oxide (Cr₂O₃)",
            "visual_character": "stable mineral green, environmental",
            "under_oxidation": "greens, olive greens",
            "under_reduction": "greens (remains stable)",
            "typical_percentage": "5-8%",
            "warmth_score": 2.0,
            "note": "Stable, doesn't shift under atmosphere changes"
        },
        "manganese": {
            "description": "Manganese dioxide (MnO₂)",
            "visual_character": "soft purple-brown, muted, organic",
            "under_oxidation": "browns, purples, browns with purple tint",
            "under_reduction": "darker browns, purples, near-black",
            "typical_percentage": "3-8%",
            "warmth_score": 1.0,
            "note": "Produces subtle colors, good for blending"
        },
        "vanadium": {
            "description": "Vanadium pentoxide (V₂O₅)",
            "visual_character": "warm yellow, slightly muted, rare",
            "under_oxidation": "yellows, yellow-greens",
            "under_reduction": "yellows, warm browns",
            "typical_percentage": "5-10%",
            "warmth_score": 7.0,
            "note": "Rare, expensive, produces unique warm tones"
        }
    }
    
    return json.dumps(colorants, indent=2)


@mcp.tool()
def list_available_fluxes() -> str:
    """
    List all available pottery glaze flux systems and their surface characteristics.
    
    Returns information about flux types, their melt behaviors, surface finishes,
    and visual effects on glazed ware.
    """
    fluxes = {
        "boron": {
            "chemistry": "Boron oxide (B₂O₃), usually from borax or boric acid",
            "melting_behavior": "Creates glassy, fluid melts with strong surface tension reduction",
            "surface_finish": "Glossy, mirror-like, highly reflective",
            "reflectivity_score": 9.5,
            "running_behavior": "Moderate to high—runs easily on vertical surfaces",
            "typical_use": "For glossy surfaces, color clarity, smooth finishes",
            "cone_range": "Any, but especially effective mid-fire (cone 5-6)",
            "visual_effect": "luminous and flowing, mirror-like luminosity",
            "note": "Creates the brightest, glossiest surfaces"
        },
        "alkaline": {
            "chemistry": "Soda (Na₂O), potassium (K₂O), or soda ash",
            "melting_behavior": "Creates fluid, flowing melts; viscosity varies with amount",
            "surface_finish": "Satin to semi-gloss, somewhat fluid",
            "reflectivity_score": 6.0,
            "running_behavior": "High—glazes will run and pool at edges",
            "typical_use": "For dynamic, running glazes; creates pooling effects",
            "cone_range": "Mid to high fire (cone 5 and up)",
            "visual_effect": "fluid and dynamic, gravity-affected flowing",
            "note": "Creates intentional runs and pooling; dramatic edge effects"
        },
        "alkaline_earth": {
            "chemistry": "Calcium (CaO), magnesium (MgO), strontium (SrO)",
            "melting_behavior": "Creates stiffer melts; limited fluidity",
            "surface_finish": "Matte, semi-matte, absorptive",
            "reflectivity_score": 2.5,
            "running_behavior": "Low—stays where applied, minimal running",
            "typical_use": "For matte surfaces, natural textures, earthy feel",
            "cone_range": "Mid to high fire (cone 5-13)",
            "visual_effect": "stable and grounded, light-absorbing",
            "note": "Creates most natural, earthy finishes"
        },
        "lead": {
            "chemistry": "Lead oxide (PbO) - use in tested commercial glazes only",
            "melting_behavior": "Creates smooth, glassy melts; very fluid",
            "surface_finish": "Glassy, smooth, luminous",
            "reflectivity_score": 8.0,
            "running_behavior": "Moderate—flows smoothly but controlled",
            "typical_use": "Historic glazes, functional ware (food-safe when tested)",
            "cone_range": "Low to mid fire (cone 06-2)",
            "visual_effect": "smooth and glassy, refined luminosity",
            "note": "Historically important; modern use requires safety testing. Not typically used in studio practice anymore."
        }
    }
    
    return json.dumps(fluxes, indent=2)


@mcp.tool()
def compare_glaze_formulations(
    glaze1_description: str,
    glaze2_description: str,
) -> str:
    """
    Compare two glaze formulations conceptually and describe visual differences.
    
    This tool accepts natural language descriptions of glazes and provides a
    qualitative comparison of their visual effects and sensory intentions.
    
    Args:
        glaze1_description: Description of first glaze (e.g., "reduction copper boron flux cone 10")
        glaze2_description: Description of second glaze (e.g., "oxidation iron alkaline earth cone 6")
    
    Returns:
        Comparison highlighting visual differences, sensory qualities, and intended effects.
    
    Note:
        This is a qualitative analysis tool. For precise parameter values, use
        analyze_glaze_formulation() with explicit colorant/flux/atmosphere specifications.
    """
    comparison = f"""
Glaze Comparison: Qualitative Analysis

Glaze 1: {glaze1_description}
Glaze 2: {glaze2_description}

This comparison tool provides qualitative sensory analysis. For precise visual parameters,
please use analyze_glaze_formulation() with explicit chemistry specifications:
- specify colorant (iron, cobalt, copper, chrome, manganese, vanadium)
- specify flux_type (boron, alkaline, alkaline_earth, lead)
- specify atmosphere (oxidation, reduction, neutral)
- specify cone number

The comparison highlights how different chemistry choices create different sensory intentions:
- Reduction vs oxidation: dramatic hue/saturation shifts
- Boron vs alkaline earth: gloss vs matte spectrum
- Iron vs cobalt: warm vs cool color character
- High fire vs mid fire: maturation and crystalline effects

Provide formulation details for quantitative analysis.
    """
    
    return json.dumps({
        "analysis": comparison,
        "recommendation": "Use analyze_glaze_formulation() for precise parameter extraction"
    })


if __name__ == "__main__":
    mcp.run()
