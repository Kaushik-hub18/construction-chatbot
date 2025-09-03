from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import difflib  # for close match suggestions

# Define request format
class ChatRequest(BaseModel):
    query: str

# Create FastAPI app
app = FastAPI()

# Allow frontend (React) to connect to backend (FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    return {"message": "Construction Chatbot Backend Running ✅"}

# Core knowledge base
knowledge_base = {
    "cement": "Cement is a binding material used in construction. It sets, hardens, and binds other materials together.",
    "concrete": "Concrete is a mixture of cement, sand, aggregates, and water. It is used as a strong building material.",
    "curing": "Curing is the process of maintaining moisture in concrete after it is placed to ensure proper strength gain.",
    "brick": "A brick is a rectangular block made of clay, used for building walls and structures.",
    "steel": "Steel provides tensile strength to concrete structures, commonly used as reinforcement in construction.",
    "aggregate": "Aggregates are granular materials like sand, gravel, or crushed stone, added to concrete or mortar to provide bulk, strength, and stability.",
    "formwork": "Formwork is a temporary mold into which concrete is poured to form structural shapes until it gains sufficient strength.",
    "foundation": "The foundation is the lowest part of a structure that transfers loads from the building to the ground. Types include shallow and deep foundations.",
    "plastering": "Plastering is the process of applying a layer of plaster over walls or ceilings to create a smooth surface for painting or finishing.",
    "masonry": "Masonry refers to the construction of structures from individual units like bricks, stones, or blocks, often bound together by mortar.",
    "rebar": "Rebar, or reinforcing bar, is steel reinforcement used in concrete to improve tensile strength and prevent cracking.",
    "precast concrete": "Precast concrete refers to concrete elements cast in a controlled environment and then transported to the construction site for installation.",
    "scaffolding": "Scaffolding is a temporary structure used to support workers and materials during the construction, maintenance, or repair of buildings.",
    "surveying": "Surveying is the technique of measuring and mapping land to determine boundaries, topography, and layout for construction planning.",
    "waterproofing": "Waterproofing is the process of making structures resistant to water penetration to prevent damage and leaks.",
    "asphalt": "Asphalt is a sticky, black mixture used primarily in road construction and roofing for its durability and water-resistant properties.",
    "beam": "A beam is a horizontal structural element that resists loads applied laterally, helping to support weight in buildings and bridges.",
    "column": "A column is a vertical structural element that primarily carries compressive loads and transfers them to the foundation.",
    "slab": "A slab is a flat, horizontal surface, often made of reinforced concrete, used for floors, roofs, or ceilings.",
    "grout": "Grout is a fluid material used to fill gaps or seal joints between tiles, masonry, or structural elements.",
    "pile": "Piles are deep foundation elements driven into soil to transfer loads from structures to deeper, stable soil layers or bedrock.",
    "retaining wall": "A retaining wall is a structure built to hold back soil, preventing erosion and maintaining level differences in ground elevation."
}

# Synonyms and variations
synonyms = {
    "cement": ["cement", "portland cement", "binding material", "cment"],
    "concrete": ["concrete", "ready mix", "mix design", "concret"],
    "curing": ["curing", "moist curing", "hydration process"],
    "brick": ["brick", "bricks", "block", "clay block"],
    "steel": ["steel", "reinforcement", "iron rods", "rebar steel"],
    "aggregate": ["aggregate", "aggregates", "gravel", "stones"],
    "formwork": ["formwork", "shuttering", "casting mold"],
    "foundation": ["foundation", "footing", "pile foundation", "raft foundation"],
    "plastering": ["plastering", "wall plaster", "finish coating"],
    "masonry": ["masonry", "brick work", "stone work"],
    "rebar": ["rebar", "reinforcement bar", "rod", "steel bar"],
    "precast concrete": ["precast", "precast concrete", "pre-cast"],
    "scaffolding": ["scaffolding", "scaffold", "support structure"],
    "surveying": ["surveying", "land survey", "leveling", "theodolite survey"],
    "waterproofing": ["waterproofing", "damp proofing", "leak proofing"],
    "asphalt": ["asphalt", "bitumen", "blacktop"],
    "beam": ["beam", "lintel beam", "support beam"],
    "column": ["column", "pillar", "vertical support"],
    "slab": ["slab", "floor slab", "roof slab"],
    "grout": ["grout", "grouting", "joint filler"],
    "pile": ["pile", "pile foundation", "deep foundation"],
    "retaining wall": ["retaining wall", "support wall", "soil retaining"]
}

# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    user_query = request.query.lower()

    # Check exact or synonym matches
    for keyword, variations in synonyms.items():
        for variation in variations:
            if variation in user_query:
                return {"answer": knowledge_base[keyword]}

    # If no direct match, suggest the closest known topic
    all_keywords = list(knowledge_base.keys())
    suggestion = difflib.get_close_matches(user_query, all_keywords, n=1, cutoff=0.5)
    
    if suggestion:
        return {
            "answer": f"I'm not sure, but did you mean **{suggestion[0]}**? Here's what I know:\n\n{knowledge_base[suggestion[0]]}"
        }

    # Default fallback response
    return {
        "answer": "I'm sorry, I don't have information on that topic yet. Please ask about construction materials, structural elements, or processes."
    }
