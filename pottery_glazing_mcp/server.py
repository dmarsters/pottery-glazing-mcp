"""FastMCP server for pottery glazing chemistry - Flat structure for cloud compatibility."""

import json
from fastmcp import FastMCP
from pottery_glazing_mcp.glaze_processor import GlazeChemistryProcessor

# Initialize processor
processor = GlazeChemistryProcessor()

# Initialize FastMCP server
server = FastMCP("pottery-glazing-chemistry")


@server.tool()
def analyze_glaze_formulation(
    colorant: str,
    colorant_percentage: float,
    flux_type: str,
    atmosphere: str,
    cone: int,
    runs: bool = False,
) -> str:
    """Analyze a pottery glaze formulation and extract visual parameters for image generation."""
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


@server.tool()
def enhance_image_prompt_from_glaze(
    base_prompt: str,
    colorant: str,
    flux_type: str,
    atmosphere: str,
    cone: int,
) -> str:
    """Enhance an image generation prompt with pottery glaze visual characteristics."""
    try:
        glaze_analysis = processor.analyze_glaze_formulation(
            colorant=colorant,
            colorant_percentage=10.0,
            flux_type=flux_type,
            atmosphere=atmosphere,
            cone=cone,
            runs=False
        )
        
        visual_params = glaze_analysis["visual_parameters"]
        sensory = glaze_analysis["sensory_intention"]
        
        enhancement_parts = []
        
        if visual_params["optical_intensity"] > 7:
            enhancement_parts.append("dark, concentrated optical quality")
        elif visual_params["optical_intensity"] < 4:
            enhancement_parts.append("bright, transparent, luminous quality")
        else:
            enhancement_parts.append("balanced, medium-value optical quality")
        
        if visual_params["reflectivity"] > 8:
            enhancement_parts.append("glossy mirror-like surface")
        elif visual_params["reflectivity"] < 3:
            enhancement_parts.append("matte absorptive surface")
        else:
            enhancement_parts.append("satin semi-gloss surface")
        
        if visual_params["saturation"] > 8:
            enhancement_parts.append("intensely saturated, vivid coloration")
        elif visual_params["saturation"] < 4:
            enhancement_parts.append("subtly tinted, muted coloration")
        else:
            enhancement_parts.append("balanced, clear coloration")
        
        hue_temp = visual_params["hue_temperature"]
        if hue_temp > 7:
            enhancement_parts.append("warm-toned, earthy")
        elif hue_temp < 3:
            enhancement_parts.append("cool-toned, pure")
        else:
            enhancement_parts.append("neutral balanced")
        
        if visual_params["maturation_level"] > 8:
            enhancement_parts.append("fully matured, intentional")
        else:
            enhancement_parts.append("developing, softer edges")
        
        enhancement_parts.append(f"feels {sensory['feels_like']}")
        enhancement_text = "; ".join(enhancement_parts)
        enhanced_prompt = f"{base_prompt} [glaze aesthetic: {enhancement_text}]"
        
        return json.dumps({
            "original_prompt": base_prompt,
            "enhancement_text": enhancement_text,
            "enhanced_prompt": enhanced_prompt
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@server.tool()
def list_available_colorants() -> str:
    """List all available pottery glaze colorants."""
    colorants = {
        "iron": {"description": "Iron oxide", "warmth": 8.0, "character": "earthy"},
        "cobalt": {"description": "Cobalt oxide", "warmth": 1.5, "character": "pure blue"},
        "copper": {"description": "Copper oxide", "warmth": 5.0, "character": "versatile"},
        "chrome": {"description": "Chromium oxide", "warmth": 2.0, "character": "stable green"},
        "manganese": {"description": "Manganese dioxide", "warmth": 1.0, "character": "soft purple"},
        "vanadium": {"description": "Vanadium pentoxide", "warmth": 7.0, "character": "warm yellow"}
    }
    return json.dumps(colorants, indent=2)


@server.tool()
def list_available_fluxes() -> str:
    """List all available flux systems."""
    fluxes = {
        "boron": {"reflectivity": 9.5, "effect": "glossy, luminous"},
        "alkaline": {"reflectivity": 6.0, "effect": "fluid, dynamic"},
        "alkaline_earth": {"reflectivity": 2.5, "effect": "matte, grounded"},
        "lead": {"reflectivity": 8.0, "effect": "glassy, smooth"}
    }
    return json.dumps(fluxes, indent=2)


@server.tool()
def compare_glaze_formulations(glaze1_description: str, glaze2_description: str) -> str:
    """Compare two glaze formulations."""
    return json.dumps({
        "glaze1": glaze1_description,
        "glaze2": glaze2_description,
        "note": "Use analyze_glaze_formulation() for precise parameters"
    })


if __name__ == "__main__":
    server.run()
