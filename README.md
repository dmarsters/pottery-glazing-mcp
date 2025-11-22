# Pottery Glazing Chemistry MCP Server

**Transform ceramic glaze chemistry into visual image generation parameters.**

Pottery glazing is a domain where chemistry directly produces sensory outcomes. This MCP server encodes that relationship mathematically, allowing potters and researchers to generate images that capture the visual intention of their glaze formulations.

## Core Insight

Expert pottery knowledge isn't just chemistry—it's a sophisticated compression of "how specific oxide + flux + atmosphere combinations produce distinctive visual character." Rather than building a generic color mixer, this server captures the categorical structure of glaze chemistry and maps it to image generation dimensions.

## What It Does

The server implements a three-layer olog framework:

1. **Categorical Structure** (YAML olog): Types and morphisms that formalize glaze chemistry
2. **Intentionality** (Reasoning document): Why these chemistry mappings produce visual effects
3. **Execution** (MCP tools): Tools that combine chemistry specifications into visual parameters

## Visual Parameters

The server outputs seven visual dimensions that image generators understand:

- **Optical Intensity** (0-10): How dark vs bright the glaze appears
  - Reduction atmosphere → dark (8-9)
  - Oxidation atmosphere → bright (3-5)

- **Saturation** (0-10): Color intensity and purity
  - Scaled by: colorant type, colorant amount, atmosphere, temperature maturation

- **Reflectivity** (0-10): Surface gloss vs matte
  - Boron flux → glossy (9-10)
  - Alkaline earth flux → matte (2-3)

- **Hue Temperature** (0=cool, 5=neutral, 10=warm)
  - Cobalt, chrome → cool (1-3)
  - Iron, vanadium → warm (7-9)

- **Maturation Level** (0-10): How "finished" the glaze feels
  - Cone 2 (low fire) → immature (3-4)
  - Cone 10 (high fire) → mature (9-10)

- **Crystalline Definition** (0-10): Surface texture and crystal clarity
  - Increases with firing temperature
  - Glossy fluxes suppress crystallinity
  - Matte fluxes enable it

- **Surface Flow** (0-10): Running/pooling behavior
  - Fluid fluxes + running glaze → high (7-9)
  - Stiff fluxes + static glaze → low (1-3)

## Colorants Supported

| Colorant | Hue | Warmth | Purity | Notes |
|----------|-----|--------|--------|-------|
| **Iron** | Brown/Red/Black | Very Warm (8/10) | Earthy (6/10) | Most versatile, historically important |
| **Cobalt** | Blue/Purple | Very Cool (1.5/10) | Pure (9/10) | Intense, potent in small amounts |
| **Copper** | Green/Red | Neutral (5/10) | Responsive (8/10) | Dramatically shifts reduction ↔ oxidation |
| **Chrome** | Green | Cool (2/10) | Stable (7/10) | Mineral-like, atmosphere-stable |
| **Manganese** | Purple/Brown | Very Cool (1/10) | Muted (5/10) | Soft, organic, good for blending |
| **Vanadium** | Yellow/Green | Warm (7/10) | Subtle (6.5/10) | Rare, produces unique warm tones |

## Flux Systems Supported

| Flux | Reflectivity | Character | Running | Notes |
|------|--------------|-----------|---------|-------|
| **Boron** | 9.5/10 | Glossy, mirror-like | Moderate | Creates brightest, glossiest surfaces |
| **Alkaline** | 6/10 | Satin, flowing | High | Creates intentional runs and pooling |
| **Alkaline Earth** | 2.5/10 | Matte, grounded | Low | Most natural, earthy finishes |
| **Lead** | 8/10 | Glassy, smooth | Moderate | Historic; modern use requires testing |

## Tools

### `analyze_glaze_formulation`

Analyze a specific glaze chemistry and extract visual parameters.

```python
result = analyze_glaze_formulation(
    colorant="cobalt",           # iron, cobalt, copper, chrome, manganese, vanadium
    colorant_percentage=2.0,     # amount in formulation (typically 0.5-15%)
    flux_type="boron",           # boron, alkaline, alkaline_earth, lead
    atmosphere="reduction",      # oxidation, reduction, neutral
    cone=10,                      # firing cone (06 to 13)
    runs=False                    # whether glaze is formulated to run
)
```

**Returns:** Dictionary with `visual_parameters`, `descriptive_qualities`, and `sensory_intention`.

### `enhance_image_prompt_from_glaze`

Take a base image prompt and infuse it with glaze aesthetic qualities.

```python
enhanced = enhance_image_prompt_from_glaze(
    base_prompt="a ceramic vase on a shelf",
    colorant="copper",
    flux_type="alkaline",
    atmosphere="reduction",
    cone=10
)
```

**Returns:** Enhanced prompt with glaze characteristics woven in naturally.

### `list_available_colorants`

Get comprehensive information about all supported colorants.

### `list_available_fluxes`

Get comprehensive information about all supported flux systems.

### `compare_glaze_formulations` (Qualitative)

Conceptually compare two glaze descriptions for visual differences.

## Usage Examples

### Example 1: Deep Blue Reduction Glaze

```python
result = analyze_glaze_formulation(
    colorant="cobalt",
    colorant_percentage=2.0,
    flux_type="boron",
    atmosphere="reduction",
    cone=10
)

# Returns:
# optical_intensity: 8.5 (dark, concentrated)
# saturation: 8.5 (deep blue)
# reflectivity: 9.5 (glossy, mirror-like)
# hue_temperature: 1.5 (cool)
# maturation_level: 9.5 (fully mature)
# sensory: "mysterious, concentrated, sultry; luminous and flowing"
```

### Example 2: Earthy Matte Iron Glaze

```python
result = analyze_glaze_formulation(
    colorant="iron",
    colorant_percentage=8.0,
    flux_type="alkaline_earth",
    atmosphere="oxidation",
    cone=6
)

# Returns:
# optical_intensity: 4.0 (bright, transparent)
# saturation: 4.5 (muted earthy brown)
# reflectivity: 2.5 (matte)
# hue_temperature: 8.0 (very warm)
# maturation_level: 7.0 (well-matured)
# sensory: "clear, bright, direct; stable and grounded"
```

### Example 3: Running Copper Reduction

```python
result = analyze_glaze_formulation(
    colorant="copper",
    colorant_percentage=8.0,
    flux_type="alkaline",
    atmosphere="reduction",
    cone=10,
    runs=True
)

# Returns:
# optical_intensity: 8.5 (dark, concentrated)
# saturation: 7.5 (deep red with mystery)
# reflectivity: 6.0 (satin fluid)
# surface_flow: 4.8 (runs due to fluid alkaline + runs=True)
# sensory: "mysterious, concentrated, sultry; fluid and dynamic"
```

## Mathematical Foundation

The server implements these categorical morphisms:

```
Atmosphere → Color Modulation
  reduction + any colorant → darker, more saturated, shifted hue

Flux → Surface Texture
  boron → gloss (9.5)
  alkaline → satin (6.0)
  alkaline_earth → matte (2.5)

Temperature → Maturation
  cone ≤ 2 → immature (3-4)
  cone 5-6 → balanced (7)
  cone ≥ 10 → mature (9-10)

Colorant → Visual Effect
  cobalt → cool (1.5), pure (9), intense (8.5)
  iron → warm (8), earthy (6), variable (6.5)
  copper → responsive (5), versatile (8), variable (8)
  ...
```

These compose into a unified transformation:

```
ColorDevelopment × FluxBehavior × Atmosphere × Temperature → VisualParameters
```

Where visual parameters are: optical_intensity, saturation, reflectivity, hue_temperature, maturation_level, crystalline_definition, surface_flow.

## Integration with Image Generators

The server outputs parameters directly usable with Flux, Midjourney, Stable Diffusion, etc.

### Method 1: Direct Enhancement

Use `enhance_image_prompt_from_glaze()` to get a complete enhanced prompt:

```
Original: "a ceramic vase on a shelf"

Enhanced: "a ceramic vase on a shelf [glaze aesthetic: dark, concentrated optical quality; glossy mirror-like surface with strong light reflection; intensely saturated, vivid coloration; cool-toned, pure character; fully matured, intentional finish; feels mysterious, concentrated, sultry; luminous and flowing]"
```

### Method 2: Manual Parameter Blending

Extract visual parameters and blend them into your own prompts:

```python
result = analyze_glaze_formulation(...)
params = result["visual_parameters"]

# Then craft prompt incorporating:
# - Saturation level
# - Gloss/matte character
# - Color warmth
# - Maturation feeling
# - Surface flow description
```

## Domain Knowledge

This server encodes pottery expertise precisely because pottery glazes contain **inherent visual information**. A potter's formulation choices directly specify sensory outcomes:

- **"I'm using boron flux"** = "I want glossy surfaces with light bounce"
- **"I'm firing in reduction"** = "I want dark, mysterious, concentrated color"
- **"I'm adding 10% cobalt"** = "I want intense, jewel-like blue"

The MCP server makes this implicit expertise explicit and reproducible.

## Testing

Run the test suite:

```bash
cd pottery_glazing_mcp
pip install -e . --break-system-packages
pip install pytest --break-system-packages
python -m pytest tests/test_glaze_processor.py -v
```

All 20 tests verify:
- Individual morphism correctness
- Composite glaze analysis consistency
- Parameter ranges (all 0-10 or appropriately bounded)
- JSON serializability
- Sensory intention mapping accuracy

## Architecture

```
pottery_glazing_mcp/
├── glazing_olog.yaml                # Categorical structure (types, morphisms)
├── glaze_processor.py               # Morphism implementations
├── server.py                        # MCP tool definitions
└── tests/
    └── test_glaze_processor.py      # 20 tests covering all dimensions
```

## Next Steps

- Deploy to FastMCP.cloud for remote access
- Integrate with Claude Desktop for multi-server composition
- Extend with additional colorants (rutile, ilmenite, etc.)
- Add crystalline glaze chemistry (matte ash glazes, etc.)
- Publish academic paper on categorical encoding of sensory domains

## References

- **Olog Framework**: [Functional Data Structures with Dependent Types](https://arxiv.org/abs/1201.6689)
- **Category Theory Applied**: Natural Transformations, Adjoint Functors
- **Pottery Science**: Savage & Poston "Ceramic Glazes" (foundational reference)
- **Lushy Project**: Encoding domain expertise as visual parameters

---

**Created as part of the Lushy project: "Epistemological infrastructure for translating domain expertise into visual representations through rigorous mathematical frameworks."**
