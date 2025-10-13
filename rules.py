# rules.py

# Mapping of keywords to waste categories
keyword_map = {
    # Recyclable
    "bottle": "recyclable",
    "plastic": "recyclable",
    "glass": "recyclable",
    "cd": "recyclable",
    "paper": "recyclable",
    "can": "recyclable",
    "cardboard": "recyclable",
    "jar": "recyclable",
    "newspaper": "recyclable",
    "magazine": "recyclable",
    "tin": "recyclable",
    "aluminum": "recyclable",
    "metal": "recyclable",
    "book": "recyclable",
    "envelope": "recyclable",
    "carton": "recyclable",
    "plastic bottle": "recyclable",
    "glass bottle": "recyclable",
    "milk carton": "recyclable",
    "juice carton": "recyclable",
    "aerosol can": "recyclable",
    "paperboard": "recyclable",
    "junk mail": "recyclable",
    "office paper": "recyclable",
    "printer paper": "recyclable",
    "folder": "recyclable",
    "cereal box": "recyclable",
    "shoebox": "recyclable",
    "metal lid": "recyclable",
    "aluminum foil": "recyclable",
    "steel can": "recyclable",
    "soda can": "recyclable",
    "beer can": "recyclable",
    "wine bottle": "recyclable",
    "beer bottle": "recyclable",
    "glass jar": "recyclable",
    "carton box": "recyclable",
    "magazine page": "recyclable",
    "catalog": "recyclable",
    "envelope paper": "recyclable",
    "notebook": "recyclable",
    "card": "recyclable",
    "milk bottle": "recyclable",
    "detergent bottle": "recyclable",
    "plastic container": "recyclable",
    "juice bottle": "recyclable",
    "soap box": "recyclable",

    # Compostable
    "food": "compostable",
    "banana": "compostable",
    "apple": "compostable",
    "orange": "compostable",
    "vegetable": "compostable",
    "fruit": "compostable",
    "leaves": "compostable",
    "grass": "compostable",
    "plant": "compostable",
    "coffee": "compostable",
    "tea": "compostable",
    "egg shell": "compostable",
    "peel": "compostable",
    "bread": "compostable",
    "rice": "compostable",
    "pasta": "compostable",
    "nutshell": "compostable",
    "flower": "compostable",
    "yard waste": "compostable",
    "leftovers": "compostable",
    "potato": "compostable",
    "tomato": "compostable",
    "onion": "compostable",
    "garlic": "compostable",
    "carrot": "compostable",
    "lettuce": "compostable",
    "spinach": "compostable",
    "cabbage": "compostable",
    "melon": "compostable",
    "peach": "compostable",
    "pear": "compostable",
    "plum": "compostable",
    "grape": "compostable",
    "strawberry": "compostable",
    "blueberry": "compostable",
    "avocado": "compostable",
    "corn": "compostable",
    "pumpkin": "compostable",
    "zucchini": "compostable",
    "eggplant": "compostable",
    "lemon": "compostable",
    "apple core": "compostable",
    "orange peel": "compostable",
    "vegetable scraps": "compostable",
    "coffee grounds": "compostable",
    "tea leaves": "compostable",
    "grass clippings": "compostable",
    "dead flowers": "compostable",
    "leftover rice": "compostable",
    "leftover pasta": "compostable",

    # Trash
    "chip": "trash",
    "wrapper": "trash",
    "styrofoam": "trash",
    "diaper": "trash",
    "cigarette": "trash",
    "plastic bag": "trash",
    "toothbrush": "trash",
    "foam": "trash",
    "napkin": "trash",
    "tissue": "trash",
    "mirror": "trash",
    "ceramic": "trash",
    "broken glass": "trash",
    "clothing": "trash",
    "rubber": "trash",
    "styrofoam cup": "trash",
    "plastic straw": "trash",
    "plastic spoon": "trash",
    "plastic fork": "trash",
    "plastic knife": "trash",
    "takeout container": "trash",
    "chip bag": "trash",
    "candy wrapper": "trash",
    "toothpaste tube": "trash",
    "shampoo bottle": "trash",
    "conditioner bottle": "trash",
    "perfume bottle": "trash",
    "makeup container": "trash",
    "shoe": "trash",
    "sock": "trash",
    "broken toy": "trash",
    "styrofoam plate": "trash",
    "plastic wrap": "trash",
    "bubble wrap": "trash",
    "polystyrene": "trash",
    "paint tube": "trash",
    "used mask": "trash",
    "sanitary pad": "trash",
    "razor": "trash",
    "plastic lid": "trash",
    "chip packet": "trash",
    "wax paper": "trash",
    "cling film": "trash",
    "broken umbrella": "trash",
    "plastic cup": "trash",
    "cosmetic wipes": "trash",
    "hairbrush": "trash",

    # Hazardous
    "battery": "hazardous",
    "electronics": "hazardous",
    "light bulb": "hazardous",
    "thermometer": "hazardous",
    "fluorescent tube": "hazardous",
    "paint": "hazardous",
    "solvent": "hazardous",
    "pesticide": "hazardous",
    "chemical": "hazardous",
    "aerosol spray": "hazardous",
    "ink cartridge": "hazardous",
    "motor oil": "hazardous",
    "cleaning chemicals": "hazardous",
    "batteries": "hazardous",
    "old phone": "hazardous",
    "old tablet": "hazardous",
    "expired medicine": "hazardous",
    "lithium battery": "hazardous",
    "electronic device": "hazardous",
    "mercury thermometer": "hazardous",
    "old circuit board": "hazardous",
}

# List of environmental facts
FACTS = [
    {
        "short": "Recycling one aluminum can saves enough energy to run a TV for 3 hours.",
        "detail": "Producing aluminum from raw materials is extremely energy-intensive. Recycling it reduces energy use by 95% and helps lower carbon emissions."
    },
    {
        "short": "Composting food waste reduces methane emissions from landfills.",
        "detail": "When food decomposes anaerobically in landfills, it releases methane — a greenhouse gas 25x more potent than CO₂. Composting turns that waste into nutrient-rich soil instead."
    },
    {
        "short": "Glass can be recycled endlessly without losing purity or quality.",
        "detail": "Unlike plastic or paper, glass doesn’t degrade with each recycling cycle, making it one of the most sustainable materials for packaging."
    },
    {
        "short": "Plastic takes over 400 years to decompose in landfills.",
        "detail": "Even when broken down into microplastics, it continues to harm ecosystems, enter food chains, and persist in the environment for centuries."
    },
    {
        "short": "E-waste contains precious metals like gold and silver.",
        "detail": "Recycling electronics helps recover valuable materials — a ton of old phones yields more gold than a ton of mined ore."
    },
    {
        "short": "Trees absorb CO₂ and improve air quality.",
        "detail": "Planting trees reduces greenhouse gases, provides oxygen, and helps regulate temperature, making them essential for combating climate change."
    },
    {
        "short": "Turning off lights saves electricity and money.",
        "detail": "Even a small action like switching off unused lights reduces electricity demand, lowers carbon emissions, and saves on energy bills."
    },
    {
        "short": "Using a reusable water bottle can prevent hundreds of plastic bottles from polluting oceans.",
        "detail": "Plastic bottles take centuries to break down. Switching to reusable bottles significantly reduces plastic waste and environmental pollution."
    },
    {
        "short": "Food waste contributes to global greenhouse gas emissions.",
        "detail": "Approximately 1.3 billion tons of food are wasted each year, generating massive methane emissions from landfills and wasting the energy used to produce it."
    },
    {
        "short": "Solar panels reduce reliance on fossil fuels.",
        "detail": "By converting sunlight into electricity, solar panels cut greenhouse gas emissions, lower energy costs, and promote sustainable energy sources."
    },
    {
        "short": "Carpooling reduces traffic congestion and emissions.",
        "detail": "Sharing rides lowers the number of vehicles on the road, reducing fuel consumption, air pollution, and traffic-related stress."
    },
    {
        "short": "Clothing made from natural fibers is more sustainable than synthetic textiles.",
        "detail": "Natural fibers like cotton, wool, and hemp biodegrade more easily than polyester or nylon, which release microplastics into waterways."
    },
    {
        "short": "Recycling paper saves trees and water.",
        "detail": "Producing recycled paper reduces deforestation, conserves water, and lowers the energy needed compared to making paper from virgin pulp."
    },
    {
        "short": "Ocean cleanup reduces plastic pollution and protects marine life.",
        "detail": "Removing plastics and debris from oceans prevents harm to marine animals, reduces toxins in the food chain, and preserves aquatic ecosystems."
    },
    {
        "short": "Using energy-efficient appliances lowers carbon footprints.",
        "detail": "Appliances with higher energy ratings consume less electricity, reduce greenhouse gas emissions, and save money over time."
    },
    {
        "short": "Meat production has a high environmental impact.",
        "detail": "Livestock farming produces significant methane emissions, uses large amounts of water, and contributes to deforestation; plant-based diets can reduce these effects."
    },
    {
        "short": "Reusing and repurposing items reduces waste.",
        "detail": "Giving items a second life decreases landfill contributions, saves resources, and encourages a circular economy."
    },
    {
        "short": "Rainwater harvesting conserves water and reduces flooding.",
        "detail": "Collecting and storing rainwater helps manage water supply sustainably, lowers dependence on municipal water, and prevents stormwater runoff issues."
    },
    {
        "short": "LED bulbs consume less energy than incandescent bulbs.",
        "detail": "LEDs use up to 80% less energy, last longer, and emit less heat, reducing both energy bills and environmental impact."
    },
    {
        "short": "Electric vehicles produce lower emissions than gasoline cars.",
        "detail": "EVs reduce greenhouse gas emissions and air pollutants, especially when charged using renewable energy sources."
    }
]
