"""
AI Plant Disease Detection - Disease Information & Recommendations Knowledge Base
=================================================================================
Contains comprehensive local agronomic and disease profile data for all 38 supported classes.
Includes disease descriptions, symptoms, causes, prevention guidance, and basic recommendations.
"""

from typing import Dict, Any, Optional

# Structured knowledge base for all 38 classes
DISEASE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "Apple - Apple Scab": {
        "plant_name": "Apple",
        "disease_name": "Apple Scab",
        "is_healthy": False,
        "short_description": "A serious fungal disease caused by Venturia inaequalis that affects apple leaves, blossoms, and fruit, leading to premature defoliation and blemished fruit.",
        "symptoms": [
            "Olive-green to dark brown or velvety black spots on leaves.",
            "Deformed, puckered, or curling foliage as lesions enlarge.",
            "Rough, scabby, cracked lesions on apple fruit skin.",
            "Early leaf drop reducing tree vigor and winter hardiness."
        ],
        "possible_causes": [
            "Fungus Venturia inaequalis overwintering in fallen leaf debris.",
            "Prolonged periods of leaf wetness and moderate spring temperatures (15-24°C).",
            "Dense tree canopy restricting natural air circulation and sunlight penetration."
        ],
        "prevention": [
            "Rake and destroy fallen leaf litter in autumn to eliminate overwintering spores.",
            "Prune branches annually to promote airflow and speed up leaf drying.",
            "Plant scab-resistant apple cultivars (e.g., Liberty, Enterprise, Freedom).",
            "Avoid overhead irrigation to minimize prolonged foliage wetness."
        ],
        "basic_recommendations": [
            "Prune infected twigs and dispose of fallen debris away from the orchard.",
            "Apply protective organic or copper-based orchard sprays early in the growing season if recommended locally.",
            "Consult with an agricultural extension officer or certified arborist for persistent orchard infections."
        ]
    },

    "Apple - Black Rot": {
        "plant_name": "Apple",
        "disease_name": "Black Rot (Frogeye Leaf Spot)",
        "is_healthy": False,
        "short_description": "A fungal disease caused by Botryosphaeria obtusa that affects leaves, fruit, and bark, causing 'frogeye' leaf spots and sunken branch cankers.",
        "symptoms": [
            "Small purple specks on leaves that enlarge into circular spots with brown centers ('frogeye' pattern).",
            "Firm, brown rot on fruit expanding into concentric dark rings.",
            "Sunken reddish-brown cankers on bark and larger limbs.",
            "Mummified fruit remaining attached to twigs through winter."
        ],
        "possible_causes": [
            "Fungus Botryosphaeria obtusa infecting stressed or mechanically damaged trees.",
            "Spore dispersal via wind and splashing rain during humid warm weather.",
            "Accumulation of dead wood, unpruned cankers, and mummified fruit in trees."
        ],
        "prevention": [
            "Prune out dead wood, fire-blighted twigs, and cankered limbs during dormancy.",
            "Remove all mummified apples from the tree and ground.",
            "Maintain optimal tree nutrition and avoid wounding bark during cultivation.",
            "Sanitize pruning equipment between cuts using 70% alcohol or diluted bleach solution."
        ],
        "basic_recommendations": [
            "Cut cankered branches 15–20 cm below visible lesion borders.",
            "Maintain balanced fertilization to improve overall tree resistance.",
            "Seek guidance from a local horticultural expert for severe branch cankers."
        ]
    },

    "Apple - Cedar Apple Rust": {
        "plant_name": "Apple",
        "disease_name": "Cedar Apple Rust",
        "is_healthy": False,
        "short_description": "A heteroecious fungal disease caused by Gymnosporangium juniperi-virginianae requiring both apple trees and Eastern red cedar/juniper hosts to complete its life cycle.",
        "symptoms": [
            "Bright yellow-orange or reddish spots on the upper leaf surface.",
            "Small black specks (fruiting bodies) forming inside leaf spots.",
            "Raised, tube-like fungal structures developing on the underside of leaves.",
            "Premature defoliation and small, distorted fruit under severe infection."
        ],
        "possible_causes": [
            "Spores blown by wind from gelatinous galls on nearby juniper/cedar trees during spring rains.",
            "Cool, wet spring weather coinciding with apple leaf emergence."
        ],
        "prevention": [
            "Remove nearby cedar or juniper trees within 1–2 miles of apple orchards where feasible.",
            "Prune and destroy cedar galls from ornamental junipers before spring rains.",
            "Choose rust-resistant apple cultivars such as Redfree, Priscilla, or William's Pride."
        ],
        "basic_recommendations": [
            "Inspect neighboring juniper trees in late winter for brown galls and prune them.",
            "Maintain vigorous tree health through balanced watering and mulching.",
            "Consult local agricultural services for region-specific rust management timing."
        ]
    },

    "Apple - Healthy": {
        "plant_name": "Apple",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The apple leaf exhibits vigorous, uniform green tissue with no signs of fungal lesions, bacterial spots, or pest damage.",
        "symptoms": [
            "Uniform vibrant green coloration across upper and lower leaf surfaces.",
            "Clean leaf margins without curling, necrosis, or scabs.",
            "Normal leaf texture, venation, and turgidity."
        ],
        "possible_causes": [
            "Optimal orchard management, balanced soil nutrition, and appropriate moisture levels."
        ],
        "prevention": [
            "Continue regular seasonal pruning and sanitization practices.",
            "Maintain soil organic matter and monitor for early pest or disease signs."
        ],
        "basic_recommendations": [
            "Maintain routine orchard scouting and balanced irrigation.",
            "Keep soil well-drained and maintain an active mulch ring around the base."
        ]
    },

    "Blueberry - Healthy": {
        "plant_name": "Blueberry",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The blueberry leaf shows optimal vigor, glossy green surface, and absence of fungal leaf spots or chlorosis.",
        "symptoms": [
            "Glossy, deep green foliage with intact margins.",
            "No rust pustules, stem cankers, or leaf mottling.",
            "Consistent shoot growth and strong plant vigor."
        ],
        "possible_causes": [
            "Proper soil acidity (pH 4.5–5.5), adequate organic matter, and consistent drip irrigation."
        ],
        "prevention": [
            "Maintain acidic soil conditions using elemental sulfur or acidic organic mulch (pine bark/needles).",
            "Ensure excellent root aeration and uniform soil moisture."
        ],
        "basic_recommendations": [
            "Continue regular soil pH monitoring and drip irrigation.",
            "Apply pine needle or bark mulch to conserve soil moisture and suppress weeds."
        ]
    },

    "Cherry - Healthy": {
        "plant_name": "Cherry",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The cherry leaf demonstrates healthy leaf development with vibrant green color and absence of powdery mildew, leaf spot, or canker symptoms.",
        "symptoms": [
            "Clean, dark green leaves with serrated margins intact.",
            "No white powdery coatings, yellow halos, or shot-hole perforations.",
            "Sturdy petiole attachment and vigorous branch growth."
        ],
        "possible_causes": [
            "Proper canopy pruning, balanced fertilization, and good orchard airflow."
        ],
        "prevention": [
            "Perform regular winter sanitation pruning and monitor for insect vectors.",
            "Avoid excessive nitrogen fertilization that creates overly lush foliage."
        ],
        "basic_recommendations": [
            "Continue preventative orchard maintenance and clean canopy management.",
            "Ensure trees receive adequate sunlight and well-draining soil."
        ]
    },

    "Cherry - Powdery Mildew": {
        "plant_name": "Cherry",
        "disease_name": "Powdery Mildew",
        "is_healthy": False,
        "short_description": "A fungal disease caused by Podosphaera clandestina resulting in white fungal patches on leaves and terminal shoots.",
        "symptoms": [
            "Patches of white, powdery fungal growth on the underside or upper surface of leaves.",
            "Upward curling, distortion, and hardening of young leaves.",
            "Stunted terminal shoot growth and premature leaf drop.",
            "Russeting or circular white blemishes on developing cherry fruit."
        ],
        "possible_causes": [
            "Fungus Podosphaera clandestina thriving in warm, dry climates with high relative humidity.",
            "Overcrowded branch canopy trapping stagnant, humid air around inner shoots.",
            "Excessive nitrogen fertilization promoting soft, susceptible new growth."
        ],
        "prevention": [
            "Prune dense canopy shoots to improve sunlight penetration and air movement.",
            "Avoid overhead irrigation; water at the tree root zone.",
            "Avoid over-fertilizing with high-nitrogen fertilizers in late spring."
        ],
        "basic_recommendations": [
            "Prune infected shoot tips as soon as symptoms appear and remove from orchard.",
            "Maintain good weed control beneath trees to reduce humidity buildup.",
            "Consult a horticultural expert for approved biorational orchard solutions if needed."
        ]
    },

    "Corn - Common Rust": {
        "plant_name": "Corn",
        "disease_name": "Common Rust",
        "is_healthy": False,
        "short_description": "A fungal disease caused by Puccinia sorghi that produces golden-brown to cinnamon-brown pustules on both upper and lower leaf surfaces of maize.",
        "symptoms": [
            "Oval to elongate, brick-red or cinnamon-brown pustules on leaf blades.",
            "Pustules rupture the leaf epidermis, releasing powdery rust spores.",
            "Yellowing, chlorosis, and necrosis around dense clusters of pustules.",
            "Severe infections cause leaf desiccation and reduced photosynthetic capacity."
        ],
        "possible_causes": [
            "Fungus Puccinia sorghi spores carried northward on wind currents from warmer regions.",
            "Moderate temperatures (16–25°C) combined with high relative humidity (>95%) and dew."
        ],
        "prevention": [
            "Plant rust-resistant or tolerant corn hybrid varieties.",
            "Plant early in the season to allow crops to mature before spore populations peak.",
            "Maintain balanced soil nutrition with adequate potassium levels."
        ],
        "basic_recommendations": [
            "Monitor fields regularly, especially on lower and mid-canopy leaves.",
            "Keep crop records to select more resistant hybrids in future planting seasons.",
            "Consult agricultural extension advisors if rust lesions appear on upper ear leaves prior to silking."
        ]
    },

    "Corn - Gray Leaf Spot": {
        "plant_name": "Corn",
        "disease_name": "Gray Leaf Spot",
        "is_healthy": False,
        "short_description": "A widespread foliar disease of maize caused by Cercospora zeae-maydis, characterized by distinctive rectangular, vein-bounded tan lesions.",
        "symptoms": [
            "Small, tan spots with yellow halos expanding into long, rectangular gray/tan lesions.",
            "Lesions strictly bounded by leaf veins, creating sharp rectangular borders.",
            "Lesions merge under severe pressure, leading to extensive leaf blight and premature drying.",
            "Weakened stalks and increased vulnerability to lodging."
        ],
        "possible_causes": [
            "Fungus Cercospora zeae-maydis overwintering in unburied corn residue.",
            "Warm, humid weather (25–30°C) with prolonged morning dews and overcast skies.",
            "Continuous corn-on-corn planting and minimal tillage systems."
        ],
        "prevention": [
            "Practice crop rotation with non-host crops (such as soybeans, wheat, or alfalfa).",
            "Plant corn hybrids with high genetic tolerance to Gray Leaf Spot.",
            "Manage crop residue to encourage decomposition of infected stalk and leaf debris."
        ],
        "basic_recommendations": [
            "Scout lower leaves before tasseling to determine disease progression.",
            "Avoid high plant densities that restrict airflow in the field.",
            "Seek advice from agronomy specialists regarding disease thresholds and hybrid resistance."
        ]
    },

    "Corn - Healthy": {
        "plant_name": "Corn",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The corn leaf displays uniform green coloration, clear parallel venation, and absence of rust pustules, blights, or insect feeding.",
        "symptoms": [
            "Uniform vibrant green leaf blade with intact margins.",
            "Clean parallel veins without chlorotic streaks or rectangular lesions.",
            "Sturdy leaf whorl and healthy photosynthetic surface."
        ],
        "possible_causes": [
            "Optimal soil fertility, adequate rainfall/irrigation, and effective crop management."
        ],
        "prevention": [
            "Continue standard crop rotation, soil testing, and balanced nitrogen management."
        ],
        "basic_recommendations": [
            "Maintain optimal weed control and scout regularly during critical growth stages (V6 to R2).",
            "Ensure balanced N-P-K nutrition to support stalk strength and yield."
        ]
    },

    "Corn - Northern Leaf Blight": {
        "plant_name": "Corn",
        "disease_name": "Northern Corn Leaf Blight",
        "is_healthy": False,
        "short_description": "A destructive foliar disease caused by Exserohilum turcicum, producing characteristic large, cigar-shaped, grayish-green to tan lesions.",
        "symptoms": [
            "Long, elliptical, cigar-shaped lesions (2.5 to 15 cm long) on leaves.",
            "Lesions initially appear grayish-green, turning tan to brown as tissue dies.",
            "Dark, olive-colored fungal sporulation visible on lesions during damp conditions.",
            "Premature death of entire leaves, reducing grain fill and ear size."
        ],
        "possible_causes": [
            "Fungus Exserohilum turcicum surviving in infected corn residue from previous seasons.",
            "Moderate temperatures (18–27°C) accompanied by extended periods of leaf wetness (6+ hours)."
        ],
        "prevention": [
            "Utilize corn hybrids with single-gene (Ht) or polygenic resistance.",
            "Rotate fields with non-grass crops for at least one to two years.",
            "Incorporate infected residue into the soil to accelerate microbial breakdown."
        ],
        "basic_recommendations": [
            "Scout fields starting at late vegetative stages, focusing on lower leaves.",
            "Maintain proper plant spacing to minimize canopy moisture accumulation.",
            "Consult local agronomic extension experts when symptoms appear prior to tasseling."
        ]
    },

    "Grape - Black Measles": {
        "plant_name": "Grape",
        "disease_name": "Black Measles (Esca Complex)",
        "is_healthy": False,
        "short_description": "A complex vascular and foliar disease caused by a consortium of wood-decay fungi (e.g., Phaeomoniella chlamydospora), causing 'tiger-stripe' leaf patterns and speckled fruit.",
        "symptoms": [
            "'Tiger-stripe' leaf patterns: yellow/reddish interveinal chlorosis and necrosis.",
            "Small, dark brown to purple circular spots ('measles') on berry skins.",
            "Cracking, shriveling, or drying of grape clusters before harvest.",
            "Dieback of cordons and trunk wood showing dark vascular discoloration."
        ],
        "possible_causes": [
            "Fungi entering through dormant pruning wounds on mature grapevines.",
            "High summer temperatures and moisture stress accelerating toxin movement to foliage.",
            "Age of vineyard (typically more severe in vines older than 8–10 years)."
        ],
        "prevention": [
            "Delay pruning until late winter when wound healing is more rapid.",
            "Protect large pruning wounds with wound sealants or protective barriers.",
            "Disinfect pruning shears regularly between vine cuts."
        ],
        "basic_recommendations": [
            "Prune back dead cordons and canes to clean, healthy white wood.",
            "Remove and incinerate infected grapevine cuttings away from the vineyard.",
            "Consult a viticulture specialist for vineyard longevity and cordon renewal programs."
        ]
    },

    "Grape - Black Rot": {
        "plant_name": "Grape",
        "disease_name": "Black Rot",
        "is_healthy": False,
        "short_description": "A severe fungal disease caused by Guignardia bidwellii that attacks all green parts of the grapevine, turning berries into hard, black, wrinkled mummies.",
        "symptoms": [
            "Circular, reddish-brown leaf spots with dark margins and tiny black dots (pycnidia).",
            "Infected berries turn brown, soften, and rapidly shrivel into hard, black, raisin-like mummies.",
            "Black, elongated cankers on young shoots and petioles.",
            "Substantial yield loss if fruit clusters are infected during bloom to veraison."
        ],
        "possible_causes": [
            "Fungus Guignardia bidwellii overwintering in mummified berries on the vine or ground.",
            "Warm, rainy spring and early summer weather (20–27°C)."
        ],
        "prevention": [
            "Remove all mummified fruit clusters from vines during dormant pruning.",
            "Cultivate soil in early spring to bury fallen mummies and reduce spore release.",
            "Open canopy through shoot positioning and leaf removal around fruit zones."
        ],
        "basic_recommendations": [
            "Prune out infected canes and ensure maximum canopy ventilation.",
            "Keep vineyard floor free of tall weeds to promote rapid drying of foliage.",
            "Consult local viticultural extension services for preventative seasonal spray schedules."
        ]
    },

    "Grape - Healthy": {
        "plant_name": "Grape",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The grapevine leaf demonstrates healthy photosynthesis, uniform green color, and clean margins without fungal spots or mildew.",
        "symptoms": [
            "Uniform, healthy green palmately lobed leaf blades.",
            "Intact leaf veins without spots, chlorosis, or necrotic margins.",
            "Strong vine tendril development and vigorous cane growth."
        ],
        "possible_causes": [
            "Good canopy management, balanced soil nutrition, and effective vineyard airflow."
        ],
        "prevention": [
            "Maintain routine canopy tucking, selective leaf pulling, and good vineyard sanitation."
        ],
        "basic_recommendations": [
            "Continue regular vineyard scouting and balanced trellis management.",
            "Maintain optimal drip irrigation and avoid water stress during berry development."
        ]
    },

    "Grape - Leaf Blight": {
        "plant_name": "Grape",
        "disease_name": "Leaf Blight (Isariopsis Clavispora)",
        "is_healthy": False,
        "short_description": "A fungal foliar disease caused by Pseudocercospora vitis (Isariopsis clavispora) causing irregular dark brown lesions and premature leaf drop in late summer.",
        "symptoms": [
            "Irregular, circular to angular dark brown spots on mature leaves.",
            "Spots turn dull brown with distinct yellowish halos.",
            "Foliage becomes brittle, dries out, and drops prematurely.",
            "Weakened vine carbohydrate reserves affecting winter hardiness."
        ],
        "possible_causes": [
            "Fungal spores spreading during warm, humid late-summer conditions.",
            "Dense, unmanaged vine canopies trapping moisture.",
            "Overwintering in fallen vineyard debris."
        ],
        "prevention": [
            "Rake and bury or compost fallen grapevine leaves after autumn harvest.",
            "Improve sunlight and airflow in the canopy by shoot thinning.",
            "Maintain balanced fertilization to prevent overly dense foliage."
        ],
        "basic_recommendations": [
            "Prune congested vines to facilitate rapid foliage drying.",
            "Remove heavily blighted leaves to reduce secondary spore spread.",
            "Consult agricultural experts for vineyard sanitation best practices."
        ]
    },

    "Orange - Citrus Greening": {
        "plant_name": "Orange",
        "disease_name": "Citrus Greening (Huanglongbing / HLB)",
        "is_healthy": False,
        "short_description": "A devastating bacterial disease caused by Candidatus Liberibacter asiaticus, transmitted by Asian citrus psyllids, causing blotchy mottle leaves, tree decline, and bitter, misshapen fruit.",
        "symptoms": [
            "Asymmetric blotchy mottle (yellowing) across leaf veins (not mirrored on both halves).",
            "Yellow shoots and upright, chlorotic 'rabbit-ear' leaves.",
            "Small, lopsided, poorly colored fruit with bitter, sour taste.",
            "Severe root loss, twig dieback, and eventual tree decline."
        ],
        "possible_causes": [
            "Bacterium Candidatus Liberibacter transmitted by Asian citrus psyllid (Diaphorina citri).",
            "Use of infected budwood or nursery grafting stock."
        ],
        "prevention": [
            "Plant only certified disease-free citrus trees from licensed nurseries.",
            "Control Asian citrus psyllid populations using integrated pest management.",
            "Inspect trees regularly for asymmetric yellow blotching.",
            "Follow quarantine rules and do not transport citrus plant material across restricted zones."
        ],
        "basic_recommendations": [
            "Report suspected HLB infections to local agricultural departments.",
            "Provide balanced foliar micronutrient feeding to support infected tree vigor if managed commercially.",
            "Remove severely declining, unproductive trees to eliminate pathogen reservoirs."
        ]
    },

    "Peach - Bacterial Spot": {
        "plant_name": "Peach",
        "disease_name": "Bacterial Spot",
        "is_healthy": False,
        "short_description": "A destructive bacterial disease caused by Xanthomonas arboricola pv. pruni affecting leaves, twigs, and stone fruit, causing shot-hole leaf symptoms and pitted fruit.",
        "symptoms": [
            "Small, water-soaked, angular purple-brown spots on leaf undersides.",
            "Infected tissue drops out, leaving a ragged 'shot-hole' appearance.",
            "Severe yellowing of leaves followed by heavy mid-season defoliation.",
            "Sunken, dark, pitted lesions with gummy exudate on peach fruit."
        ],
        "possible_causes": [
            "Bacterium Xanthomonas arboricola overwintering in twig cankers and bud scales.",
            "Spreading by wind-blown rain and heavy dews in sandy soils during warm weather (21–29°C)."
        ],
        "prevention": [
            "Plant bacterial spot-resistant peach varieties (e.g., Clayton, Candor, Biscoe).",
            "Avoid planting orchards on highly exposed, windy sites with sandy soils.",
            "Prune to promote open canopy structure and rapid drying.",
            "Avoid excess nitrogen fertilizer that encourages succulent, susceptible shoots."
        ],
        "basic_recommendations": [
            "Prune out infected twig cankers during regular winter maintenance.",
            "Maintain optimal tree nutrition with adequate potassium.",
            "Seek guidance from agricultural extension services for spring management strategies."
        ]
    },

    "Peach - Healthy": {
        "plant_name": "Peach",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The peach leaf shows vibrant green color, intact lanceolate blade structure, and complete absence of bacterial spots or shot-hole lesions.",
        "symptoms": [
            "Smooth, lanceolate green leaves with clean finely serrated margins.",
            "No water-soaked spots, shot-holes, or leaf curl symptoms.",
            "Healthy petiole and vigorous shoot growth."
        ],
        "possible_causes": [
            "Balanced soil management, adequate irrigation, and proper orchard airflow."
        ],
        "prevention": [
            "Maintain routine orchard pruning and monitor for stone fruit pests and diseases."
        ],
        "basic_recommendations": [
            "Continue standard seasonal orchard care and soil moisture monitoring.",
            "Apply mulch around tree dripline to conserve root moisture."
        ]
    },

    "Pepper Bell - Bacterial Spot": {
        "plant_name": "Pepper Bell",
        "disease_name": "Bacterial Spot",
        "is_healthy": False,
        "short_description": "A serious bacterial disease caused by Xanthomonas campestris pv. vesicatoria affecting bell pepper leaves and fruit, causing defoliation and sunscald.",
        "symptoms": [
            "Small, circular to irregular water-soaked spots on leaves turning brown/black.",
            "Lesions develop a yellow halo and centers may become thin and papery.",
            "Extensive leaf yellowing and severe premature leaf drop.",
            "Raised, blister-like or scabby spots on green pepper fruit."
        ],
        "possible_causes": [
            "Bacterium Xanthomonas campestris introduced on contaminated seed or transplants.",
            "Spreading rapidly through splashing water, overhead irrigation, and working in wet fields.",
            "High temperatures (24–30°C) combined with high relative humidity."
        ],
        "prevention": [
            "Use certified disease-free seeds and resistant pepper cultivars.",
            "Avoid overhead sprinkler irrigation; use drip irrigation at ground level.",
            "Rotate crops with non-solanaceous plants for at least 2–3 years.",
            "Never handle or cultivate pepper plants when foliage is wet."
        ],
        "basic_recommendations": [
            "Remove and destroy severely infected pepper plants from small garden plots.",
            "Apply organic mulch around plant bases to prevent soil splashing onto lower leaves.",
            "Consult local horticulture advisors for approved preventative copper-based spray schedules."
        ]
    },

    "Pepper Bell - Healthy": {
        "plant_name": "Pepper Bell",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The bell pepper leaf exhibits healthy, glossy green coloration with smooth margins and no signs of bacterial or viral spotting.",
        "symptoms": [
            "Glossy, smooth, deep green leaf blades with intact margins.",
            "No necrotic spots, mosaic mottling, or curling.",
            "Sturdy stem development and normal flower/fruit set."
        ],
        "possible_causes": [
            "Balanced fertilization, proper spacing, and drip irrigation."
        ],
        "prevention": [
            "Maintain consistent watering schedule and scout regularly for aphids or thrips."
        ],
        "basic_recommendations": [
            "Continue regular watering at the base and balanced tomato/pepper fertilizer.",
            "Ensure adequate staking or support as pepper fruits develop."
        ]
    },

    "Potato - Early Blight": {
        "plant_name": "Potato",
        "disease_name": "Early Blight",
        "is_healthy": False,
        "short_description": "A common fungal disease caused by Alternaria solani affecting potato foliage and tubers, recognizable by characteristic concentric 'target-board' leaf lesions.",
        "symptoms": [
            "Dark brown to black circular spots with concentric rings ('target' pattern).",
            "Yellow chlorotic halos surrounding expanding lesions.",
            "Lower and older leaves infected first, gradually progressing upwards.",
            "Premature defoliation resulting in reduced tuber size and yield."
        ],
        "possible_causes": [
            "Fungus Alternaria solani surviving in infected crop debris or solanaceous weeds.",
            "Alternating wet and dry weather cycles with warm temperatures (24–29°C).",
            "Plant stress caused by poor nutrition, heavy tuber load, or nematode pressure."
        ],
        "prevention": [
            "Practice a 3–4 year crop rotation away from potatoes, tomatoes, and eggplants.",
            "Plant certified disease-free seed potatoes.",
            "Maintain optimal soil nitrogen and potassium fertility throughout the season.",
            "Use drip irrigation and avoid late afternoon overhead watering."
        ],
        "basic_recommendations": [
            "Prune off heavily spotted lower leaves to improve airflow and slow disease spread.",
            "Ensure adequate hilling of soil to protect growing tubers from spore wash-off.",
            "Consult local agronomy experts for protective early-season management protocols."
        ]
    },

    "Potato - Healthy": {
        "plant_name": "Potato",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The potato foliage demonstrates lush green color, full leaf expansion, and absence of target spots, late blight lesions, or viral curling.",
        "symptoms": [
            "Lush, compound green leaves with smooth, healthy leaflets.",
            "No water-soaked spots, concentric rings, or mosaic patterns.",
            "Vigorous vine canopy supporting underground tuber development."
        ],
        "possible_causes": [
            "Good soil hilling, certified seed potatoes, and balanced irrigation."
        ],
        "prevention": [
            "Maintain consistent hilling, weed management, and preventative monitoring."
        ],
        "basic_recommendations": [
            "Continue uniform soil moisture management (avoiding waterlogged soil).",
            "Monitor weekly for early signs of blight or Colorado potato beetles."
        ]
    },

    "Potato - Late Blight": {
        "plant_name": "Potato",
        "disease_name": "Late Blight",
        "is_healthy": False,
        "short_description": "A devastating oomycete disease caused by Phytophthora infestans (the pathogen behind the Irish Potato Famine), causing rapid rot of leaves, stems, and tubers.",
        "symptoms": [
            "Large, irregular water-soaked pale green or dark brown lesions on leaves.",
            "White, velvety fungal-like downy growth on the underside of leaves during humid weather.",
            "Dark brown to black lesions rapidly killing entire stems and petioles.",
            "Foul odor and complete collapse of the canopy in severe outbreaks.",
            "Tubers develop a dry, reddish-brown granular rot beneath the skin."
        ],
        "possible_causes": [
            "Oomycete Phytophthora infestans surviving in infected seed tubers, cull piles, or volunteer potatoes.",
            "Cool, wet, foggy weather (10–20°C) with persistent humidity >90%."
        ],
        "prevention": [
            "Plant only certified disease-free seed potatoes.",
            "Destroy all volunteer potato plants and eliminate cull potato piles.",
            "Avoid overhead irrigation; ensure wide row spacing for maximum drying.",
            "Choose potato cultivars with partial late blight resistance."
        ],
        "basic_recommendations": [
            "Immediately remove and bag severely infected plants to prevent airborne spore spread.",
            "Do not harvest tubers from infected fields until vines have been dead for 2–3 weeks.",
            "Contact local agricultural extension services immediately upon confirming late blight."
        ]
    },

    "Raspberry - Healthy": {
        "plant_name": "Raspberry",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The raspberry leaf exhibits healthy serrated compound foliage, uniform green color, and absence of cane blight, rust, or virus symptoms.",
        "symptoms": [
            "Healthy compound leaves with rich green upper surfaces and silvery undersides.",
            "Intact serrated leaf margins without scorch or chlorosis.",
            "Strong primocane and floricane vigor with healthy fruit clusters."
        ],
        "possible_causes": [
            "Well-drained soil, trellised cane management, and appropriate cane pruning."
        ],
        "prevention": [
            "Prune out spent floricanes after harvest and maintain good row spacing."
        ],
        "basic_recommendations": [
            "Maintain consistent soil moisture through drip lines and organic wood chip mulch.",
            "Ensure canes are properly supported on trellises for optimal sun exposure."
        ]
    },

    "Soybean - Healthy": {
        "plant_name": "Soybean",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The soybean trifoliate leaf displays healthy green coloration, normal leaf structure, and no signs of bacterial blight, rust, or fungal leaf spot.",
        "symptoms": [
            "Uniform green trifoliate leaves with clean, intact margins.",
            "No rust pustules, brown spots, or yellow mosaic mottling.",
            "Robust nodulation and vigorous vegetative development."
        ],
        "possible_causes": [
            "Optimal soil fertility, seed inoculation, and timely weed management."
        ],
        "prevention": [
            "Practice annual crop rotation and maintain balanced soil phosphorus/potassium."
        ],
        "basic_recommendations": [
            "Continue regular field scouting throughout flowering and pod-fill stages.",
            "Monitor soil drainage to avoid root rot conditions."
        ]
    },

    "Squash - Powdery Mildew": {
        "plant_name": "Squash",
        "disease_name": "Powdery Mildew",
        "is_healthy": False,
        "short_description": "A prevalent fungal disease caused by Podosphaera xanthii affecting cucurbits, producing conspicuous white powdery fungal patches across leaf surfaces.",
        "symptoms": [
            "White, talcum-like powdery spots on upper and lower leaf surfaces, petioles, and stems.",
            "Spots enlarge rapidly to cover entire leaf surfaces in white fungal growth.",
            "Leaves turn yellow, brown, become brittle, and die prematurely.",
            "Exposed squash fruit suffer sunscald and reduced sugar content."
        ],
        "possible_causes": [
            "Fungus Podosphaera xanthii thriving in dense canopies with low light and high humidity.",
            "Warm, dry weather (20–27°C) following humid mornings.",
            "Overcrowded plant spacing restricting air movement."
        ],
        "prevention": [
            "Select powdery mildew-resistant squash varieties.",
            "Provide ample spacing between squash hills to maximize airflow.",
            "Plant in full sun and avoid shaded garden locations.",
            "Water early in the morning using drip irrigation."
        ],
        "basic_recommendations": [
            "Remove heavily infected older leaves from the base of the plant.",
            "Apply approved organic horticultural oils or potassium bicarbonate early if recommended locally.",
            "Consult local horticulture extension for region-specific cucurbit guidelines."
        ]
    },

    "Strawberry - Healthy": {
        "plant_name": "Strawberry",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The strawberry trifoliate leaf demonstrates vibrant green color, strong leaf turgor, and complete absence of leaf scorch, leaf spot, or powdery mildew.",
        "symptoms": [
            "Glossy, deep green trifoliate leaves with healthy serrated edges.",
            "No purple spots, white centers, or scorched leaf margins.",
            "Strong crown development and prolific flowering/runner production."
        ],
        "possible_causes": [
            "Proper bed drainage, straw mulching, and balanced feeding."
        ],
        "prevention": [
            "Renovate strawberry beds annually and maintain clean straw mulch."
        ],
        "basic_recommendations": [
            "Ensure regular drip irrigation directly at the root zone.",
            "Keep strawberry beds free of weeds to maximize sunlight and airflow."
        ]
    },

    "Strawberry - Leaf Scorch": {
        "plant_name": "Strawberry",
        "disease_name": "Leaf Scorch",
        "is_healthy": False,
        "short_description": "A common fungal disease caused by Diplocarpon earlianum that affects strawberry foliage, calyxes, and runners, causing widespread purple-brown blotches.",
        "symptoms": [
            "Small, irregular dark purple or brown spots on the upper leaf surface.",
            "Spots lack distinct white centers, remaining solid dark purple-brown.",
            "Lesions coalesce, causing leaf margins to curl upward and look 'scorched'.",
            "Severe infection turns entire leaves brown and dry, reducing crown vigor."
        ],
        "possible_causes": [
            "Fungus Diplocarpon earlianum overwintering on living infected leaves and plant debris.",
            "Prolonged leaf wetness and warm, humid weather conditions."
        ],
        "prevention": [
            "Plant resistant strawberry cultivars.",
            "Use drip irrigation rather than overhead sprinklers to keep leaves dry.",
            "Space plants properly in raised beds to ensure good air circulation.",
            "Mow and renovate beds after harvest, removing infected leaf debris."
        ],
        "basic_recommendations": [
            "Remove severely scorched leaves during bed cleanup.",
            "Apply clean straw mulch under fruit to prevent soil splashing.",
            "Seek guidance from agricultural extension agents for seasonal bed renovation practices."
        ]
    },

    "Tomato - Bacterial Spot": {
        "plant_name": "Tomato",
        "disease_name": "Bacterial Spot",
        "is_healthy": False,
        "short_description": "A destructive bacterial disease caused by Xanthomonas species that causes dark, water-soaked spots on tomato leaves, stems, and fruit.",
        "symptoms": [
            "Small, dark brown to black water-soaked spots (2–3 mm) on leaves.",
            "Lesions develop greasy appearance and may have yellow halos.",
            "Leaves turn yellow, brown, and drop prematurely, exposing fruit to sunscald.",
            "Small, raised, scab-like spots on green tomato fruits."
        ],
        "possible_causes": [
            "Bacterium Xanthomonas spp. introduced through infected seeds or transplants.",
            "Splashing rain, overhead watering, and high relative humidity with temperatures >25°C.",
            "Working in tomato patches when plants are damp."
        ],
        "prevention": [
            "Use certified disease-free seed and disease-tested transplants.",
            "Avoid overhead irrigation; water at soil level using drip irrigation.",
            "Rotate tomato crops with non-solanaceous crops for at least 2–3 years.",
            "Disinfect stakes, cages, and pruning tools before each season."
        ],
        "basic_recommendations": [
            "Remove and safely dispose of severely infected plant parts.",
            "Mulch around tomato bases with straw or plastic to stop soil splash.",
            "Consult local agricultural extension experts for organic or copper spray guidelines."
        ]
    },

    "Tomato - Early Blight": {
        "plant_name": "Tomato",
        "disease_name": "Early Blight",
        "is_healthy": False,
        "short_description": "A very common fungal disease caused by Alternaria linariae (A. solani) producing characteristic concentric 'target-like' brown lesions on tomato foliage.",
        "symptoms": [
            "Dark brown to black spots with concentric rings ('target' pattern) on older leaves.",
            "Surrounding leaf tissue turns yellow, leading to premature leaf drop from the bottom up.",
            "Dark, sunken, leathery cankers on stems near the soil line (collar rot).",
            "Sunken, dark lesions on fruit near the stem attachment."
        ],
        "possible_causes": [
            "Fungus Alternaria solani overwintering in infected tomato debris or soil.",
            "Warm, humid weather (24–29°C) with repeated wet/dry cycles.",
            "Under-fertilized or stressed tomato plants with dense lower foliage."
        ],
        "prevention": [
            "Stake or cage tomato plants to keep foliage off the ground.",
            "Prune off the bottom 30 cm of leaves once plants are established.",
            "Mulch soil around plants to prevent fungal spores from splashing up from soil.",
            "Water at the base early in the morning and avoid wetting leaves."
        ],
        "basic_recommendations": [
            "Prune off infected lower leaves as soon as first target spots appear.",
            "Ensure balanced tomato fertilizer with adequate calcium and potassium.",
            "Consult local extension specialists for preventative bio-fungicide options."
        ]
    },

    "Tomato - Healthy": {
        "plant_name": "Tomato",
        "disease_name": "Healthy Foliage",
        "is_healthy": True,
        "short_description": "The tomato leaf demonstrates strong vigor, rich green color, and complete absence of fungal spots, blights, or insect damage.",
        "symptoms": [
            "Deep green, vibrant compound leaves with healthy leaf hairs.",
            "No yellow halos, concentric rings, water-soaked spots, or wilting.",
            "Sturdy stem development and healthy flower truss formation."
        ],
        "possible_causes": [
            "Balanced soil nutrition, consistent watering, and proper staking/air circulation."
        ],
        "prevention": [
            "Maintain baseline pruning of lower suckers and consistent drip watering."
        ],
        "basic_recommendations": [
            "Continue regular watering at the base to avoid blossom end rot.",
            "Stake plants securely and maintain mulch around the base."
        ]
    },

    "Tomato - Late Blight": {
        "plant_name": "Tomato",
        "disease_name": "Late Blight",
        "is_healthy": False,
        "short_description": "A rapid and destructive oomycete disease caused by Phytophthora infestans that can kill mature tomato plants in days during cool, wet weather.",
        "symptoms": [
            "Large, irregular water-soaked pale green or dark greasy spots on leaves.",
            "White, downy fungal-like growth visible on the underside of leaves during high humidity.",
            "Stems develop dark brown to black greasy lesions, becoming brittle.",
            "Fruit develops large, firm, greasy, golden-brown or dark mottled rot patches."
        ],
        "possible_causes": [
            "Oomycete Phytophthora infestans spreading via wind-borne sporangia over miles.",
            "Cool, wet, cloudy weather (15–22°C) with persistent humidity >90%."
        ],
        "prevention": [
            "Choose late blight-resistant tomato varieties (e.g., Mountain Magic, Defiant, Jasper).",
            "Plant in full sun and space plants widely for maximum air circulation.",
            "Avoid overhead watering and keep foliage dry.",
            "Destroy volunteer tomato and potato plants in the garden area."
        ],
        "basic_recommendations": [
            "Immediately remove and bag infected plants to prevent spores spreading to neighboring crops.",
            "Do not compost plants with active late blight.",
            "Contact your local agricultural extension service immediately to track regional blight alerts."
        ]
    },

    "Tomato - Leaf Mold": {
        "plant_name": "Tomato",
        "disease_name": "Leaf Mold",
        "is_healthy": False,
        "short_description": "A fungal disease caused by Passalora fulva (Cladosporium fulvum) common in greenhouse and high-tunnel tomatoes with high humidity.",
        "symptoms": [
            "Pale green to yellowish spots with indistinct margins on the upper leaf surface.",
            "Olive-green to velvety brown mold growth on the corresponding leaf underside.",
            "Infected leaves curl, wither, turn brown, and drop prematurely.",
            "Symptoms start on older lower leaves and progress upwards through the plant."
        ],
        "possible_causes": [
            "Fungus Passalora fulva thriving in environments with relative humidity >85%.",
            "Temperatures between 21–24°C in enclosed or poorly ventilated growing structures."
        ],
        "prevention": [
            "Increase greenhouse or high-tunnel ventilation with fans and ridge vents.",
            "Space plants generously to allow continuous air movement through the canopy.",
            "Water at the base and avoid wetting the foliage.",
            "Choose tomato varieties with genetic resistance to leaf mold races."
        ],
        "basic_recommendations": [
            "Prune lower foliage and suckers to improve internal canopy airflow.",
            "Lower humidity in enclosed spaces below 80% if possible.",
            "Seek advice from greenhouse specialists for humidity management."
        ]
    },

    "Tomato - Mosaic Virus": {
        "plant_name": "Tomato",
        "disease_name": "Mosaic Virus (ToMV / TMV)",
        "is_healthy": False,
        "short_description": "A highly stable plant virus (Tomato Mosaic Virus / Tobacco Mosaic Virus) causing mottled green/yellow leaf patterns, distortion, and stunted growth.",
        "symptoms": [
            "Mottled light and dark green mosaic patterns on foliage.",
            "Distorted, blistered, crinkled, or 'shoestring'-like thin leaves.",
            "Stunted plant growth and reduced flowering.",
            "Uneven ripening, internal browning, and yellow rings on tomato fruit."
        ],
        "possible_causes": [
            "Virus mechanically transmitted via hands, pruning tools, and tobacco products.",
            "Contaminated seed or infected plant debris in soil.",
            "Extremely stable virus that persists on surfaces and dry debris for years."
        ],
        "prevention": [
            "Plant virus-resistant tomato varieties (designated with 'T' or 'ToMV').",
            "Wash hands thoroughly with soap before handling tomato plants (especially tobacco users).",
            "Disinfect pruning tools in a 20% non-fat dry milk solution or 10% bleach.",
            "Control root-feeding nematodes and remove solanaceous weeds around gardens."
        ],
        "basic_recommendations": [
            "Immediately rogue (dig up and destroy) infected plants to prevent mechanical spread.",
            "Do not compost virus-infected plants.",
            "Consult agricultural extension advisors for resistant seed recommendations."
        ]
    },

    "Tomato - Septoria Leaf Spot": {
        "plant_name": "Tomato",
        "disease_name": "Septoria Leaf Spot",
        "is_healthy": False,
        "short_description": "A very prevalent fungal disease caused by Septoria lycopersici characterized by numerous small, circular spots with light gray centers and dark brown margins.",
        "symptoms": [
            "Numerous small (2–3 mm), circular spots with gray/white centers and dark brown borders.",
            "Tiny black specks (pycnidia) visible inside the center of mature spots.",
            "Severe yellowing of affected leaves followed by rapid defoliation from the bottom up.",
            "Fruit is rarely infected directly, but suffers sunscald due to lost canopy."
        ],
        "possible_causes": [
            "Fungus Septoria lycopersici overwintering in tomato debris and solanaceous weeds (e.g., nightshade).",
            "Extended periods of warm (20–25°C), rainy, humid weather with splashing water."
        ],
        "prevention": [
            "Rotate crops for at least 2–3 years away from tomatoes and potatoes.",
            "Mulch heavily around plants to create a barrier between soil and lower leaves.",
            "Prune bottom leaves to maintain a 30 cm clearance above the mulch.",
            "Use drip irrigation and avoid watering late in the day."
        ],
        "basic_recommendations": [
            "Pinch off infected lower leaves at the first sign of small gray spots.",
            "Clean up all fallen tomato debris at the end of the season.",
            "Consult local extension agents for preventative fungal management guidance."
        ]
    },

    "Tomato - Spider Mites": {
        "plant_name": "Tomato",
        "disease_name": "Two-Spotted Spider Mites",
        "is_healthy": False,
        "short_description": "Pest damage caused by microscopic Two-Spotted Spider Mites (Tetranychus urticae) that pierce plant cells, causing yellow stippling and fine webbing.",
        "symptoms": [
            "Fine yellow or white stippling (tiny dots) across the upper leaf surface.",
            "Leaves turn bronze, yellow, dry out, and drop prematurely.",
            "Fine, silky webbing visible on leaf undersides and between stem branches.",
            "Stunted plant growth and poor fruit quality under heavy mite infestations."
        ],
        "possible_causes": [
            "Hot, dry, and dusty weather conditions favoring rapid mite reproduction.",
            "Broad-spectrum insecticides that kill beneficial predatory insects (ladybugs, lacewings, predatory mites)."
        ],
        "prevention": [
            "Keep tomato plants well-watered to reduce drought stress.",
            "Spray undersides of leaves with a strong jet of water to dislodge mites and disrupt webs.",
            "Avoid excessive nitrogen fertilizer which stimulates rapid mite reproduction.",
            "Encourage or release natural predators like predatory mites (Phytoseiulus persimilis)."
        ],
        "basic_recommendations": [
            "Apply insecticidal soap or neem oil spray to leaf undersides early in the morning.",
            "Remove and discard severely infested branches in sealed bags.",
            "Consult an IPM (Integrated Pest Management) specialist for biological control options."
        ]
    },

    "Tomato - Target Spot": {
        "plant_name": "Tomato",
        "disease_name": "Target Spot",
        "is_healthy": False,
        "short_description": "A fungal disease caused by Corynespora cassiicola causing brown lesions with faint concentric rings on leaves, stems, and fruit.",
        "symptoms": [
            "Small, pinpoint brown spots on leaves expanding into circular brown lesions with light centers.",
            "Faint concentric circles visible inside mature lesions.",
            "Extensive leaf yellowing and defoliation in the lower and middle canopy.",
            "Sunken, brown circular pits on ripe and green tomato fruit."
        ],
        "possible_causes": [
            "Fungus Corynespora cassiicola thriving in warm, humid tropical and subtropical conditions.",
            "Dense plant canopies that stay wet for prolonged periods."
        ],
        "prevention": [
            "Improve plant spacing and prune suckers to optimize airflow.",
            "Use drip irrigation to prevent foliage from getting wet.",
            "Remove solanaceous weeds and volunteer plants from the field.",
            "Rotate crops with non-host plants (such as corn or grasses)."
        ],
        "basic_recommendations": [
            "Prune infected leaves from lower stems and destroy them away from the field.",
            "Ensure proper tomato staking and trellis support.",
            "Consult agricultural extension advisors for regional disease management timing."
        ]
    },

    "Tomato - Yellow Leaf Curl Virus": {
        "plant_name": "Tomato",
        "disease_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "is_healthy": False,
        "short_description": "A devastating viral disease transmitted by the sweetpotato whitefly (Bemisia tabaci), causing severe upward leaf cupping, yellowing, and stunted bushy growth.",
        "symptoms": [
            "Severe upward curling and cupping of leaflet margins.",
            "Pronounced yellowing (chlorosis) of leaf margins and interveinal areas.",
            "Significant stunting of new growth, giving the plant a compact, erect, bushy appearance.",
            "Flowers drop before setting fruit; plants infected early produce no marketable fruit."
        ],
        "possible_causes": [
            "Virus transmitted by silverleaf / sweetpotato whiteflies (Bemisia tabaci).",
            "Warm climates supporting year-round whitefly populations.",
            "Infected transplants brought in from other regions."
        ],
        "prevention": [
            "Plant TYLCV-resistant tomato cultivars.",
            "Use fine insect netting / row covers to exclude whiteflies from young plants.",
            "Use reflective silver mulches to repel whitefly vectors.",
            "Control whitefly populations using yellow sticky traps and horticultural oils."
        ],
        "basic_recommendations": [
            "Rogue (pull up and bag) infected plants immediately to prevent whiteflies spreading the virus.",
            "Keep fields free of alternate weed hosts like nightshades and mallows.",
            "Consult local agricultural extension agents for whitefly vector management programs."
        ]
    }
}


def normalize_class_key(class_name: str) -> str:
    """Normalize class name string for flexible lookup."""
    return class_name.strip().replace("—", "-").replace("–", "-")


def get_disease_info(class_name: str) -> Dict[str, Any]:
    """
    Safely retrieve disease information for a predicted class name.
    
    Returns:
        Dictionary with disease profile and guidance, or a safe fallback.
    """
    if not class_name:
        return get_fallback_info("Unknown Class")

    # 1. Exact match lookup
    if class_name in DISEASE_KNOWLEDGE_BASE:
        return DISEASE_KNOWLEDGE_BASE[class_name]

    # 2. Normalized lookup (handle em-dash / en-dash / spaces)
    normalized = normalize_class_key(class_name)
    if normalized in DISEASE_KNOWLEDGE_BASE:
        return DISEASE_KNOWLEDGE_BASE[normalized]

    for key, data in DISEASE_KNOWLEDGE_BASE.items():
        if normalize_class_key(key).lower() == normalized.lower():
            return data

    # 3. Safe fallback if class info is missing
    return get_fallback_info(class_name)


def get_fallback_info(class_name: str) -> Dict[str, Any]:
    """Provide a graceful fallback dictionary if disease info is unavailable."""
    return {
        "plant_name": "Plant",
        "disease_name": class_name,
        "is_healthy": "healthy" in class_name.lower(),
        "short_description": f"Specific agronomic profile data is currently being curated for {class_name}.",
        "symptoms": [
            "Inspect leaf color, texture, and spotting patterns carefully.",
            "Check both upper and lower leaf surfaces for lesions or fungal growth."
        ],
        "possible_causes": [
            "Environmental stress, fungal pathogens, bacteria, or nutrient imbalance."
        ],
        "prevention": [
            "Maintain clean gardening tools and ensure proper plant spacing.",
            "Avoid overhead irrigation and practice crop rotation."
        ],
        "basic_recommendations": [
            "Ensure adequate soil drainage and monitor plant vigor.",
            "Consult a local agricultural extension officer or horticulturist for detailed diagnosis."
        ]
    }
