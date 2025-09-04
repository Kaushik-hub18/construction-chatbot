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

# --- Core knowledge base ---
knowledge_base = {
    # --- Greetings & small talk ---
    "hi": "Hello! 👋 How can I help you with construction today?",
    "hello": "Hi there! Ask me anything about construction materials or processes.",
    "hey": "Hey! 👷 I'm your construction assistant.",
    "good morning": "Good morning ☀️! Ready to talk construction?",
    "good afternoon": "Good afternoon 🌤️! How can I assist you?",
    "good evening": "Good evening 🌙! Ask me any construction-related query.",
    "ok": "👍 Okay! Do you want to know something about construction?",
    "thanks": "You're welcome! 😊 Happy to help with construction queries.",
    "bye": "Goodbye 👋! Keep building strong!",

    # --- Creator related ---
    "who made you": "I was created by Kaushik Nath Yarramsetty 🏗️.",
    "who created you": "I was created by Kaushik Nath Yarramsetty 🏗️.",
    "your creator": "My creator is Kaushik Nath Yarramsetty 🏗️.",
    "developer": "I was developed by Kaushik Nath Yarramsetty 🏗️.",
    "owner": "My owner is Kaushik Nath Yarramsetty 🏗️.",

    # --- Basic terms ---
    "construction": "Construction is the process of building infrastructure such as houses, roads, bridges, and other facilities.",
    "building": "A building is a structure with walls and a roof, created for people to live, work, or use for various purposes.",
    "civil engineering": "Civil engineering is a professional discipline that deals with the design, construction, and maintenance of physical and natural structures.",
    "architecture": "Architecture is the art and science of designing buildings and structures.",
    "structure": "A structure is any system of connected parts designed to resist loads, such as buildings, bridges, or towers.",
    "contractor": "A contractor is a person or company responsible for carrying out construction work as per contract.",
    "engineer": "An engineer is a professional who applies scientific and mathematical principles to design and build structures.",
    "labor": "Labor refers to the workforce that performs physical tasks in construction.",
    "site": "A construction site is the designated location where building activities are carried out.",
    "drawing": "Construction drawings are detailed plans prepared by architects and engineers that guide construction activities.",
    "blueprint": "A blueprint is a technical drawing that shows the design, dimensions, and specifications of a building.",
    "material": "Construction materials are the physical elements (cement, steel, sand, bricks, etc.) used to build structures.",
    "load": "Load refers to the weight or force that a structure must carry, such as dead load, live load, or wind load.",
    "foundation": "The foundation is the lowest part of a structure that transfers loads from the building to the ground.",

    # --- Materials ---
    "cement": "Cement is a binding material used in construction. It sets, hardens, and binds other materials together.",
    "concrete": "Concrete is a mixture of cement, sand, aggregates, and water. It is used as a strong building material.",
    "curing": "Curing is the process of maintaining moisture in concrete after it is placed to ensure proper strength gain.",
    "brick": "A brick is a rectangular block made of clay, used for building walls and structures.",
    "aac block": "AAC (Autoclaved Aerated Concrete) blocks are lightweight, precast foam concrete blocks used for construction.",
    "steel": "Steel provides tensile strength to concrete structures, commonly used as reinforcement in construction.",
    "rebar": "Rebar, or reinforcing bar, is steel reinforcement used in concrete to improve tensile strength and prevent cracking.",
    "aggregate": "Aggregates are granular materials like sand, gravel, or crushed stone, added to concrete or mortar to provide bulk, strength, and stability.",
    "bitumen": "Bitumen is a black, sticky material used for road construction and waterproofing.",
    "fly ash": "Fly ash is a byproduct of coal combustion, used in cement and concrete for improved durability and sustainability.",
    "gypsum": "Gypsum is a soft sulfate mineral, used in plaster, drywall, and as a retarder in cement.",
    "timber": "Timber is processed wood, widely used in formwork, furniture, flooring, and roofing.",
    "glass": "Glass is used in modern construction for windows, facades, and decorative purposes.",
    "aluminium": "Aluminium is lightweight, corrosion-resistant metal used in facades, windows, and structural applications.",
    "polymer": "Polymers are plastic-based materials used in pipes, insulation, flooring, and coatings.",

    # --- Structural Elements ---
    "slab": "A slab is a flat, horizontal concrete element used in floors and roofs.",
    "beam": "A beam is a horizontal structural element that resists loads applied laterally to its axis.",
    "column": "A column is a vertical structural element that transfers loads from beams and slabs to the foundation.",
    "lintel": "A lintel is a horizontal support placed above doors and windows to bear loads from above.",
    "retaining wall": "A retaining wall holds back soil or rock from a building, road, or area.",
    "shear wall": "A shear wall is a vertical wall that resists lateral forces like wind and earthquakes.",
    "pile foundation": "Pile foundation is a deep foundation system used to transfer load to hard soil layers or rock.",

    # --- Techniques & Work ---
    "formwork": "Formwork is a temporary mold into which concrete is poured to form structural shapes until it gains strength.",
    "shuttering": "Shuttering is another term for formwork, providing a mold for concrete structures.",
    "plastering": "Plastering is applying plaster to walls and ceilings to create a smooth finish.",
    "masonry": "Masonry is building structures with bricks, stones, or blocks, usually bound with mortar.",
    "precast concrete": "Precast concrete is concrete cast in a controlled environment, then transported to the site.",
    "scaffolding": "Scaffolding is a temporary structure used to support workers and materials.",
    "grouting": "Grouting fills gaps or strengthens structures with cementitious or chemical materials.",
    "tiling": "Tiling is the process of laying tiles for flooring or wall finishes.",
    "painting": "Painting is applying protective or decorative coating to surfaces.",
    "plumbing": "Plumbing involves installing pipes, fittings, and fixtures for water supply and drainage.",
    "electrical work": "Electrical work includes wiring, lighting, and installation of power systems in buildings.",
    "hvac": "HVAC (Heating, Ventilation, and Air Conditioning) controls indoor environment and comfort.",
    "waterproofing": "Waterproofing makes structures resistant to water penetration.",

    # --- Roads & Infrastructure ---
    "pavement": "Pavement is the durable surface of roads, often made with asphalt or concrete.",
    "asphalt": "Asphalt is a sticky, black mixture used in road construction and roofing.",
    "bridge": "A bridge is a structure that spans obstacles like rivers or roads.",
    "highway": "A highway is a main road designed for fast and heavy traffic.",
    "tunnel": "A tunnel is an underground passage constructed for roads, trains, or utilities.",

    # --- Surveying & Testing ---
    "surveying": "Surveying measures and maps land to determine boundaries and layouts.",
    "soil testing": "Soil testing determines soil properties and bearing capacity.",
    "nondestructive testing": "NDT methods test materials and structures without causing damage.",
    "slump test": "Slump test checks the workability of fresh concrete.",
    "cube test": "Cube test measures the compressive strength of concrete.",

    # --- Management & Contracts ---
    "boq": "A Bill of Quantities (BOQ) lists all materials, labor, and costs for a project.",
    "estimation": "Estimation predicts cost, materials, and time for construction.",
    "project management": "Construction project management oversees planning, execution, and delivery.",
    "gantt chart": "A Gantt chart is a project scheduling tool showing activities and timelines.",
    "site mobilization": "Site mobilization prepares resources and workers at a construction site.",
    "tender": "Tendering is the process of inviting bids for a construction project.",
    "contract": "A construction contract is a legal agreement between client and contractor.",

    # --- Safety & Sustainability ---
    "safety": "Construction safety includes PPE, scaffolding safety, and site protocols.",
    "ppe": "Personal Protective Equipment (PPE) includes helmets, gloves, boots, and safety vests.",
    "osha": "OSHA standards define safety regulations for workplaces.",
    "green building": "Green building uses eco-friendly materials and energy-efficient designs.",
    "leed": "LEED is a green building certification for sustainable construction.",
    "bim": "Building Information Modeling (BIM) is a digital representation of building data.",
    "rainwater harvesting": "Rainwater harvesting collects and stores rainwater for reuse.",
    "solar energy": "Solar energy is harnessed using panels for electricity in buildings."
}

# --- Synonyms and variations ---
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

# --- Chat endpoint ---
@app.post("/chat")
async def chat(request: ChatRequest):
    user_query = request.query.lower()

    # 1. Check exact greetings & small talk (to avoid "did you mean" for hi/hello etc.)
    for g in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "ok", "thanks", "bye"]:
        if g in user_query:
            return {"answer": knowledge_base[g]}

    # --- Custom creator Q&A ---
    if any(phrase in user_query for phrase in ["who made you", "who created you", "your creator", "developed you", "who is your owner"]):
        return {"answer": "I was created by Kaushik Nath Yarramsetty 🏗️."}    
    

    # 2. Check exact or synonym matches
    for keyword, variations in synonyms.items():
        for variation in variations:
            if variation in user_query:
                return {"answer": knowledge_base[keyword]}

    # 3. If no direct match, suggest the closest known topic
    all_keywords = list(knowledge_base.keys())
    suggestion = difflib.get_close_matches(user_query, all_keywords, n=1, cutoff=0.5)
    
    if suggestion:
        return {
            "answer": f"I'm not sure, but did you mean **{suggestion[0]}**? Here's what I know:\n\n{knowledge_base[suggestion[0]]}"
        }

    # 4. Default fallback response
    return {
        "answer": "I'm sorry, I don't have information on that topic yet. Please ask about construction materials, structural elements, or processes."
    }
