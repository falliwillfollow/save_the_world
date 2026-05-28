extends Node3D

signal world_build_progress(progress: float, status: String)
signal world_build_completed

const MANIFEST_PATH := "res://assets/data/civic_floor_80_v0.world.json"
const CIAC_INTERACTABLE_SCRIPT := preload("res://scripts/CiacStructureInteractable.gd")
const CIAC_SPATIAL_SCALE := preload("res://scripts/CiacSpatialScale.gd")
const COMMON_HOUSE_BUILDER := preload("res://scripts/CommonHouseInteriorBuilder.gd")
const RESIDENTIAL_POD_BUILDER := preload("res://scripts/ResidentialPodInteriorBuilder.gd")
const QUIET_STUDIO_BUILDER := preload("res://scripts/QuietStudioInteriorBuilder.gd")
const FOOD_COMMONS_BUILDER := preload("res://scripts/FoodCommonsInteriorBuilder.gd")
const CARE_SOCIAL_BUILDER := preload("res://scripts/CareSocialInteriorBuilder.gd")
const MAINTENANCE_SHOP_BUILDER := preload("res://scripts/MaintenanceShopInteriorBuilder.gd")
const SERVICE_NODE_BUILDER := preload("res://scripts/ServiceNodeBuilder.gd")
const CAMPUS_LIFE_BUILDER := preload("res://scripts/CiacCampusLifeBuilder.gd")
const CAMPUS_AESTHETIC_BUILDER := preload("res://scripts/CiacCampusAestheticBuilder.gd")

@onready var geometry_root: Node3D = $GeometryRoot
@onready var label_root: Node3D = $LabelRoot

var _manifest: Dictionary = {}
var _modules_by_id: Dictionary = {}
var _evidence_by_id: Dictionary = {}
var _resource_telemetry_by_id: Dictionary = {}
var _location_positions: Dictionary = {}
var _inspection_layer: CanvasLayer
var _inspection_panel: PanelContainer
var _inspection_title: Label
var _inspection_overview_body: RichTextLabel
var _inspection_scale_body: RichTextLabel
var _inspection_modules_body: RichTextLabel
var _inspection_evidence_body: RichTextLabel
var _inspection_effects_body: RichTextLabel
var _inspection_actor: Node
var _scale_records: Array = []

func _ready() -> void:
    _emit_progress(0.02, "Loading CIaC manifest")
    _create_inspection_ui()
    call_deferred("_build_world_async")

func _build_world_async() -> void:
    await get_tree().process_frame
    if not _load_manifest():
        _emit_progress(1.0, "CIaC manifest missing")
        world_build_completed.emit()
        return

    _emit_progress(0.1, "Indexing modules and evidence")
    _index_manifest()
    await get_tree().process_frame

    _spawn_ground()
    _spawn_zones()
    _emit_progress(0.25, "Drawing civic zones")
    await get_tree().process_frame

    _spawn_paths()
    _spawn_campus_aesthetic()
    _emit_progress(0.45, "Drawing accessible paths")
    await get_tree().process_frame

    _spawn_structures()
    _emit_progress(0.7, "Placing structures")
    await get_tree().process_frame

    _spawn_infrastructure_nodes()
    _spawn_campus_life()
    _spawn_manifest_summary()
    _emit_progress(1.0, "CIaC district ready")
    world_build_completed.emit()

func get_spawn_data() -> Dictionary:
    return {
        "position": Vector3(0.0, 1.35, 62.0),
        "look_target": Vector3(0.0, 2.0, 8.0)
    }

func show_record_inspection(kind: String, record: Dictionary, actor: Node = null) -> void:
    if _inspection_panel == null:
        return
    _inspection_title.text = str(record.get("label", "CIaC element"))
    _inspection_overview_body.text = _build_inspection_overview_text(kind, record)
    _inspection_scale_body.text = _build_inspection_scale_text(record)
    _inspection_modules_body.text = _build_inspection_modules_text(record)
    _inspection_evidence_body.text = _build_inspection_evidence_text(record)
    _inspection_effects_body.text = _build_inspection_effects_text(record)
    _inspection_panel.visible = true
    _inspection_actor = actor
    if _inspection_actor != null and _inspection_actor.has_method("enter_inspection_focus"):
        _inspection_actor.enter_inspection_focus()

func close_record_inspection() -> void:
    if _inspection_panel == null:
        return
    _inspection_panel.visible = false
    if _inspection_actor != null and _inspection_actor.has_method("exit_inspection_focus"):
        _inspection_actor.exit_inspection_focus()
    _inspection_actor = null

func use_vertical_access(record: Dictionary, actor: Node) -> void:
    if actor == null or not actor.has_method("focus_viewpoint"):
        return
    var target_position := _dict_to_vec3(record.get("target_position", {}))
    var look_target := _dict_to_vec3(record.get("look_target", {}))
    actor.call("focus_viewpoint", target_position, look_target)

func is_inspection_open() -> bool:
    return _inspection_panel != null and _inspection_panel.visible

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("pause_menu") and is_inspection_open():
        close_record_inspection()
        get_viewport().set_input_as_handled()

func _load_manifest() -> bool:
    var manifest_path := str(ProjectSettings.get_setting("ciac/selected_manifest_path", ""))
    if manifest_path.is_empty() or not FileAccess.file_exists(manifest_path):
        manifest_path = MANIFEST_PATH

    if not FileAccess.file_exists(manifest_path):
        push_warning("CIaC manifest not found: %s" % manifest_path)
        return false

    var raw := FileAccess.get_file_as_string(manifest_path)
    var parsed: Variant = JSON.parse_string(raw)
    if typeof(parsed) != TYPE_DICTIONARY:
        push_warning("CIaC manifest is not valid JSON: %s" % manifest_path)
        return false

    _manifest = parsed
    return true

func _index_manifest() -> void:
    _modules_by_id.clear()
    for module in _manifest.get("modules", []):
        if typeof(module) == TYPE_DICTIONARY:
            var module_id := str(module.get("module_id", ""))
            if not module_id.is_empty():
                _modules_by_id[module_id] = module

    _evidence_by_id.clear()
    for evidence in _manifest.get("evidence_cards", []):
        if typeof(evidence) == TYPE_DICTIONARY:
            var evidence_id := str(evidence.get("id", ""))
            if not evidence_id.is_empty():
                _evidence_by_id[evidence_id] = evidence

    _resource_telemetry_by_id.clear()
    var telemetry: Dictionary = _dict_value(_manifest, "resource_telemetry")
    var resources: Array = _array_value(telemetry, "resources")
    for resource in resources:
        if typeof(resource) == TYPE_DICTIONARY:
            var resource_id := str(resource.get("id", ""))
            if not resource_id.is_empty():
                _resource_telemetry_by_id[resource_id] = resource

func _spawn_ground() -> void:
    var bounds := _manifest_world_bounds()
    var center: Vector3 = bounds.get("center", Vector3(0.0, 0.0, 8.0))
    var size: Vector3 = bounds.get("size", Vector3(116.0, 0.5, 132.0))
    _spawn_box("CivicGround", Vector3(center.x, -0.25, center.z), Vector3(size.x, 0.5, size.z), Color(0.28, 0.33, 0.3), true)
    _spawn_box("SpawnPad", Vector3(center.x, 0.06, center.z + size.z * 0.43), Vector3(34.0, 0.12, 26.0), Color(0.34, 0.42, 0.39), true)

func _spawn_zones() -> void:
    for zone in _manifest.get("zones", []):
        if typeof(zone) != TYPE_DICTIONARY:
            continue
        var position := _dict_to_vec3(zone.get("position", {}))
        var size := _dict_to_vec3(zone.get("size", {}))
        size.y = maxf(size.y, 0.035)
        _spawn_box(
            str(zone.get("id", "zone")),
            position,
            size,
            _color_for_token(str(zone.get("color_token", zone.get("type", "zone")))).lightened(0.25),
            false,
            true
        )

func _spawn_paths() -> void:
    var manifest_paths: Array = _array_value(_manifest, "paths")
    if not manifest_paths.is_empty():
        for path in manifest_paths:
            if typeof(path) != TYPE_DICTIONARY:
                continue
            var points := []
            for point in _array_value(path, "points"):
                points.append(_dict_to_vec3(point))
            if points.size() >= 2:
                _spawn_path_polyline(str(path.get("id", "path")), points, str(path.get("type", "primary_access")))
        return
    _spawn_path_polyline("campus_quad_loop", [
        Vector3(-32.0, 0.0, 28.0),
        Vector3(32.0, 0.0, 28.0),
        Vector3(32.0, 0.0, -28.0),
        Vector3(-32.0, 0.0, -28.0),
        Vector3(-32.0, 0.0, 28.0),
    ], "primary_access")

func _spawn_campus_aesthetic() -> void:
    CAMPUS_AESTHETIC_BUILDER.build_site(geometry_root, label_root)

func _spawn_structures() -> void:
    _location_positions.clear()
    _scale_records.clear()
    for structure in _manifest.get("structures", []):
        if typeof(structure) != TYPE_DICTIONARY:
            continue
        var structure_record: Dictionary = _duplicate_dict(structure)
        var position := _scaled_structure_position(structure_record, _dict_to_vec3(structure_record.get("position", {})))
        var structure_id := str(structure_record.get("id", ""))
        if not structure_id.is_empty():
            _location_positions[structure_id] = position
        var size := CIAC_SPATIAL_SCALE.structure_size(structure_record, _dict_to_vec3(structure_record.get("size", {})))
        var scale_record: Dictionary = CIAC_SPATIAL_SCALE.scale_record(structure_record)
        structure_record["scale"] = scale_record
        _scale_records.append(scale_record)
        _spawn_scale_marker(position, size, scale_record)
        var systems: Array = _array_value(structure_record, "systems")
        var color := _color_for_systems(systems)
        var structure_type := str(structure_record.get("type", ""))
        CAMPUS_AESTHETIC_BUILDER.decorate_structure(geometry_root, label_root, structure_record, position, size, color)
        _spawn_vertical_access_points(structure_record, position, size, scale_record)
        if structure_type == "common_house":
            COMMON_HOUSE_BUILDER.build(self, geometry_root, label_root, structure_record, position, size, color, CIAC_INTERACTABLE_SCRIPT)
            continue
        if structure_type == "residential_pod":
            RESIDENTIAL_POD_BUILDER.build(self, geometry_root, label_root, structure_record, position, size, color, CIAC_INTERACTABLE_SCRIPT)
            continue
        if structure_type == "quiet_studio":
            QUIET_STUDIO_BUILDER.build(self, geometry_root, label_root, structure_record, position, size, color, CIAC_INTERACTABLE_SCRIPT)
            continue
        if structure_type == "food_commons" or structure_type == "protein_commons":
            FOOD_COMMONS_BUILDER.build(self, geometry_root, label_root, structure_record, position, size, color, CIAC_INTERACTABLE_SCRIPT)
            continue
        if structure_type == "care_room" or structure_type == "social_cultural":
            CARE_SOCIAL_BUILDER.build(self, geometry_root, label_root, structure_record, position, size, color, CIAC_INTERACTABLE_SCRIPT)
            continue
        if structure_type == "maintenance_shop":
            MAINTENANCE_SHOP_BUILDER.build(self, geometry_root, label_root, structure_record, position, size, color, CIAC_INTERACTABLE_SCRIPT)
            continue
        var body := _spawn_box(
            str(structure_record.get("id", "structure")),
            position + Vector3(0.0, size.y * 0.5, 0.0),
            size,
            color,
            true,
            false,
            "structure",
            structure_record
        )
        _add_roof_accent(body, size, color.lightened(0.3))
        _spawn_entry_marker(position, size, color.lightened(0.18))
        _spawn_label(str(structure_record.get("label", "Structure")), position + Vector3(0.0, size.y + 0.45, 0.0))

func _spawn_infrastructure_nodes() -> void:
    for node in _manifest.get("infrastructure_nodes", []):
        if typeof(node) != TYPE_DICTIONARY:
            continue
        var node_record: Dictionary = _duplicate_dict(node)
        var position := _campus_node_position(node_record, _dict_to_vec3(node_record.get("position", {})))
        var node_type := str(node_record.get("type", "node"))
        _bind_resource_telemetry(node_record, node_type)
        var color := _color_for_token(node_type)
        var node_id := str(node_record.get("id", ""))
        if not node_id.is_empty():
            _location_positions[node_id] = position
        SERVICE_NODE_BUILDER.build(self, geometry_root, label_root, node_record, position, color, CIAC_INTERACTABLE_SCRIPT)

func _spawn_campus_life() -> void:
    CAMPUS_LIFE_BUILDER.build(self, geometry_root, label_root, _manifest, _location_positions, CIAC_INTERACTABLE_SCRIPT)

func _spawn_manifest_summary() -> void:
    var population: Dictionary = _dict_value(_manifest, "population")
    var residents := str(population.get("residents", "unknown"))
    _spawn_welcome_board(residents)
    _spawn_scale_summary_board()

func _spawn_box(
    node_name: String,
    position: Vector3,
    size: Vector3,
    color: Color,
    has_collision: bool,
    transparent: bool = false,
    kind: String = "",
    record: Dictionary = {}
) -> StaticBody3D:
    var body := StaticBody3D.new()
    body.name = node_name
    body.position = position
    geometry_root.add_child(body)

    var mesh_instance := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = size
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _make_material(color, transparent)
    body.add_child(mesh_instance)

    if has_collision:
        var collision := CollisionShape3D.new()
        var shape := BoxShape3D.new()
        shape.size = size
        collision.shape = shape
        body.add_child(collision)

    if not kind.is_empty():
        body.set_script(CIAC_INTERACTABLE_SCRIPT)
        body.call("setup", self, kind, record)

    return body

func _spawn_cylinder_node(record: Dictionary, position: Vector3, radius: float, height: float, color: Color) -> void:
    var body := StaticBody3D.new()
    body.name = str(record.get("id", "node"))
    body.position = position + Vector3(0.0, height * 0.5, 0.0)
    body.set_script(CIAC_INTERACTABLE_SCRIPT)
    body.call("setup", self, "node", record)
    geometry_root.add_child(body)

    var mesh_instance := MeshInstance3D.new()
    var mesh := CylinderMesh.new()
    mesh.top_radius = radius
    mesh.bottom_radius = radius
    mesh.height = height
    mesh.radial_segments = 28
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _make_material(color, false)
    body.add_child(mesh_instance)

    var collision := CollisionShape3D.new()
    var shape := CylinderShape3D.new()
    shape.radius = radius
    shape.height = height
    collision.shape = shape
    body.add_child(collision)

func _spawn_path_segment(path_id: String, a: Vector3, b: Vector3, path_type: String) -> void:
    var delta := b - a
    var length := Vector2(delta.x, delta.z).length()
    if length <= 0.05:
        return
    var mid := (a + b) * 0.5 + Vector3(0.0, 0.02, 0.0)
    var width := 1.8 if path_type == "primary_access" else 1.15
    var body := _spawn_box("%s_segment" % path_id, mid, Vector3(width, 0.05, length), Color(0.78, 0.74, 0.62), false, false)
    body.rotation.y = atan2(delta.x, delta.z)

func _spawn_path_polyline(path_id: String, points: Array, path_type: String) -> void:
    for i in range(maxi(points.size() - 1, 0)):
        _spawn_path_segment(path_id, points[i], points[i + 1], path_type)

func _spawn_label(text: String, position: Vector3) -> void:
    pass

func _add_roof_accent(body: StaticBody3D, size: Vector3, color: Color) -> void:
    var mesh_instance := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = Vector3(size.x + 0.35, 0.18, size.z + 0.35)
    mesh_instance.position = Vector3(0.0, size.y * 0.5 + 0.12, 0.0)
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _make_material(color, false)
    body.add_child(mesh_instance)

func _spawn_entry_marker(position: Vector3, size: Vector3, color: Color) -> void:
    _spawn_box(
        "EntryMarker",
        position + Vector3(0.0, 0.055, size.z * 0.5 + 1.1),
        Vector3(minf(size.x * 0.42, 4.8), 0.1, 2.0),
        color,
        true
    )

func _spawn_vertical_access_points(structure: Dictionary, position: Vector3, size: Vector3, scale_record: Dictionary) -> void:
    var floors := int(scale_record.get("floor_count", 1))
    if floors <= 1:
        return
    var record_id := str(structure.get("id", "structure"))
    var tower_x := size.x * 0.5 - 2.1
    var front_z := size.z * 0.5 + 2.13
    var ground_position := position + Vector3(tower_x - 0.56, 1.18, front_z + 0.06)
    var upper_floor_y := 0.55 + 3.15
    var upper_position := position + Vector3(tower_x - 0.56, upper_floor_y + 0.78, front_z + 0.06)
    var upper_player_position := position + Vector3(tower_x, upper_floor_y + 1.35, front_z - 1.25)
    var ground_player_position := position + Vector3(tower_x, 1.35, front_z + 1.45)
    _spawn_lift_call_point(
        "%sLiftCallGround" % record_id,
        ground_position,
        "Lift to level 2",
        structure,
        upper_player_position,
        upper_player_position + Vector3(0.0, 0.4, 4.0)
    )
    _spawn_lift_call_point(
        "%sLiftCallLevel2" % record_id,
        upper_position,
        "Lift to ground",
        structure,
        ground_player_position,
        ground_player_position + Vector3(0.0, 0.4, -4.0)
    )

func _spawn_lift_call_point(node_name: String, position: Vector3, label: String, structure: Dictionary, target_position: Vector3, look_target: Vector3) -> void:
    var record := {
        "id": "%s.%s" % [str(structure.get("id", "structure")), node_name],
        "label": label,
        "type": "vertical_access",
        "parent_id": str(structure.get("id", "")),
        "parent_label": str(structure.get("label", "Structure")),
        "target_position": _vec3_to_dict(target_position),
        "look_target": _vec3_to_dict(look_target),
        "operating_notes": [
            "Functional lift call point for moving between the ground level and second-level landing.",
            "Represents accessible vertical circulation in the walkthrough, not a certified elevator design."
        ],
        "model_effects": [
            "Makes upper-level structure capacity physically reachable during inspection."
        ],
        "module_refs": _array_value(structure, "module_refs"),
        "evidence_card_id": str(structure.get("evidence_card_id", ""))
    }
    var body := _spawn_box(node_name, position, Vector3(0.82, 1.22, 0.16), Color(0.18, 0.22, 0.22), true, false, "vertical_access", record)
    var label_node := Label3D.new()
    label_node.name = "LiftCallLabel"
    label_node.text = "LIFT\nE"
    label_node.position = Vector3(0.0, 0.03, -0.09)
    label_node.font_size = 20
    label_node.pixel_size = 0.011
    label_node.modulate = Color(0.9, 0.86, 0.72)
    body.add_child(label_node)

func _spawn_scale_marker(position: Vector3, size: Vector3, scale_record: Dictionary) -> void:
    var status := str(scale_record.get("status", "review"))
    var occupancy := int(scale_record.get("occupancy", 0))
    var capacity := int(scale_record.get("modeled_capacity", 0))
    var marker_color := _scale_status_color(status)
    _spawn_box(
        "ScaleStatus_%s" % str(scale_record.get("structure_id", "structure")),
        position + Vector3(0.0, size.y + 0.18, -size.z * 0.5 - 0.32),
        Vector3(minf(size.x, 9.0), 0.16, 0.48),
        marker_color,
        false
    )

func _spawn_welcome_board(residents: String) -> void:
    var board := StaticBody3D.new()
    board.name = "CiacWelcomeBoard"
    board.position = Vector3(-38.0, 1.55, 34.0)
    geometry_root.add_child(board)

    var mesh_instance := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = Vector3(8.2, 2.4, 0.36)
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _make_material(Color(0.16, 0.19, 0.18), false)
    board.add_child(mesh_instance)

    var collision := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = mesh.size
    collision.shape = shape
    board.add_child(collision)

    var label := Label3D.new()
    label.name = "WelcomeBoardText"
    label.text = "CIaC Civic Floor\n%s residents\nPress E on doors, bulletins, fixtures, and residents" % residents
    label.position = Vector3(0.0, 0.0, -0.24)
    label.font_size = 28
    label.pixel_size = 0.017
    label.modulate = Color(0.9, 0.94, 0.9)
    board.add_child(label)

func _spawn_scale_summary_board() -> void:
    var board := StaticBody3D.new()
    board.name = "ScaleCapacityBoard"
    board.position = Vector3(38.0, 1.65, 35.0)
    board.set_script(CIAC_INTERACTABLE_SCRIPT)
    board.call("setup", self, "system", {
        "id": "scale_capacity_board",
        "label": "Campus Scale and Capacity Board",
        "type": "scale_capacity",
        "scale": _scale_summary_record(),
        "model_effects": [
            "Shows whether structures should grow in place, duplicate, or stop population scaling.",
            "Uses researched human-scale thresholds as review gates rather than blindly replicating buildings."
        ],
        "operating_notes": [
            "Green means the current node is within modeled capacity.",
            "Warning means this node is approaching its soft threshold.",
            "Fail means the world should redesign, expand, or duplicate before promotion."
        ]
    })
    geometry_root.add_child(board)

    var mesh_instance := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = Vector3(12.0, 3.4, 0.4)
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _make_material(Color(0.16, 0.19, 0.2), false)
    board.add_child(mesh_instance)

    var collision := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = mesh.size
    collision.shape = shape
    board.add_child(collision)

    var label := Label3D.new()
    label.name = "ScaleCapacityBoardText"
    label.text = "Scale Capacity\n%s\n%s" % [_scale_summary_text(), _next_scale_attention()]
    label.position = Vector3(0.0, 0.05, -0.26)
    label.font_size = 34
    label.pixel_size = 0.022
    label.modulate = Color(0.92, 0.96, 0.92)
    board.add_child(label)

func _create_inspection_ui() -> void:
    _inspection_layer = CanvasLayer.new()
    _inspection_layer.name = "CiacInspectionLayer"
    add_child(_inspection_layer)

    _inspection_panel = PanelContainer.new()
    _inspection_panel.name = "InspectionPanel"
    _inspection_panel.position = Vector2(24.0, 92.0)
    _inspection_panel.custom_minimum_size = Vector2(620.0, 620.0)
    _inspection_panel.visible = false
    _inspection_layer.add_child(_inspection_panel)

    var margin := MarginContainer.new()
    margin.add_theme_constant_override("margin_left", 16)
    margin.add_theme_constant_override("margin_right", 16)
    margin.add_theme_constant_override("margin_top", 14)
    margin.add_theme_constant_override("margin_bottom", 14)
    _inspection_panel.add_child(margin)

    var stack := VBoxContainer.new()
    stack.add_theme_constant_override("separation", 10)
    margin.add_child(stack)

    var header := HBoxContainer.new()
    header.add_theme_constant_override("separation", 10)
    stack.add_child(header)

    _inspection_title = Label.new()
    _inspection_title.text = "CIaC Element"
    _inspection_title.add_theme_font_size_override("font_size", 22)
    _inspection_title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    header.add_child(_inspection_title)

    var close_button := Button.new()
    close_button.text = "Close"
    close_button.custom_minimum_size = Vector2(92.0, 34.0)
    close_button.pressed.connect(close_record_inspection)
    header.add_child(close_button)

    var tabs := TabContainer.new()
    tabs.custom_minimum_size = Vector2(580.0, 480.0)
    tabs.size_flags_vertical = Control.SIZE_EXPAND_FILL
    stack.add_child(tabs)

    _inspection_overview_body = _create_inspection_tab(tabs, "Overview")
    _inspection_scale_body = _create_inspection_tab(tabs, "Scale")
    _inspection_modules_body = _create_inspection_tab(tabs, "Modules")
    _inspection_evidence_body = _create_inspection_tab(tabs, "Evidence")
    _inspection_effects_body = _create_inspection_tab(tabs, "Effects")

    var hint := Label.new()
    hint.text = "Mouse wheel scrolls the active tab. Esc or Close returns to walk mode."
    hint.modulate = Color(0.74, 0.78, 0.82)
    stack.add_child(hint)

func _create_inspection_tab(tabs: TabContainer, tab_name: String) -> RichTextLabel:
    var body := RichTextLabel.new()
    body.name = tab_name
    body.custom_minimum_size = Vector2(560.0, 430.0)
    body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    body.size_flags_vertical = Control.SIZE_EXPAND_FILL
    body.fit_content = false
    body.bbcode_enabled = false
    body.scroll_active = true
    body.selection_enabled = true
    tabs.add_child(body)
    return body

func _build_inspection_overview_text(kind: String, record: Dictionary) -> String:
    var lines = []
    lines.append("%s: %s" % [kind.capitalize(), str(record.get("id", ""))])
    if record.has("type"):
        lines.append("Type: %s" % str(record.get("type", "")))
    if record.has("parent_label"):
        lines.append("Part of: %s" % str(record.get("parent_label", "")))
    if record.has("fixture_role"):
        lines.append("Role: %s" % str(record.get("fixture_role", "")))
    if record.has("archetype"):
        lines.append("Archetype: %s" % str(record.get("archetype", "")))
    if record.has("current_routine"):
        lines.append("Routine: %s" % str(record.get("current_routine", "")))
    if record.has("time"):
        lines.append("Time: %s for %s minutes" % [str(record.get("time", "")), str(record.get("duration_minutes", ""))])
    if record.has("home_structure_id"):
        lines.append("Home: %s" % str(record.get("home_structure_id", "")))
    if record.has("location_id"):
        lines.append("Destination: %s" % str(record.get("location_id", "")))
    if record.has("privacy"):
        lines.append("Privacy: %s" % str(record.get("privacy", "")))
    if record.has("systems"):
        lines.append("Systems: %s" % _join_values(record.get("systems", []), 8))
    if record.has("scale"):
        var scale: Dictionary = _dict_value(record, "scale")
        lines.append("Scale status: %s (%s/%s)" % [
            str(scale.get("status", "review")),
            str(scale.get("occupancy", "?")),
            str(scale.get("modeled_capacity", "?"))
        ])
    if record.has("state"):
        var state: Dictionary = _dict_value(record, "state")
        if state.has("status"):
            lines.append("Status: %s" % str(state.get("status", "")))
        if state.has("occupancy"):
            lines.append("Occupancy: %s" % str(state.get("occupancy", "")))
    if record.has("metrics"):
        lines.append("")
        lines.append("Metrics:")
        var metrics: Dictionary = _dict_value(record, "metrics")
        for key in metrics.keys():
            if key == "fields":
                continue
            lines.append("- %s: %s" % [str(key).replace("_", " "), str(metrics[key])])
        var fields: Dictionary = _dict_value(metrics, "fields")
        if not fields.is_empty():
            lines.append("")
            lines.append("Capability fields:")
            for key in fields.keys():
                lines.append("- %s: %s" % [str(key).replace("_", " "), str(fields[key])])
    return _join_strings(lines, "\n")

func _build_inspection_scale_text(record: Dictionary) -> String:
    var scale: Dictionary = _dict_value(record, "scale")
    if scale.is_empty():
        return "No scale or capacity annotation is attached to this element."

    if scale.has("pass_count") or scale.has("warn_count") or scale.has("fail_count"):
        var summary_lines = []
        summary_lines.append("Campus scale status: %s" % str(scale.get("status", "review")).to_upper())
        summary_lines.append("Pass: %s" % str(scale.get("pass_count", 0)))
        summary_lines.append("Warn: %s" % str(scale.get("warn_count", 0)))
        summary_lines.append("Fail: %s" % str(scale.get("fail_count", 0)))
        summary_lines.append("")
        summary_lines.append("Recommendation:")
        summary_lines.append("- %s" % str(scale.get("recommendation", "Review before promotion.")))
        var attention: Array = _array_value(scale, "attention")
        if not attention.is_empty():
            summary_lines.append("")
            summary_lines.append("Structures needing attention:")
            for item in attention.slice(0, mini(attention.size(), 8)):
                summary_lines.append("- %s" % str(item))
        summary_lines.append("")
        summary_lines.append("Research basis:")
        summary_lines.append("- %s" % str(scale.get("research_basis", "No basis attached.")))
        return _join_strings(summary_lines, "\n")

    var utilization := float(scale.get("utilization", 0.0)) * 100.0
    var lines = []
    lines.append("Status: %s" % str(scale.get("status", "review")).to_upper())
    lines.append("Occupancy: %s" % str(scale.get("occupancy", "?")))
    lines.append("Modeled capacity: %s" % str(scale.get("modeled_capacity", "?")))
    lines.append("Soft threshold: %s" % str(scale.get("soft_threshold", "?")))
    lines.append("Hard threshold: %s" % str(scale.get("hard_threshold", "?")))
    lines.append("Utilization: %.0f%%" % utilization)
    if scale.has("floor_count"):
        lines.append("Floors: %s" % str(scale.get("floor_count", 1)))
    if scale.has("vertical_program"):
        lines.append("Vertical program: %s" % str(scale.get("vertical_program", "")))
    lines.append("")
    lines.append("Scaling strategy:")
    lines.append("- %s" % str(scale.get("strategy", "review")))
    lines.append("")
    lines.append("Recommendation:")
    lines.append("- %s" % str(scale.get("recommendation", "Review before promotion.")))
    lines.append("")
    lines.append("Research basis:")
    lines.append("- %s" % str(scale.get("research_basis", "No basis attached.")))
    return _join_strings(lines, "\n")

func _build_inspection_effects_text(record: Dictionary) -> String:
    var lines = []
    var model_effects: Array = _array_value(record, "model_effects")
    if not model_effects.is_empty():
        lines.append("Model effects:")
        for effect in model_effects.slice(0, mini(model_effects.size(), 8)):
            lines.append("- %s" % str(effect))
    else:
        lines.append("No object-specific model effects are declared.")

    var operating_notes: Array = _array_value(record, "operating_notes")
    if not operating_notes.is_empty():
        lines.append("")
        lines.append("Operating notes:")
        for note in operating_notes.slice(0, mini(operating_notes.size(), 8)):
            lines.append("- %s" % str(note))
    return _join_strings(lines, "\n")

func _build_inspection_modules_text(record: Dictionary) -> String:
    var lines = []
    var module_refs: Array = _array_value(record, "module_refs")
    lines.append("Linked modules:")
    if module_refs.is_empty():
        lines.append("- None attached in this manifest.")
    else:
        for module_ref in module_refs:
            var module_id := str(module_ref)
            var module: Dictionary = _dict_value(_modules_by_id, module_id)
            if module.is_empty():
                lines.append("- %s" % module_id)
            else:
                lines.append("- %s [%s]" % [str(module.get("label", module_id)), str(module.get("status", "unknown"))])
                var summary := str(module.get("summary", ""))
                if not summary.is_empty():
                    lines.append("  %s" % summary)
                if module.has("placement_target_id"):
                    lines.append("  target: %s" % str(module.get("placement_target_id", "")))
    return _join_strings(lines, "\n")

func _build_inspection_evidence_text(record: Dictionary) -> String:
    var lines = []
    var evidence_id := str(record.get("evidence_card_id", ""))
    var evidence: Dictionary = _dict_value(_evidence_by_id, evidence_id)
    if not evidence.is_empty():
        lines.append("Evidence: %s" % evidence_id)
        lines.append("- %s" % str(evidence.get("summary", evidence.get("title", evidence_id))))
        var reviews: Array = _array_value(evidence, "review_required")
        if not reviews.is_empty():
            lines.append("- Review: %s" % _join_values(reviews, 8))
        var assumptions: Array = _array_value(evidence, "assumptions")
        if not assumptions.is_empty():
            lines.append("- Assumption: %s" % str(assumptions[0]))

        var sources: Array = _array_value(evidence, "sources")
        if not sources.is_empty():
            lines.append("")
            lines.append("Sources:")
            for source in sources.slice(0, mini(sources.size(), 6)):
                if typeof(source) != TYPE_DICTIONARY:
                    continue
                lines.append("- %s (%s)" % [str(source.get("title", source.get("id", "source"))), str(source.get("organization", "source"))])
            if sources.size() > 6:
                lines.append("- +%d more in the manifest evidence card." % (sources.size() - 6))
    else:
        lines.append("No evidence card is attached to this record.")
    return _join_strings(lines, "\n")

func _dict_to_vec3(value) -> Vector3:
    if typeof(value) != TYPE_DICTIONARY:
        return Vector3.ZERO
    return Vector3(
        float(value.get("x", 0.0)),
        float(value.get("y", 0.0)),
        float(value.get("z", 0.0))
    )

func _vec3_to_dict(value: Vector3) -> Dictionary:
    return {
        "x": value.x,
        "y": value.y,
        "z": value.z
    }

func _manifest_world_bounds() -> Dictionary:
    var points := []
    for zone in _manifest.get("zones", []):
        if typeof(zone) != TYPE_DICTIONARY:
            continue
        var zone_position := _dict_to_vec3(zone.get("position", {}))
        var zone_size := _dict_to_vec3(zone.get("size", {}))
        points.append(zone_position + Vector3(-zone_size.x * 0.5, 0.0, -zone_size.z * 0.5))
        points.append(zone_position + Vector3(zone_size.x * 0.5, 0.0, zone_size.z * 0.5))
    for structure in _manifest.get("structures", []):
        if typeof(structure) == TYPE_DICTIONARY:
            points.append(_dict_to_vec3(structure.get("position", {})))
    for node in _manifest.get("infrastructure_nodes", []):
        if typeof(node) == TYPE_DICTIONARY:
            points.append(_dict_to_vec3(node.get("position", {})))
    for path in _manifest.get("paths", []):
        if typeof(path) != TYPE_DICTIONARY:
            continue
        for point in _array_value(path, "points"):
            points.append(_dict_to_vec3(point))
    if points.is_empty():
        return {
            "center": Vector3(0.0, 0.0, 8.0),
            "size": Vector3(116.0, 0.5, 132.0)
        }
    var min_x := INF
    var max_x := -INF
    var min_z := INF
    var max_z := -INF
    for point in points:
        min_x = minf(min_x, point.x)
        max_x = maxf(max_x, point.x)
        min_z = minf(min_z, point.z)
        max_z = maxf(max_z, point.z)
    var width := maxf(150.0, max_x - min_x + 96.0)
    var depth := maxf(150.0, max_z - min_z + 96.0)
    return {
        "center": Vector3((min_x + max_x) * 0.5, 0.0, (min_z + max_z) * 0.5),
        "size": Vector3(width, 0.5, depth)
    }

func _scaled_structure_position(record: Dictionary, base: Vector3) -> Vector3:
    var display: Dictionary = _dict_value(record, "display")
    if bool(display.get("position_authoritative", false)):
        return base
    var structure_type := str(record.get("type", ""))
    var record_id := str(record.get("id", ""))
    match record_id:
        "structure_common_house":
            return Vector3(0.0, 0.0, 8.0)
        "structure_food_commons":
            return Vector3(-24.0, 0.0, 38.0)
        "structure_protein_commons":
            return Vector3(24.0, 0.0, 38.0)
        "structure_care_room":
            return Vector3(-32.0, 0.0, 4.0)
        "structure_social_cultural":
            return Vector3(32.0, 0.0, 4.0)
        "structure_maintenance_shop":
            return Vector3(24.0, 0.0, -44.0)
        "structure_quiet_studio":
            return Vector3(-24.0, 0.0, -42.0)
        "structure_residential_pod_1":
            return Vector3(-48.0, 0.0, 24.0)
        "structure_residential_pod_2":
            return Vector3(48.0, 0.0, 24.0)
        "structure_residential_pod_3":
            return Vector3(-48.0, 0.0, -24.0)
        "structure_residential_pod_4":
            return Vector3(48.0, 0.0, -24.0)
    match structure_type:
        "care_room":
            return base + Vector3(-10.0, 0.0, 0.0)
        "social_cultural":
            return base + Vector3(10.0, 0.0, 0.0)
        "food_commons":
            return base + Vector3(0.0, 0.0, 9.0)
        "protein_commons":
            return base + Vector3(10.0, 0.0, 8.0)
        "maintenance_shop":
            return base + Vector3(10.0, 0.0, -9.0)
        "quiet_studio":
            return base + Vector3(-9.0, 0.0, -9.0)
        "residential_pod":
            var sign_x := 1.0
            if base.x < 0.0:
                sign_x = -1.0
            var sign_z := 1.0
            if base.z < 0.0:
                sign_z = -1.0
            return base + Vector3(sign_x * 8.0, 0.0, sign_z * 6.0)
        _:
            return base

func _campus_node_position(record: Dictionary, base: Vector3) -> Vector3:
    var display: Dictionary = _dict_value(record, "display")
    if bool(display.get("position_authoritative", false)):
        return base
    var node_type := str(record.get("type", ""))
    match node_type:
        "water":
            return Vector3(-48.0, 0.0, -44.0)
        "energy":
            return Vector3(0.0, 0.0, -52.0)
        "sanitation":
            return Vector3(48.0, 0.0, -42.0)
        "risk":
            return Vector3(0.0, 0.0, -18.0)
        _:
            return base

func _dict_value(source: Dictionary, key: String) -> Dictionary:
    var value: Variant = source.get(key, {})
    if typeof(value) == TYPE_DICTIONARY:
        return value
    return {}

func _duplicate_dict(source: Dictionary) -> Dictionary:
    var duplicate_value: Variant = source.duplicate(true)
    if typeof(duplicate_value) == TYPE_DICTIONARY:
        return duplicate_value
    return {}

func _bind_resource_telemetry(record: Dictionary, resource_id: String) -> void:
    var telemetry: Dictionary = _dict_value(_resource_telemetry_by_id, resource_id)
    if telemetry.is_empty():
        return
    var metrics: Dictionary = _duplicate_dict(telemetry)
    var existing_metrics: Dictionary = _dict_value(record, "metrics")
    for key in existing_metrics.keys():
        metrics[key] = existing_metrics[key]
    record["metrics"] = metrics

func _array_value(source: Dictionary, key: String) -> Array:
    var value: Variant = source.get(key, [])
    if typeof(value) == TYPE_ARRAY:
        return value
    return []

func _make_material(color: Color, transparent: bool) -> StandardMaterial3D:
    var mat := StandardMaterial3D.new()
    mat.albedo_color = color
    mat.roughness = 0.88
    if transparent:
        mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
        mat.albedo_color.a = 0.38
    return mat

func _color_for_systems(systems) -> Color:
    if systems.is_empty():
        return Color(0.74, 0.72, 0.66)
    return _color_for_token(str(systems[0]))

func _scale_status_color(status: String) -> Color:
    match status:
        "pass":
            return Color(0.23, 0.67, 0.38)
        "warn":
            return Color(0.9, 0.68, 0.22)
        "fail":
            return Color(0.78, 0.22, 0.18)
        _:
            return Color(0.58, 0.6, 0.62)

func _scale_summary_text() -> String:
    if _scale_records.is_empty():
        return "scale: no structure capacity records"
    return "scale: %d pass | %d warn | %d fail" % [
        _status_count("pass"),
        _status_count("warn"),
        _status_count("fail")
    ]

func _scale_summary_record() -> Dictionary:
    var attention: Array = []
    for scale_value in _scale_records:
        if typeof(scale_value) != TYPE_DICTIONARY:
            continue
        var scale: Dictionary = scale_value
        if str(scale.get("status", "pass")) != "pass":
            attention.append("%s: %s" % [str(scale.get("label", "Structure")), str(scale.get("recommendation", ""))])
    return {
        "status": "pass" if _status_count("fail") == 0 and _status_count("warn") == 0 else "warn",
        "pass_count": _status_count("pass"),
        "warn_count": _status_count("warn"),
        "fail_count": _status_count("fail"),
        "attention": attention,
        "recommendation": _next_scale_attention(),
        "research_basis": "Campus-scale overlay joins the scaling research threshold reports to each walkable structure."
    }

func _status_count(status: String) -> int:
    var count := 0
    for scale_value in _scale_records:
        if typeof(scale_value) == TYPE_DICTIONARY:
            var scale: Dictionary = scale_value
            if str(scale.get("status", "")) == status:
                count += 1
    return count

func _next_scale_attention() -> String:
    for target_status in ["fail", "warn"]:
        for scale_value in _scale_records:
            if typeof(scale_value) != TYPE_DICTIONARY:
                continue
            var scale: Dictionary = scale_value
            if str(scale.get("status", "")) == target_status:
                return "next: %s - %s" % [str(scale.get("label", "Structure")), str(scale.get("strategy", "review"))]
    return "next: all current nodes are within modeled capacity"

func _color_for_token(token: String) -> Color:
    match token:
        "housing", "residential":
            return Color(0.72, 0.64, 0.54)
        "food":
            return Color(0.35, 0.62, 0.38)
        "water":
            return Color(0.24, 0.55, 0.74)
        "energy":
            return Color(0.82, 0.66, 0.22)
        "sanitation", "service_edge":
            return Color(0.48, 0.48, 0.5)
        "maintenance":
            return Color(0.82, 0.47, 0.24)
        "care", "care_health":
            return Color(0.76, 0.34, 0.48)
        "governance", "risk", "risk_resilience":
            return Color(0.45, 0.36, 0.64)
        "labor_time", "dignity_privacy":
            return Color(0.34, 0.62, 0.62)
        "mobility":
            return Color(0.66, 0.72, 0.58)
        "common_core", "social":
            return Color(0.76, 0.72, 0.64)
        _:
            return Color(0.65, 0.65, 0.61)

func _join_values(values, limit: int) -> String:
    if typeof(values) != TYPE_ARRAY:
        return str(values)
    var parts = []
    var count := mini(values.size(), limit)
    for i in range(count):
        parts.append(str(values[i]))
    if values.size() > limit:
        parts.append("+%d more" % (values.size() - limit))
    return _join_strings(parts, ", ")

func _join_strings(values, separator: String) -> String:
    var result := ""
    for i in range(values.size()):
        if i > 0:
            result += separator
        result += str(values[i])
    return result

func _emit_progress(progress: float, status: String) -> void:
    world_build_progress.emit(clampf(progress, 0.0, 1.0), status)
