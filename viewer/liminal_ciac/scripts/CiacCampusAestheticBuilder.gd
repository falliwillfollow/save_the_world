extends RefCounted
class_name CiacCampusAestheticBuilder

const PATH_STONE := Color(0.72, 0.67, 0.56)
const PATH_EDGE := Color(0.45, 0.36, 0.28)
const QUAD_GRASS := Color(0.28, 0.42, 0.31)
const PLANTING := Color(0.21, 0.34, 0.24)
const BRICK := Color(0.58, 0.34, 0.24)
const LIMESTONE := Color(0.78, 0.72, 0.63)
const GLASS := Color(0.24, 0.38, 0.42)
const LAMP := Color(0.94, 0.82, 0.55)

static func build_site(root: Node3D, label_root: Node3D) -> void:
    _box(root, "MainMallStone", Vector3(0.0, 0.095, 8.0), Vector3(5.2, 0.07, 110.0), PATH_STONE, false)
    _box(root, "DiningWalkStone", Vector3(0.0, 0.1, 38.0), Vector3(56.0, 0.07, 4.2), PATH_STONE, false)
    _box(root, "ResidentialNorthWalkStone", Vector3(0.0, 0.1, 25.5), Vector3(92.0, 0.07, 3.2), PATH_STONE.darkened(0.03), false)
    _box(root, "ResidentialSouthWalkStone", Vector3(0.0, 0.1, -25.5), Vector3(92.0, 0.07, 3.2), PATH_STONE.darkened(0.03), false)
    _box(root, "ServiceWalkStone", Vector3(8.0, 0.1, -44.0), Vector3(82.0, 0.07, 3.0), PATH_STONE.darkened(0.08), false)

    _box(root, "NorthQuadLawn", Vector3(0.0, 0.08, 17.0), Vector3(52.0, 0.06, 17.0), QUAD_GRASS, false)
    _box(root, "SouthQuadLawn", Vector3(0.0, 0.08, -8.0), Vector3(52.0, 0.06, 22.0), QUAD_GRASS, false)
    _box(root, "WestResidenceGreen", Vector3(-42.0, 0.08, 0.0), Vector3(14.0, 0.06, 34.0), QUAD_GRASS.darkened(0.05), false)
    _box(root, "EastResidenceGreen", Vector3(42.0, 0.08, 0.0), Vector3(14.0, 0.06, 34.0), QUAD_GRASS.darkened(0.05), false)

    _cylinder(root, "FoundersCourt", Vector3(0.0, 0.14, 8.0), 7.0, 0.08, Color(0.66, 0.6, 0.48), false, 48)
    _cylinder(root, "FoundersCourtInner", Vector3(0.0, 0.2, 8.0), 3.5, 0.08, Color(0.36, 0.47, 0.44), false, 48)
    _monument_sign(root, "FoundersGreenSign", Vector3(0.0, 0.65, 15.4), "FOUNDERS GREEN")

    for z in [-38.0, -26.0, -14.0, 0.0, 14.0, 28.0, 42.0, 54.0]:
        _lamp(root, Vector3(-4.1, 0.0, z))
        _lamp(root, Vector3(4.1, 0.0, z))

    for z in [-32.0, -18.0, -4.0, 12.0, 26.0, 40.0]:
        _tree(root, Vector3(-36.0, 0.0, z), 1.0)
        _tree(root, Vector3(36.0, 0.0, z), 1.0)

    for x in [-52.0, -40.0, -28.0, 28.0, 40.0, 52.0]:
        _tree(root, Vector3(x, 0.0, 31.0), 0.88)
        _tree(root, Vector3(x, 0.0, -31.0), 0.88)

    _bench(root, Vector3(-9.0, 0.18, 12.0), 0.0)
    _bench(root, Vector3(9.0, 0.18, 12.0), 0.0)
    _bench(root, Vector3(-9.0, 0.18, 2.0), PI)
    _bench(root, Vector3(9.0, 0.18, 2.0), PI)
    _bench(root, Vector3(-28.0, 0.18, 39.8), PI * 0.5)
    _bench(root, Vector3(28.0, 0.18, 39.8), PI * 0.5)

static func decorate_structure(root: Node3D, label_root: Node3D, record: Dictionary, position: Vector3, size: Vector3, base_color: Color) -> void:
    var structure_type := str(record.get("type", "structure"))
    var system_color := _system_accent(record, base_color)
    var front_z := size.z * 0.5
    var back_z := -size.z * 0.5
    var half_x := size.x * 0.5
    var floors := _floor_count(record)

    _box(root, "%sPlinth" % str(record.get("id", "structure")), position + Vector3(0.0, 0.18, 0.0), Vector3(size.x + 1.3, 0.36, size.z + 1.3), LIMESTONE.darkened(0.12), false)
    _vertical_facade_shell(root, record, position, size, base_color, floors)
    _floor_bands(root, record, position, size, floors)
    _box(root, "%sCornice" % str(record.get("id", "structure")), position + Vector3(0.0, size.y + 0.34, 0.0), Vector3(size.x + 0.9, 0.28, size.z + 0.9), LIMESTONE, false)
    _box(root, "%sSystemBand" % str(record.get("id", "structure")), position + Vector3(0.0, size.y + 0.08, front_z + 0.1), Vector3(size.x + 0.6, 0.18, 0.14), system_color.lightened(0.18), false)

    var entry_width := minf(maxf(size.x * 0.34, 4.2), 8.0)
    _box(root, "%sEntryCanopy" % str(record.get("id", "structure")), position + Vector3(0.0, 2.75, front_z + 1.05), Vector3(entry_width + 1.4, 0.24, 2.1), LIMESTONE.lightened(0.08), false)
    _entry_reveal(root, str(record.get("id", "structure")), position, front_z, entry_width)

    var column_count := 2
    if size.x >= 22.0:
        column_count = 4
    if structure_type == "common_house":
        column_count = 6
    var column_offsets: Array = _portico_column_offsets(entry_width, column_count)
    for i in range(column_offsets.size()):
        var column_x := float(column_offsets[i])
        _cylinder(root, "%sColumn%d" % [str(record.get("id", "structure")), i], position + Vector3(column_x, 1.42, front_z + 0.78), 0.16, 2.85, LIMESTONE.lightened(0.06), false, 18)

    var window_count := maxi(int(size.x / 5.0), 2)
    for i in range(window_count):
        var t := 0.5
        if window_count > 1:
            t = float(i) / float(window_count - 1)
        var x := lerpf(-half_x + 2.0, half_x - 2.0, t)
        if absf(x) < entry_width * 0.42:
            continue
        _box(root, "%sFrontWindow%d" % [str(record.get("id", "structure")), i], position + Vector3(x, 2.05, front_z + 0.11), Vector3(1.35, 0.82, 0.1), GLASS, false)
        _box(root, "%sBackWindow%d" % [str(record.get("id", "structure")), i], position + Vector3(x, 2.05, back_z - 0.11), Vector3(1.35, 0.82, 0.1), GLASS.darkened(0.08), false)
        _upper_windows(root, record, position, size, x, i, floors)

    var sign_text := _department_name(structure_type)
    _facade_sign(root, str(record.get("id", "structure")), position, front_z, sign_text, entry_width)
    if floors > 1:
        _floor_count_plaque(root, str(record.get("id", "structure")), position + Vector3(-half_x + 1.25, 2.55, front_z + 0.2), floors)
        _vertical_core(root, record, position, size, floors)
        _front_access_tower(root, record, position, size, floors)
        _upper_level_program_shells(root, record, position, size, floors, structure_type)
        _balcony_or_roof_edge(root, record, position, size, floors, structure_type)

    if structure_type == "residential_pod":
        _box(root, "%sGardenEdge" % str(record.get("id", "structure")), position + Vector3(0.0, 0.16, front_z + 2.45), Vector3(size.x * 0.82, 0.28, 0.8), PLANTING, false)
    elif structure_type == "common_house":
        _box(root, "%sArcadePaving" % str(record.get("id", "structure")), position + Vector3(0.0, 0.13, front_z + 2.6), Vector3(size.x * 0.72, 0.08, 2.8), PATH_STONE.lightened(0.04), false)
    elif structure_type == "maintenance_shop":
        _box(root, "%sServiceApron" % str(record.get("id", "structure")), position + Vector3(0.0, 0.11, front_z + 2.6), Vector3(size.x * 0.72, 0.08, 3.6), Color(0.38, 0.38, 0.36), false)

static func _vertical_facade_shell(root: Node3D, record: Dictionary, position: Vector3, size: Vector3, color: Color, floors: int) -> void:
    if floors <= 1:
        return
    var record_id := str(record.get("id", "structure"))
    var ground_wall_h := 3.25
    var upper_h := maxf(size.y - ground_wall_h, 0.0)
    if upper_h <= 0.35:
        return
    var y := ground_wall_h + upper_h * 0.5
    var facade_color := color.lightened(0.05)
    var wall_t := 0.18
    _box(root, "%sUpperBackFacade" % record_id, position + Vector3(0.0, y, -size.z * 0.5 - 0.04), Vector3(size.x, upper_h, wall_t), facade_color.darkened(0.02), false)
    _box(root, "%sUpperLeftFacade" % record_id, position + Vector3(-size.x * 0.5 - 0.04, y, 0.0), Vector3(wall_t, upper_h, size.z), facade_color, false)
    _box(root, "%sUpperRightFacade" % record_id, position + Vector3(size.x * 0.5 + 0.04, y, 0.0), Vector3(wall_t, upper_h, size.z), facade_color, false)
    _box(root, "%sUpperFrontFacade" % record_id, position + Vector3(0.0, y, size.z * 0.5 + 0.04), Vector3(size.x, upper_h, wall_t), facade_color.lightened(0.04), false)

static func _floor_bands(root: Node3D, record: Dictionary, position: Vector3, size: Vector3, floors: int) -> void:
    if floors <= 1:
        return
    var record_id := str(record.get("id", "structure"))
    for floor_index in range(1, floors):
        var y := 0.55 + float(floor_index) * 3.15
        if y >= size.y - 0.3:
            continue
        _box(root, "%sFloorBandFront%d" % [record_id, floor_index], position + Vector3(0.0, y, size.z * 0.5 + 0.16), Vector3(size.x + 0.45, 0.16, 0.12), LIMESTONE.darkened(0.02), false)
        _box(root, "%sFloorBandBack%d" % [record_id, floor_index], position + Vector3(0.0, y, -size.z * 0.5 - 0.16), Vector3(size.x + 0.45, 0.16, 0.12), LIMESTONE.darkened(0.08), false)
        _box(root, "%sFloorBandLeft%d" % [record_id, floor_index], position + Vector3(-size.x * 0.5 - 0.16, y, 0.0), Vector3(0.12, 0.16, size.z + 0.45), LIMESTONE.darkened(0.06), false)
        _box(root, "%sFloorBandRight%d" % [record_id, floor_index], position + Vector3(size.x * 0.5 + 0.16, y, 0.0), Vector3(0.12, 0.16, size.z + 0.45), LIMESTONE.darkened(0.06), false)

static func _upper_windows(root: Node3D, record: Dictionary, position: Vector3, size: Vector3, x: float, window_index: int, floors: int) -> void:
    if floors <= 1:
        return
    var record_id := str(record.get("id", "structure"))
    var front_z := size.z * 0.5
    var back_z := -size.z * 0.5
    for floor_index in range(1, floors):
        var y := 0.55 + float(floor_index) * 3.15 + 1.45
        if y > size.y - 0.75:
            continue
        _box(root, "%sFrontUpperWindow%d_%d" % [record_id, floor_index, window_index], position + Vector3(x, y, front_z + 0.15), Vector3(1.18, 0.78, 0.1), GLASS.lightened(0.04), false)
        _box(root, "%sBackUpperWindow%d_%d" % [record_id, floor_index, window_index], position + Vector3(x, y, back_z - 0.15), Vector3(1.18, 0.78, 0.1), GLASS.darkened(0.08), false)

static func _vertical_core(root: Node3D, record: Dictionary, position: Vector3, size: Vector3, floors: int) -> void:
    var record_id := str(record.get("id", "structure"))
    var core_height := maxf(size.y - 0.45, 3.2)
    var side_x := size.x * 0.5 + 0.78
    var core_z := -size.z * 0.25
    _box(root, "%sStairCore" % record_id, position + Vector3(side_x, core_height * 0.5, core_z), Vector3(1.35, core_height, 2.2), LIMESTONE.darkened(0.12), false)
    _box(root, "%sStairCoreGlass" % record_id, position + Vector3(side_x + 0.02, core_height * 0.56, core_z + 1.12), Vector3(0.9, core_height * 0.62, 0.1), GLASS.lightened(0.08), false)
    for floor_index in range(1, floors):
        var y := 0.55 + float(floor_index) * 3.15
        if y < size.y:
            _box(root, "%sStairLanding%d" % [record_id, floor_index], position + Vector3(side_x - 0.25, y, core_z + 1.22), Vector3(1.85, 0.12, 1.2), LIMESTONE.lightened(0.02), true)
            _stair_flight(root, "%sStairFlight%d" % [record_id, floor_index], position + Vector3(side_x, y - 1.2, core_z + 0.25), floor_index)
            _box(root, "%sElevatorDoor%d" % [record_id, floor_index], position + Vector3(side_x - 0.7, y + 0.55, core_z + 1.14), Vector3(0.08, 1.1, 0.72), GLASS.darkened(0.08), false)

static func _front_access_tower(root: Node3D, record: Dictionary, position: Vector3, size: Vector3, floors: int) -> void:
    var record_id := str(record.get("id", "structure"))
    var tower_height := maxf(size.y - 0.15, 6.8)
    var front_z := size.z * 0.5 + 2.05
    var tower_x := size.x * 0.5 - 2.1
    var tower_center := position + Vector3(tower_x, tower_height * 0.5, front_z)
    var tower_w := 2.4
    var tower_d := 3.2
    _box(root, "%sVisibleAccessTowerGlass" % record_id, tower_center, Vector3(tower_w, tower_height, 0.12), GLASS.lightened(0.12), false)
    _box(root, "%sVisibleAccessTowerBack" % record_id, position + Vector3(tower_x, tower_height * 0.5, front_z - tower_d), Vector3(tower_w, tower_height, 0.14), LIMESTONE.darkened(0.12), false)
    _box(root, "%sVisibleAccessTowerLeft" % record_id, position + Vector3(tower_x - tower_w * 0.5, tower_height * 0.5, front_z - tower_d * 0.5), Vector3(0.14, tower_height, tower_d), LIMESTONE.darkened(0.08), false)
    _box(root, "%sVisibleAccessTowerRight" % record_id, position + Vector3(tower_x + tower_w * 0.5, tower_height * 0.5, front_z - tower_d * 0.5), Vector3(0.14, tower_height, tower_d), LIMESTONE.darkened(0.08), false)
    _box(root, "%sVisibleAccessTowerRoof" % record_id, position + Vector3(tower_x, tower_height + 0.18, front_z - tower_d * 0.5), Vector3(tower_w + 0.35, 0.26, tower_d + 0.35), LIMESTONE, false)

    _box(root, "%sGroundElevatorDoor" % record_id, position + Vector3(tower_x - 0.54, 1.15, front_z + 0.08), Vector3(0.72, 1.75, 0.1), GLASS.darkened(0.12), false)
    _box(root, "%sGroundStairDoor" % record_id, position + Vector3(tower_x + 0.54, 1.1, front_z + 0.08), Vector3(0.72, 1.55, 0.1), Color(0.18, 0.2, 0.19), false)
    _access_sign(root, "%sAccessTowerSign" % record_id, position + Vector3(tower_x, 2.45, front_z + 0.15))

    for floor_index in range(1, floors):
        var floor_y := 0.55 + float(floor_index) * 3.15
        if floor_y >= tower_height:
            continue
        _box(root, "%sAccessLanding%d" % [record_id, floor_index], position + Vector3(tower_x, floor_y, front_z - tower_d * 0.45), Vector3(tower_w - 0.35, 0.12, 1.05), LIMESTONE.lightened(0.04), true)
        _box(root, "%sAccessElevatorDoor%d" % [record_id, floor_index], position + Vector3(tower_x - 0.56, floor_y + 0.75, front_z + 0.08), Vector3(0.7, 1.25, 0.1), GLASS.darkened(0.1), false)
        _visible_switchback_stair(root, "%sVisibleStair%d" % [record_id, floor_index], position + Vector3(tower_x + 0.5, floor_y - 1.36, front_z - tower_d * 0.52), floor_index)

static func _access_sign(root: Node3D, node_name: String, position: Vector3) -> void:
    var sign_root := Node3D.new()
    sign_root.name = node_name
    sign_root.position = position
    root.add_child(sign_root)
    _box(sign_root, "AccessSignPanel", Vector3.ZERO, Vector3(1.95, 0.44, 0.08), Color(0.17, 0.2, 0.2), false)
    var label := Label3D.new()
    label.name = "AccessSignText"
    label.text = "STAIR / LIFT"
    label.position = Vector3(0.0, 0.0, 0.06)
    label.font_size = 22
    label.pixel_size = 0.01
    label.modulate = Color(0.92, 0.88, 0.74)
    sign_root.add_child(label)

static func _visible_switchback_stair(root: Node3D, node_name: String, position: Vector3, floor_index: int) -> void:
    var direction := 1.0 if floor_index % 2 == 1 else -1.0
    for step_index in range(10):
        var t := float(step_index) / 9.0
        _box(
            root,
            "%sTread%d" % [node_name, step_index],
            position + Vector3(0.0, t * 2.45, direction * (-1.0 + t * 2.0)),
            Vector3(1.02, 0.11, 0.32),
            LIMESTONE.darkened(0.06),
            true
        )
    _box(root, "%sHandrailA" % node_name, position + Vector3(-0.58, 1.45, 0.0), Vector3(0.07, 2.7, 2.32), Color(0.2, 0.22, 0.21), false)
    _box(root, "%sHandrailB" % node_name, position + Vector3(0.58, 1.45, 0.0), Vector3(0.07, 2.7, 2.32), Color(0.2, 0.22, 0.21), false)

static func _upper_level_program_shells(root: Node3D, record: Dictionary, position: Vector3, size: Vector3, floors: int, structure_type: String) -> void:
    var record_id := str(record.get("id", "structure"))
    for floor_index in range(1, floors):
        var floor_y := 0.55 + float(floor_index) * 3.15
        if floor_y >= size.y - 0.25:
            continue
        _box(root, "%sUpperFloorSlab%d" % [record_id, floor_index], position + Vector3(0.0, floor_y, 0.0), Vector3(size.x - 1.4, 0.1, size.z - 1.4), Color(0.54, 0.5, 0.43), true)
        var room_color := _upper_program_color(structure_type)
        _box(root, "%sUpperProgramNorth%d" % [record_id, floor_index], position + Vector3(-size.x * 0.22, floor_y + 0.58, -size.z * 0.25), Vector3(size.x * 0.28, 0.95, size.z * 0.24), room_color, false)
        _box(root, "%sUpperProgramSouth%d" % [record_id, floor_index], position + Vector3(size.x * 0.2, floor_y + 0.58, size.z * 0.18), Vector3(size.x * 0.32, 0.95, size.z * 0.22), room_color.lightened(0.06), false)

static func _stair_flight(root: Node3D, node_name: String, position: Vector3, floor_index: int) -> void:
    var direction := 1.0 if floor_index % 2 == 1 else -1.0
    for step_index in range(7):
        var t := float(step_index) / 6.0
        _box(
            root,
            "%sStep%d" % [node_name, step_index],
            position + Vector3(0.0, t * 1.85, direction * (-0.72 + t * 1.44)),
            Vector3(1.0, 0.12, 0.34),
            LIMESTONE.darkened(0.08),
            true
        )

static func _upper_program_color(structure_type: String) -> Color:
    match structure_type:
        "residential_pod":
            return Color(0.5, 0.47, 0.42)
        "common_house":
            return Color(0.54, 0.5, 0.39)
        "quiet_studio":
            return Color(0.42, 0.5, 0.52)
        "care_room":
            return Color(0.58, 0.44, 0.5)
        "food_commons", "protein_commons":
            return Color(0.46, 0.56, 0.42)
        "maintenance_shop":
            return Color(0.48, 0.46, 0.42)
        _:
            return Color(0.5, 0.5, 0.46)

static func _balcony_or_roof_edge(root: Node3D, record: Dictionary, position: Vector3, size: Vector3, floors: int, structure_type: String) -> void:
    var record_id := str(record.get("id", "structure"))
    var front_z := size.z * 0.5
    if structure_type == "common_house":
        _box(root, "%sRoofTerrace" % record_id, position + Vector3(0.0, size.y + 0.58, 0.0), Vector3(size.x * 0.52, 0.12, size.z * 0.36), PATH_STONE.lightened(0.08), false)
        _box(root, "%sRoofParapetFront" % record_id, position + Vector3(0.0, size.y + 0.9, size.z * 0.18), Vector3(size.x * 0.52, 0.42, 0.16), LIMESTONE.darkened(0.05), false)
        _box(root, "%sRoofPlanter" % record_id, position + Vector3(-size.x * 0.2, size.y + 0.88, -size.z * 0.08), Vector3(3.8, 0.42, 0.8), PLANTING, false)
    elif structure_type == "residential_pod":
        _box(root, "%sUpperBalcony" % record_id, position + Vector3(0.0, 4.05, front_z + 0.92), Vector3(size.x * 0.46, 0.16, 1.05), LIMESTONE.darkened(0.04), false)
        _box(root, "%sUpperBalconyRail" % record_id, position + Vector3(0.0, 4.42, front_z + 1.42), Vector3(size.x * 0.46, 0.42, 0.1), LIMESTONE.lightened(0.04), false)
    else:
        _box(root, "%sParapetFront" % record_id, position + Vector3(0.0, size.y + 0.62, front_z + 0.12), Vector3(size.x * 0.82, 0.36, 0.14), LIMESTONE.darkened(0.04), false)

static func _floor_count(record: Dictionary) -> int:
    var scale_value: Variant = record.get("scale", {})
    if typeof(scale_value) == TYPE_DICTIONARY:
        var scale: Dictionary = scale_value
        return int(scale.get("floor_count", 1))
    return 1

static func _department_name(structure_type: String) -> String:
    match structure_type:
        "common_house":
            return "COMMON HOUSE"
        "residential_pod":
            return "RESIDENTIAL COLLEGE"
        "food_commons":
            return "DINING COMMONS"
        "protein_commons":
            return "PROTEIN LAB"
        "care_room":
            return "CARE CLINIC"
        "social_cultural":
            return "CULTURE COMMONS"
        "maintenance_shop":
            return "STEWARDSHIP SHOP"
        "quiet_studio":
            return "QUIET STUDIO"
        _:
            return "CIVIC BUILDING"

static func _facade_sign(root: Node3D, record_id: String, position: Vector3, front_z: float, text: String, entry_width: float) -> void:
    var sign_root := Node3D.new()
    sign_root.name = "%sFacadeSign" % record_id
    sign_root.position = position + Vector3(0.0, 3.28, front_z + 0.28)
    root.add_child(sign_root)
    _box(sign_root, "SignPanel", Vector3.ZERO, Vector3(entry_width + 1.0, 0.48, 0.08), Color(0.17, 0.2, 0.2), false)
    var label := Label3D.new()
    label.name = "SignText"
    label.text = text
    label.position = Vector3(0.0, -0.02, 0.055)
    label.font_size = 30
    label.pixel_size = 0.012
    label.modulate = Color(0.92, 0.88, 0.74)
    sign_root.add_child(label)

static func _floor_count_plaque(root: Node3D, record_id: String, position: Vector3, floors: int) -> void:
    var plaque_root := Node3D.new()
    plaque_root.name = "%sFloorCountPlaque" % record_id
    plaque_root.position = position
    root.add_child(plaque_root)
    _box(plaque_root, "PlaquePanel", Vector3.ZERO, Vector3(0.08, 0.56, 1.0), Color(0.2, 0.22, 0.22), false)
    var label := Label3D.new()
    label.name = "PlaqueText"
    label.text = "%d LEVELS" % floors
    label.position = Vector3(-0.055, 0.0, 0.0)
    label.font_size = 20
    label.pixel_size = 0.01
    label.modulate = Color(0.9, 0.86, 0.72)
    label.rotation.y = -PI * 0.5
    plaque_root.add_child(label)

static func _monument_sign(root: Node3D, node_name: String, position: Vector3, text: String) -> void:
    var sign_root := Node3D.new()
    sign_root.name = node_name
    sign_root.position = position
    root.add_child(sign_root)
    _box(sign_root, "StoneBase", Vector3(0.0, -0.28, 0.0), Vector3(4.6, 0.28, 0.7), LIMESTONE.darkened(0.1), true)
    _box(sign_root, "SignPanel", Vector3(0.0, 0.22, 0.0), Vector3(4.2, 0.75, 0.18), Color(0.18, 0.21, 0.2), false)
    var label := Label3D.new()
    label.name = "MonumentText"
    label.text = text
    label.position = Vector3(0.0, 0.22, 0.12)
    label.font_size = 24
    label.pixel_size = 0.012
    label.modulate = Color(0.9, 0.86, 0.72)
    sign_root.add_child(label)

static func _portico_column_offsets(entry_width: float, column_count: int) -> Array:
    var offsets: Array = []
    var side_count := maxi(int(ceilf(float(column_count) / 2.0)), 1)
    var clear_half := minf(maxf(entry_width * 0.32, 2.45), 3.1)
    var outer_half := maxf(entry_width * 0.66, clear_half + 1.25)
    for side in [-1.0, 1.0]:
        for i in range(side_count):
            var t := 0.0
            if side_count > 1:
                t = float(i) / float(side_count - 1)
            offsets.append(side * lerpf(clear_half, outer_half, t))
    return offsets

static func _entry_reveal(root: Node3D, record_id: String, position: Vector3, front_z: float, entry_width: float) -> void:
    var reveal_color := Color(0.16, 0.18, 0.17)
    var side_x := entry_width * 0.5 + 0.2
    _box(root, "%sEntryRevealLeft" % record_id, position + Vector3(-side_x, 1.55, front_z + 0.1), Vector3(0.22, 2.35, 0.12), reveal_color, false)
    _box(root, "%sEntryRevealRight" % record_id, position + Vector3(side_x, 1.55, front_z + 0.1), Vector3(0.22, 2.35, 0.12), reveal_color, false)
    _box(root, "%sEntryRevealHeader" % record_id, position + Vector3(0.0, 2.75, front_z + 0.1), Vector3(entry_width + 0.62, 0.22, 0.12), reveal_color.lightened(0.08), false)

static func _system_accent(record: Dictionary, fallback: Color) -> Color:
    var systems: Array = _array_value(record, "systems")
    if systems.is_empty():
        return fallback
    match str(systems[0]):
        "housing", "residential":
            return Color(0.64, 0.48, 0.34)
        "food":
            return Color(0.32, 0.58, 0.36)
        "water":
            return Color(0.24, 0.5, 0.64)
        "energy":
            return Color(0.76, 0.61, 0.18)
        "care", "care_health":
            return Color(0.7, 0.31, 0.43)
        "maintenance":
            return Color(0.73, 0.42, 0.24)
        "common_core", "social":
            return Color(0.6, 0.54, 0.44)
        _:
            return fallback

static func _bench(root: Node3D, position: Vector3, rotation_y: float) -> void:
    var bench_root := Node3D.new()
    bench_root.name = "CampusBench"
    bench_root.position = position
    bench_root.rotation.y = rotation_y
    root.add_child(bench_root)
    _box(bench_root, "BenchSeat", Vector3(0.0, 0.38, 0.0), Vector3(3.0, 0.16, 0.55), Color(0.48, 0.31, 0.18), true)
    _box(bench_root, "BenchBack", Vector3(0.0, 0.8, -0.24), Vector3(3.0, 0.18, 0.18), Color(0.42, 0.27, 0.16), true)
    _box(bench_root, "BenchLegA", Vector3(-1.15, 0.2, 0.0), Vector3(0.18, 0.4, 0.42), Color(0.18, 0.18, 0.17), true)
    _box(bench_root, "BenchLegB", Vector3(1.15, 0.2, 0.0), Vector3(0.18, 0.4, 0.42), Color(0.18, 0.18, 0.17), true)

static func _lamp(root: Node3D, position: Vector3) -> void:
    _cylinder(root, "CampusLampPole", position + Vector3(0.0, 1.35, 0.0), 0.07, 2.7, Color(0.12, 0.13, 0.12), false, 12)
    _sphere(root, "CampusLampGlow", position + Vector3(0.0, 2.82, 0.0), 0.28, LAMP, false)

static func _tree(root: Node3D, position: Vector3, scale: float) -> void:
    _cylinder(root, "CampusTreeTrunk", position + Vector3(0.0, 0.8 * scale, 0.0), 0.16 * scale, 1.6 * scale, Color(0.34, 0.22, 0.14), true, 10)
    _sphere(root, "CampusTreeCanopyA", position + Vector3(0.0, 2.0 * scale, 0.0), 1.05 * scale, Color(0.24, 0.42, 0.25), false)
    _sphere(root, "CampusTreeCanopyB", position + Vector3(0.72 * scale, 1.82 * scale, 0.18 * scale), 0.76 * scale, Color(0.28, 0.48, 0.28), false)
    _sphere(root, "CampusTreeCanopyC", position + Vector3(-0.62 * scale, 1.88 * scale, -0.18 * scale), 0.7 * scale, Color(0.22, 0.37, 0.23), false)

static func _box(root: Node3D, node_name: String, position: Vector3, size: Vector3, color: Color, has_collision: bool) -> StaticBody3D:
    var body := StaticBody3D.new()
    body.name = node_name
    body.position = position
    root.add_child(body)

    var mesh_instance := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = size
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _material(color)
    body.add_child(mesh_instance)

    if has_collision:
        var collision := CollisionShape3D.new()
        var shape := BoxShape3D.new()
        shape.size = size
        collision.shape = shape
        body.add_child(collision)

    return body

static func _cylinder(root: Node3D, node_name: String, position: Vector3, radius: float, height: float, color: Color, has_collision: bool, radial_segments: int) -> StaticBody3D:
    var body := StaticBody3D.new()
    body.name = node_name
    body.position = position
    root.add_child(body)

    var mesh_instance := MeshInstance3D.new()
    var mesh := CylinderMesh.new()
    mesh.top_radius = radius
    mesh.bottom_radius = radius
    mesh.height = height
    mesh.radial_segments = radial_segments
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _material(color)
    body.add_child(mesh_instance)

    if has_collision:
        var collision := CollisionShape3D.new()
        var shape := CylinderShape3D.new()
        shape.radius = radius
        shape.height = height
        collision.shape = shape
        body.add_child(collision)

    return body

static func _sphere(root: Node3D, node_name: String, position: Vector3, radius: float, color: Color, has_collision: bool) -> StaticBody3D:
    var body := StaticBody3D.new()
    body.name = node_name
    body.position = position
    root.add_child(body)

    var mesh_instance := MeshInstance3D.new()
    var mesh := SphereMesh.new()
    mesh.radius = radius
    mesh.height = radius * 2.0
    mesh.radial_segments = 14
    mesh.rings = 7
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _material(color)
    body.add_child(mesh_instance)

    if has_collision:
        var collision := CollisionShape3D.new()
        var shape := SphereShape3D.new()
        shape.radius = radius
        collision.shape = shape
        body.add_child(collision)

    return body

static func _label(label_root: Node3D, text: String, position: Vector3, font_size: int, color: Color) -> void:
    pass

static func _material(color: Color) -> StandardMaterial3D:
    var mat := StandardMaterial3D.new()
    mat.albedo_color = color
    mat.roughness = 0.9
    return mat

static func _array_value(source: Dictionary, key: String) -> Array:
    var value: Variant = source.get(key, [])
    if typeof(value) == TYPE_ARRAY:
        return value
    return []
