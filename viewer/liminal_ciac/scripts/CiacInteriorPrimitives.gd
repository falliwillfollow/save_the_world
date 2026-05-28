extends RefCounted
class_name CiacInteriorPrimitives

static func box(root: Node3D, node_name: String, position: Vector3, size: Vector3, color: Color, has_collision: bool = true) -> StaticBody3D:
    var body := StaticBody3D.new()
    body.name = node_name
    body.position = position
    root.add_child(body)

    var mesh_instance := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = size
    mesh_instance.mesh = mesh
    mesh_instance.material_override = material(color)
    body.add_child(mesh_instance)

    if has_collision:
        var collision := CollisionShape3D.new()
        var shape := BoxShape3D.new()
        shape.size = size
        collision.shape = shape
        body.add_child(collision)

    return body

static func fixture_box(root: Node3D, level: Node, interactable_script: Script, node_name: String, position: Vector3, size: Vector3, color: Color, parent_record: Dictionary, label: String, role: String, module_ref: String = "", effects: Array = [], notes: Array = []) -> StaticBody3D:
    var body := box(root, node_name, position, size, color, true)
    body.set_script(interactable_script)
    body.call("setup", level, "fixture", _fixture_record(parent_record, node_name, label, role, module_ref, effects, notes))
    return body

static func cylinder(root: Node3D, node_name: String, position: Vector3, radius: float, height: float, color: Color, has_collision: bool = true, radial_segments: int = 28) -> StaticBody3D:
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
    mesh_instance.material_override = material(color)
    body.add_child(mesh_instance)

    if has_collision:
        var collision := CollisionShape3D.new()
        var shape := CylinderShape3D.new()
        shape.radius = radius
        shape.height = height
        collision.shape = shape
        body.add_child(collision)

    return body

static func fixture_cylinder(root: Node3D, level: Node, interactable_script: Script, node_name: String, position: Vector3, radius: float, height: float, color: Color, parent_record: Dictionary, label: String, role: String, module_ref: String = "", effects: Array = [], notes: Array = [], radial_segments: int = 28) -> StaticBody3D:
    var body := cylinder(root, node_name, position, radius, height, color, true, radial_segments)
    body.set_script(interactable_script)
    body.call("setup", level, "fixture", _fixture_record(parent_record, node_name, label, role, module_ref, effects, notes))
    return body


static func plaque(root: Node3D, level: Node, interactable_script: Script, node_name: String, local_position: Vector3, structure: Dictionary, title_suffix: String) -> StaticBody3D:
    var body := box(root, node_name, local_position, Vector3(0.18, 1.2, 2.2), Color(0.95, 0.9, 0.74), true)
    body.set_script(interactable_script)
    var duplicate_value: Variant = structure.duplicate(true)
    var record: Dictionary = {}
    if typeof(duplicate_value) == TYPE_DICTIONARY:
        record = duplicate_value
    record["label"] = "%s - %s" % [str(structure.get("label", "Structure")), title_suffix]
    body.call("setup", level, "plaque", record)
    return body

static func bulletin(root: Node3D, level: Node, interactable_script: Script, node_name: String, local_position: Vector3, structure: Dictionary, title: String) -> StaticBody3D:
    var body := box(root, node_name, local_position, Vector3(0.2, 1.55, 2.65), Color(0.19, 0.23, 0.24), true)
    body.set_script(interactable_script)
    var duplicate_value: Variant = structure.duplicate(true)
    var record: Dictionary = {}
    if typeof(duplicate_value) == TYPE_DICTIONARY:
        record = duplicate_value
    record["label"] = "%s - %s" % [str(structure.get("label", "Structure")), title]
    record["type"] = "building_bulletin"
    record["fixture_role"] = "Building status, scale, modules, and evidence bulletin"
    record["model_effects"] = [
        "moves structure status and statistics from floating world text into an inspectable in-building surface",
        "keeps the building's capacity, modules, and evidence available at the point of use"
    ]
    record["operating_notes"] = [
        _bulletin_text(structure),
        "Press E on this bulletin for the full inspection tabs."
    ]
    body.call("setup", level, "fixture", record)

    box(body, "BulletinHeader", Vector3(-0.12, 0.55, 0.0), Vector3(0.06, 0.2, 2.2), Color(0.78, 0.72, 0.58), false)
    local_label(body, "BULLETIN\nE TO READ", Vector3(-0.16, 0.02, 0.0), 18, Color(0.96, 0.93, 0.82), Vector3(0.0, -PI * 0.5, 0.0))
    return body

static func label(label_root: Node3D, text: String, position: Vector3, font_size: int = 30) -> void:
    pass

static func local_label(root: Node3D, text: String, position: Vector3, font_size: int = 20, color: Color = Color(0.94, 0.96, 0.94), rotation: Vector3 = Vector3.ZERO) -> Label3D:
    var label_node := Label3D.new()
    label_node.name = "TelemetryLabel"
    label_node.text = text
    label_node.position = position
    label_node.rotation = rotation
    label_node.font_size = font_size
    label_node.pixel_size = 0.018
    label_node.modulate = color
    label_node.billboard = BaseMaterial3D.BILLBOARD_DISABLED
    root.add_child(label_node)
    return label_node

static func material(color: Color) -> StandardMaterial3D:
    var mat := StandardMaterial3D.new()
    mat.albedo_color = color
    mat.roughness = 0.86
    return mat

static func open_shell(root: Node3D, size: Vector3, color: Color, wall_t: float, wall_h: float, door_w: float) -> void:
    box(root, "Floor", Vector3(0.0, 0.05, 0.0), Vector3(size.x, 0.1, size.z), Color(0.58, 0.53, 0.45), true)
    box(root, "BackWall", Vector3(0.0, wall_h * 0.5, -size.z * 0.5), Vector3(size.x, wall_h, wall_t), color, true)
    box(root, "LeftWall", Vector3(-size.x * 0.5, wall_h * 0.5, 0.0), Vector3(wall_t, wall_h, size.z), color, true)
    box(root, "RightWall", Vector3(size.x * 0.5, wall_h * 0.5, 0.0), Vector3(wall_t, wall_h, size.z), color, true)
    box(root, "FrontWallLeft", Vector3(-(size.x + door_w) * 0.25, wall_h * 0.5, size.z * 0.5), Vector3((size.x - door_w) * 0.5, wall_h, wall_t), color, true)
    box(root, "FrontWallRight", Vector3((size.x + door_w) * 0.25, wall_h * 0.5, size.z * 0.5), Vector3((size.x - door_w) * 0.5, wall_h, wall_t), color, true)
    box(root, "HeaderBeam", Vector3(0.0, wall_h + 0.18, size.z * 0.5), Vector3(size.x, 0.36, wall_t), color.lightened(0.12), true)
    box(root, "EntryMat", Vector3(0.0, 0.08, size.z * 0.5 + 1.45), Vector3(maxf(door_w + 1.0, 4.8), 0.08, 2.4), Color(0.32, 0.45, 0.43), true)

static func _fixture_record(parent_record: Dictionary, node_name: String, label: String, role: String, module_ref: String, effects: Array, notes: Array) -> Dictionary:
    var parent_id := str(parent_record.get("id", ""))
    var record := {
        "id": "%s.%s" % [parent_id, node_name],
        "label": label,
        "type": "fixture",
        "fixture_role": role,
        "parent_id": parent_id,
        "parent_label": str(parent_record.get("label", "CIaC element")),
        "evidence_card_id": str(parent_record.get("evidence_card_id", "")),
        "systems": _array_value(parent_record, "systems"),
        "model_effects": effects,
        "operating_notes": notes
    }
    var metrics: Dictionary = _dict_value(parent_record, "metrics")
    if not metrics.is_empty():
        record["metrics"] = metrics
    if module_ref.is_empty():
        record["module_refs"] = _array_value(parent_record, "module_refs")
    else:
        record["module_refs"] = [module_ref]
    return record

static func _array_value(source: Dictionary, key: String) -> Array:
    var value: Variant = source.get(key, [])
    if typeof(value) == TYPE_ARRAY:
        return value
    return []

static func _dict_value(source: Dictionary, key: String) -> Dictionary:
    var value: Variant = source.get(key, {})
    if typeof(value) == TYPE_DICTIONARY:
        return value
    return {}

static func _bulletin_text(structure: Dictionary) -> String:
    var scale: Dictionary = _dict_value(structure, "scale")
    var state: Dictionary = _dict_value(structure, "state")
    var lines: Array = []
    if not scale.is_empty():
        lines.append("scale %s  occ %s/%s" % [
            str(scale.get("status", "review")).to_upper(),
            str(scale.get("occupancy", "?")),
            str(scale.get("modeled_capacity", "?"))
        ])
        if scale.has("floor_count"):
            lines.append("%s levels" % str(scale.get("floor_count", "?")))
    elif not state.is_empty():
        lines.append("status %s" % str(state.get("status", "modeled")).to_upper())
        if state.has("occupancy"):
            lines.append("occupancy %s" % str(state.get("occupancy", "?")))
    else:
        lines.append("modeled civic structure")
    var module_refs: Array = _array_value(structure, "module_refs")
    lines.append("%d linked modules" % module_refs.size())
    return "\n".join(lines)
