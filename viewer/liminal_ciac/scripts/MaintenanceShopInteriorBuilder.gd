extends RefCounted
class_name MaintenanceShopInteriorBuilder

const P := preload("res://scripts/CiacInteriorPrimitives.gd")
const WALL_T := 0.3
const WALL_H := 3.25
const DOOR_W := 4.2

static func build(level: Node, geometry_root: Node3D, label_root: Node3D, structure: Dictionary, base: Vector3, size: Vector3, color: Color, interactable_script: Script) -> void:
    var root := Node3D.new()
    root.name = str(structure.get("id", "maintenance_shop"))
    root.position = base
    root.rotation.y = 0.0 if base.z < 0.0 else PI
    geometry_root.add_child(root)

    P.open_shell(root, size, color, WALL_T, WALL_H, DOOR_W)
    _repair_bay(root, size)
    _tool_library(root, level, interactable_script, structure, size)
    _parts_inventory(root, level, interactable_script, structure, size)
    _maintenance_board(root, level, interactable_script, structure, size)
    _steward_workbench(root, level, interactable_script, structure, size)

    P.plaque(root, level, interactable_script, "MaintenanceModulesPlaque", Vector3(-size.x * 0.5 + 0.9, 1.4, size.z * 0.5 - 2.1), structure, "Modules and sources")
    P.bulletin(root, level, interactable_script, "MaintenanceStatusBulletin", Vector3(size.x * 0.5 - 0.68, 1.65, size.z * 0.5 - 2.1), structure, "Shop bulletin")
    P.label(label_root, str(structure.get("label", "Maintenance Shop")), base + Vector3(0.0, WALL_H + 0.9, 0.0), 28)
    P.label(label_root, "asset board", base + _world_from_local(root, Vector3(size.x * 0.5 - 0.8, 1.8, -size.z * 0.5 + 3.8)), 19)

static func _repair_bay(root: Node3D, size: Vector3) -> void:
    P.box(root, "RepairBayMat", Vector3(1.4, 0.08, 0.2), Vector3(6.4, 0.08, 4.2), Color(0.34, 0.36, 0.34), true)
    P.box(root, "CartLift", Vector3(1.4, 0.35, 0.2), Vector3(3.4, 0.28, 1.8), Color(0.52, 0.52, 0.48), true)
    P.box(root, "MobileWorkCart", Vector3(4.9, 0.68, -1.2), Vector3(1.1, 0.9, 1.4), Color(0.74, 0.48, 0.24), true)

static func _tool_library(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "ToolLibraryWall", Vector3(-size.x * 0.5 + 0.75, 1.55, -1.5), Vector3(0.9, 2.55, 7.4), Color(0.48, 0.36, 0.26), structure, "Tool library wall", "Shared maintenance tool access fixture", "maintenance.maintainable_commons_spine.v0_1", ["makes shared maintenance capacity visible"], ["Tool access rules and safety training remain review items."])
    for index in range(4):
        var z := -4.2 + float(index) * 1.9
        P.box(root, "ToolRack%d" % index, Vector3(-size.x * 0.5 + 1.5, 1.35, z), Vector3(0.35, 1.45, 1.15), Color(0.28, 0.32, 0.34), true)

static func _parts_inventory(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "PartsShelfA", Vector3(-1.8, 1.25, -size.z * 0.5 + 1.0), Vector3(4.4, 2.0, 0.8), Color(0.5, 0.38, 0.27), structure, "Parts inventory shelf", "Maintainability and spare-parts fixture", "maintenance.maintainable_commons_spine.v0_1", ["represents avoiding deferred maintenance through visible spare capacity"], ["Actual quantities belong in the maintenance ledger."])
    P.box(root, "PartsShelfB", Vector3(3.6, 1.25, -size.z * 0.5 + 1.0), Vector3(4.4, 2.0, 0.8), Color(0.5, 0.38, 0.27), true)
    P.fixture_box(root, level, interactable_script, "CriticalSparesLocker", Vector3(size.x * 0.5 - 1.0, 1.2, -size.z * 0.5 + 1.7), Vector3(1.1, 1.9, 2.1), Color(0.55, 0.58, 0.62), structure, "Critical spares locker", "Failure recovery fixture", "maintenance.maintainable_commons_spine.v0_1", ["links maintenance readiness to graceful degradation"], ["Does not certify that critical spare counts are sufficient."])

static func _maintenance_board(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.fixture_box(root, level, interactable_script, "AssetRegistryBoard", Vector3(size.x * 0.5 - 0.68, 1.8, -size.z * 0.5 + 3.8), Vector3(0.18, 1.8, 4.2), Color(0.22, 0.3, 0.34), structure, "Asset registry board", "Maintenance queue and asset visibility board", "maintenance.maintainable_commons_spine.v0_1", ["makes maintenance backlog and hidden labor risks inspectable"], ["Should reflect the actual model ledger in a future sprint."])
    P.local_label(root, _maintenance_board_text(structure), Vector3(size.x * 0.5 - 0.9, 2.05, -size.z * 0.5 + 3.8), 17, Color(1.0, 0.9, 0.76))
    P.box(root, "QueuePriorityRail", Vector3(size.x * 0.5 - 0.9, 0.62, -size.z * 0.5 + 6.4), Vector3(0.3, 0.55, 2.7), Color(0.9, 0.76, 0.32), true)

static func _steward_workbench(root: Node3D, level: Node, interactable_script: Script, structure: Dictionary, size: Vector3) -> void:
    P.box(root, "StewardBench", Vector3(-2.5, 0.78, size.z * 0.5 - 3.2), Vector3(5.2, 0.42, 1.2), Color(0.42, 0.31, 0.25), true)
    P.box(root, "BenchSeat", Vector3(-2.5, 0.42, size.z * 0.5 - 4.35), Vector3(4.8, 0.34, 0.5), Color(0.32, 0.48, 0.47), true)
    P.fixture_box(root, level, interactable_script, "SafetyPpeLocker", Vector3(size.x * 0.5 - 1.1, 1.15, size.z * 0.5 - 3.2), Vector3(1.2, 1.8, 1.8), Color(0.62, 0.58, 0.52), structure, "Maintenance PPE locker", "Worker safety fixture", "maintenance.maintainable_commons_spine.v0_1", ["keeps maintenance labor from becoming invisible or unsafe"], ["Training and role boundaries remain explicit requirements."])

static func _world_from_local(root: Node3D, local: Vector3) -> Vector3:
    return local.rotated(Vector3.UP, root.rotation.y)

static func _maintenance_board_text(structure: Dictionary) -> String:
    var state: Dictionary = _dict_value(structure, "state")
    return "MAINTENANCE\nstatus %s\nmodules %d\noccupancy %s\ncritical spares visible" % [
        str(state.get("status", "unknown")).to_upper(),
        _array_value(structure, "module_refs").size(),
        str(state.get("occupancy", "unknown"))
    ]

static func _dict_value(source: Dictionary, key: String) -> Dictionary:
    var value: Variant = source.get(key, {})
    if typeof(value) == TYPE_DICTIONARY:
        return value
    return {}

static func _array_value(source: Dictionary, key: String) -> Array:
    var value: Variant = source.get(key, [])
    if typeof(value) == TYPE_ARRAY:
        return value
    return []
