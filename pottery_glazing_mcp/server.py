"""
Pottery Glazing Chemistry MCP Server

Exposes glaze chemistry analysis and image prompt enhancement as MCP tools.
"""

import json
from mcp.server import Server
from mcp.types import Tool, TextContent
from pottery_glazing_mcp.glaze_processor import GlazeChemistryProcessor

# Initialize processor
processor = GlazeChemistryProcessor()

# Initialize MCP server
mcp = Server("pottery-glazing-chemistry")


@mcp.call_tool()
async def call_tool(name: str, arguments: dict) -> str:
    """Handle tool calls."""
    
    if name == "analyze_glaze_formulation":
        return analyze_glaze_formulation(**arguments)
    elif name == "enhance_image_prompt_from_glaze":
        return enhance_image_prompt_from_glaze(**arguments)
    elif name == "list_available_colorants":
        return list_available_colorants()
    elif name == "list_available_fluxes":
        return list_available_fluxes()
    elif name == "compare_glaze_formulations":
        return compare_glaze_formulations(**arguments)
    else:
        return json.dumps({"error": f"Unknown tool: {name}"})


@mcp.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="analyze_glaze_formulation",
            description="Analyze a pottery glaze formulation and extract visual parameters for image generation",
            inputSchema={
                "type": "object",
                "properties": {
                    "colorant": {
                        "type": "string",
                        "description": "Metal oxide colorant (iron, cobalt, copper, chrome, manganese, vanadium)"
                    },
                    "colorant_percentage": {
                        "type": "number",
                        "description": "Percentage of colorant in formulation"
                    },
                    "flux_type": {
                        "type": "string",
                        "description": "Flux system (boron, alkaline, alkaline_earth, lead)"
                    },
                    "atmosphere": {
                        "type": "string",
                        "description": "Firing atmosphere (oxidation, reduction, neutral)"
                    },
                    "cone": {
                        "type": "integer",
                        "description": "Firing cone number"
                    },
                    "runs": {
                        "type": "boolean",
                        "description": "Whether glaze runs"
                    }
                },
                "required": ["colorant", "colorant_percentage", "flux_type", "atmosphere", "cone"]
            }
        ),
        Tool(
            name="enhance_image_prompt_from_glaze",
            description="Enhance an image prompt with glaze visual characteristics",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_prompt": {"type": "string", "description": "Original image prompt"},
                    "colorant": {"type": "string", "description": "Metal oxide colorant"},
                    "flux_type": {"type": "string", "description": "Flux system"},
                    "atmosphere": {"type": "string", "description": "Firing atmosphere"},
                    "cone": {"type": "integer", "description": "Firing cone"}
                },
                "required": ["base_prompt", "colorant", "flux_type", "atmosphere", "cone"]
            }
        ),
        Tool(
            name="list_available_colorants",
            description="List all available pottery glaze colorants",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="list_available_fluxes",
            description="List all available flux systems",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="compare_glaze_formulations",
            description="Compare two glaze formulations",
            inputSchema={
                "type": "object",
                "properties": {
                    "glaze1_description": {"type": "string"},
                    "glaze2_description": {"type": "string"}
                },
                "required": ["glaze1_description", "glaze2_description"]
            }
        )
    ]


def analyze_glaze_formulation(
    colorant: str,
    colorant_percentage: float,
    flux_type: str,
    atmosphere: str,
    cone: int,
    runs: bool = False,
) -> str:
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


def enhance_image_prompt_from_glaze(
    base_prompt: str,
    colorant: str,
    flux_type: str,
    atmosphere: str,
    cone: int,
) -> str:
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


def list_available_colorants() -> str:
    colorants = {
        "iron": {"description": "Iron oxide", "warmth": 8.0, "character": "earthy"},
        "cobalt": {"description": "Cobalt oxide", "warmth": 1.5, "character": "pure blue"},
        "copper": {"description": "Copper oxide", "warmth": 5.0, "character": "versatile"},
        "chrome": {"description": "Chromium oxide", "warmth": 2.0, "character": "stable green"},
        "manganese": {"description": "Manganese dioxide", "warmth": 1.0, "character": "soft purple"},
        "vanadium": {"description": "Vanadium pentoxide", "warmth": 7.0, "character": "warm yellow"}
    }
    return json.dumps(colorants, indent=2)


def list_available_fluxes() -> str:
    fluxes = {
        "boron": {"reflectivity": 9.5, "effect": "glossy, luminous"},
        "alkaline": {"reflectivity": 6.0, "effect": "fluid, dynamic"},
        "alkaline_earth": {"reflectivity": 2.5, "effect": "matte, grounded"},
        "lead": {"reflectivity": 8.0, "effect": "glassy, smooth"}
    }
    return json.dumps(fluxes, indent=2)


def compare_glaze_formulations(glaze1_description: str, glaze2_description: str) -> str:
    return json.dumps({
        "glaze1": glaze1_description,
        "glaze2": glaze2_description,
        "note": "Use analyze_glaze_formulation() for precise parameters"
    })

