# Style-conditioned prompts and prompt templates for the Image Generator

# Dictionary of available styles and their prompt enhancements
STYLES = {
    "None (Raw Prompt)": {
        "suffix": "",
        "negative": "",
        "description": "Uses your prompt exactly as entered."
    },
    "Cyberpunk": {
        "suffix": ", cyberpunk style, neon lighting, highly detailed, futuristic city streets, glowing signs, rain-slicked pavement, synthwave color palette, 8k resolution",
        "negative": "organic, rural, historical, bright sunlight, natural landscape",
        "description": "Futuristic neon-drenched cities and high-tech, low-life aesthetics."
    },
    "Anime": {
        "suffix": ", anime style, detailed, vibrant colors, expressive characters, beautiful line art, studio ghibli or makoto shinkai aesthetic, high-definition",
        "negative": "photorealistic, 3d render, deformed, blurry, low quality",
        "description": "Vibrant, hand-drawn Japanese animation style."
    },
    "Photorealistic": {
        "suffix": ", photorealistic, hyper-detailed 8k, DSLR camera, professional lighting, shot on 35mm lens, sharp focus, natural shadows, volumetric light, award-winning photography",
        "negative": "drawing, painting, illustration, cartoon, anime, 3d render, CGI, sketch",
        "description": "Looks like a real photo taken with a high-end camera."
    },
    "3D Render / Pixar": {
        "suffix": ", 3D style, cute, Pixar aesthetic, claymation style, vibrant color grading, ray-traced shadows, soft lighting, detailed textures, octane render",
        "negative": "photorealistic, sketch, drawing, low-poly, deformed, flat lighting",
        "description": "Smooth 3D animated character and environment style."
    },
    "Fantasy / Oil Painting": {
        "suffix": ", mythical fantasy oil painting, dramatic lighting, detailed brush strokes, epic scale, magical atmosphere, rich canvas texture, masterwork, romanticism",
        "negative": "modern, futuristic, neon, photo, digital, clean vector, minimalist",
        "description": "Classic, rich textured oil paintings of magical worlds."
    },
    "Pixel Art": {
        "suffix": ", detailed pixel art, 8-bit retro gaming aesthetic, vibrant colors, clean grid, nostalgic console style, pixelated",
        "negative": "photorealistic, smooth gradient, blur, 3d render, vector art",
        "description": "Charming retro 8-bit and 16-bit gaming graphics."
    },
    "Steampunk": {
        "suffix": ", steampunk aesthetic, brass and copper gears, steam pipes, Victorian retro-futurism, sepia and gold tones, intricate clockwork details, industrial revolution",
        "negative": "modern, plastic, cyberpunk, neon, digital screen, sleek space age",
        "description": "Victorian science fiction with brass machinery and steam power."
    },
    "Origami / Papercraft": {
        "suffix": ", origami papercraft art, layered textured paper, soft shadow play, handcrafted feel, pastel color palette, depth of field",
        "negative": "liquid, glass, glossy, realistic skin, photographic, metal",
        "description": "Delicate, folded, layered paper creations."
    },
    "Surrealism": {
        "suffix": ", surrealist art style, dreamlike atmosphere, Salvador Dali and Rene Magritte inspired, melting clocks, bizarre landscapes, mind-bending compositions, highly detailed",
        "negative": "ordinary, normal, realistic, standard, boring, predictable",
        "description": "Dream-like, fantastical, and logic-defying imagery."
    }
}

# Creative starter prompts for random generation
RANDOM_PROMPTS = [
    "A mystical library inside a hollow giant redwood tree, filled with glowing ancient books",
    "A futuristic astronaut playing a saxophone on the surface of Mars, Earth in the background",
    "An ancient temple floating among pink clouds at sunset, waterfalls cascading into the sky",
    "A cozy cabin in the woods made of giant mushrooms, smoke curling from the chimney",
    "A majestic mechanical dragon made of brass and crystals, sleeping on a pile of glowing gold coins",
    "A cute red panda wearing a tiny chef's hat, preparing sushi in a miniature kitchen",
    "A mysterious wizard path winding through a neon forest with floating bioluminescent jellyfish",
    "An underwater city enclosed in giant glass domes, with whales swimming between towers",
    "A majestic white stag with antlers made of cherry blossom branches, walking in a misty forest",
    "A vintage typewriter that prints out miniature glowing stars and galaxies",
    "A sleeping cat curled up on top of a crescent moon, floating in a starry night sky",
    "A bustling medieval market on the back of a colossal walking turtle",
    "A cybernetic falcon flying over a desert city at sunset, neon wings shining",
    "A cozy train compartment riding through a snowy wonderland, tea steaming on the table",
    "A vibrant street festival in Venice, but the canals are filled with glowing liquid stardust"
]

def get_style_names():
    """Returns a list of available style names."""
    return list(STYLES.keys())

def get_style_info(style_name):
    """Returns the suffix, negative prompt, and description for a style."""
    return STYLES.get(style_name, STYLES["None (Raw Prompt)"])

def enhance_prompt(prompt, style_name):
    """
    Applies the style-conditioned suffix to the user's prompt.
    Returns the final prompt sent to the generator.
    """
    style_info = get_style_info(style_name)
    suffix = style_info["suffix"]
    return f"{prompt}{suffix}"

def get_random_prompt():
    """Selects and returns a random prompt from the predefined list."""
    import random
    return random.choice(RANDOM_PROMPTS)
