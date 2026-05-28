extends RefCounted
class_name FoodCommonsInteriorBuilder

const P := preload("res://scripts/CiacInteriorPrimitives.gd")
const WALL_T := 0.3
const WALL_H := 3.25
const DOOR_W := 4.0

static func build(level: Node, geometry_root: Node3D, label_root: Node3D, structure: Dictionary, base: Vector3, size: Vector3, color: Color, interactable_script: Script) -> void:
    var root := Node3D.new()
    root.name = str(structure.get("id", "food_commons"))
    root.position = base
    root.rotation.y = _rotation_toward_quad(base)
    geometry_root.add_child(root)

    P.open_shell(root, size, color, WALL_T, WALL_H, DOOR_W)
    var structure_type := str(structure.get("type", "food_commons"))
    if structure_type == "protein_commons":
        _protein_commons(root, level, interactable_script, structure, size)
    else:
        _hybrid_food_commons(root, level, interactable_script, structure, size)
    _shared_food_safety_band(root, level, interactable_script, structure, size)

    P.plaque(root, level, interactable_script, "FoodCommonsModulesPlaque", Vector3(-size.x * 0.5 + 0.9, 1.4, size.z * 0.5 - 2.1), structure, "Modules and sources")
    P.bulletin(root, level, interactable_script, "FoodCommonsStatusBulletin", Vector3(size.x * 0.5 - 0.68, 1.65, size.z * 0.5 - 2.1), structure, "Commons bulletin")
    P.label(label_root, str(structure.get("label", "Food Commons")), base + Vector3(0.0, WALL_H + 0.9, 0.0), 28)
    P.label(label_root, "food safety board", base + _world_from_local(root, Vector3(size.x * 0.5 - 0.8, 1.8, -size.z * 0.5 + 3.6)), 19)

static func _hybrid_food_commons(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "WashPrepRun", Vector3(-size.x * 0.5 + 2.1, 0.88, -size.z * 0.5 + 3.0), Vector3(3.4, 0.95, 1.2), Color(0.68, 0.68, 0.62), structure, "Wash and prep run", "Food safety prep fixture", "food.hybrid_food_commons.v0_1", ["makes food handling and prep separation visible"], ["Food code compliance requires local professional review."])
    P.fixture_box(root, level, interactable_script, "CookingIsland", Vector3(-2.2, 0.82, -1.4), Vector3(4.4, 0.82, 1.45), Color(0.64, 0.58, 0.48), structure, "Cooking island", "Shared cooking production surface", "food.hybrid_food_commons.v0_1", ["represents shared meal production capacity"], ["Does not validate staffing, menu, or commercial kitchen requirements."])
    P.box(root, "SharedServingRail", Vector3(1.8, 0.72, size.z * 0.5 - 3.6), Vector3(5.8, 0.42, 1.0), Color(0.52, 0.39, 0.28), true)
    P.fixture_box(root, level, interactable_script, "DryPantryShelves", Vector3(size.x * 0.5 - 0.75, 1.5, -size.z * 0.5 + 3.0), Vector3(0.9, 2.4, 4.3), Color(0.48, 0.36, 0.26), structure, "Dry pantry shelves", "Staple inventory fixture", "food.hybrid_food_commons.v0_1", ["represents inspectable food inventory capacity"], ["Inventory math remains in the model, not in this visual fixture."])
    P.fixture_box(root, level, interactable_script, "ColdStore", Vector3(size.x * 0.5 - 2.1, 1.15, -size.z * 0.5 + 6.4), Vector3(2.5, 1.9, 1.5), Color(0.55, 0.67, 0.72), structure, "Cold store", "Refrigerated food safety fixture", "food.hybrid_food_commons.v0_1", ["links food storage to critical energy assumptions"], ["Cold-chain performance is conceptual until engineered."])
    _commons_tables(root, size)

static func _protein_commons(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "CultureBench", Vector3(-size.x * 0.5 + 2.1, 0.9, -size.z * 0.5 + 3.1), Vector3(3.3, 0.9, 1.2), Color(0.66, 0.68, 0.6), structure, "Protein culture bench", "Supplemental protein production fixture", "food.protein_commons_supplement.v0_1", ["represents local supplemental protein production capacity"], ["Resident acceptance and food-safety review remain explicit assumptions."])
    for index in range(3):
        var x := -1.8 + float(index) * 1.8
        P.fixture_box(root, level, interactable_script, "FermentationCabinet%d" % index, Vector3(x, 1.2, -1.0), Vector3(1.0, 2.0, 1.1), Color(0.45, 0.67, 0.58), structure, "Protein culture cabinet %d" % (index + 1), "Controlled production cabinet", "food.protein_commons_supplement.v0_1", ["shows why protein commons needs energy, hygiene, and monitoring"], ["Not a validated process design."])
    P.fixture_box(root, level, interactable_script, "IngredientColdCabinet", Vector3(size.x * 0.5 - 1.4, 1.15, -size.z * 0.5 + 2.8), Vector3(1.5, 1.9, 2.6), Color(0.55, 0.67, 0.72), structure, "Ingredient cold cabinet", "Protein commons cold-chain fixture", "food.protein_commons_supplement.v0_1", ["links supplemental protein to critical energy continuity"], ["Cold-chain standards need review."])
    P.box(root, "ResidentTastingCounter", Vector3(1.2, 0.72, size.z * 0.5 - 3.5), Vector3(5.4, 0.42, 1.0), Color(0.52, 0.39, 0.28), true)
    P.box(root, "ProcessLogDesk", Vector3(-size.x * 0.5 + 2.1, 0.72, size.z * 0.5 - 3.5), Vector3(2.8, 0.42, 1.0), Color(0.42, 0.31, 0.25), true)

static func _shared_food_safety_band(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.box(root, "HandwashStation", Vector3(-size.x * 0.5 + 0.9, 0.92, size.z * 0.5 - 3.7), Vector3(0.9, 0.85, 1.4), Color(0.72, 0.72, 0.68), true)
    P.fixture_box(root, level, interactable_script, "FoodSafetyBoard", Vector3(size.x * 0.5 - 0.68, 1.8, -size.z * 0.5 + 3.6), Vector3(0.18, 1.65, 3.2), Color(0.22, 0.3, 0.34), structure, "Food safety board", "Inspection and protocol visibility board", "", ["makes food safety assumptions inspectable"], ["Local rules, training, and inspection requirements remain unresolved review work."])
    P.box(root, "CleanDirtyDivider", Vector3(0.0, 1.1, -size.z * 0.5 + 6.8), Vector3(size.x - 2.4, 0.16, 0.18), Color(0.9, 0.76, 0.32), true)

static func _commons_tables(root: Node3D, size: Vector3) -> void:
    for index in range(2):
        var x := -2.8 + float(index) * 5.6
        P.box(root, "DiningTable%d" % index, Vector3(x, 0.7, 1.6), Vector3(3.8, 0.28, 1.3), Color(0.44, 0.32, 0.22), true)
        P.box(root, "DiningBenchA%d" % index, Vector3(x, 0.42, 0.55), Vector3(3.6, 0.32, 0.42), Color(0.34, 0.25, 0.18), true)
        P.box(root, "DiningBenchB%d" % index, Vector3(x, 0.42, 2.65), Vector3(3.6, 0.32, 0.42), Color(0.34, 0.25, 0.18), true)

static func _rotation_toward_quad(base: Vector3) -> float:
    if base.z > 12.0:
        return PI
    if base.z < -12.0:
        return 0.0
    if base.x < 0.0:
        return PI * 0.5
    return -PI * 0.5

static func _world_from_local(root: Node3D, local: Vector3) -> Vector3:
    return local.rotated(Vector3.UP, root.rotation.y)
