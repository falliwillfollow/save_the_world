extends Node3D
class_name CiacResidentAvatar

var _hip: Node3D
var _torso: Node3D
var _head: Node3D
var _left_arm_pivot: Node3D
var _right_arm_pivot: Node3D
var _left_forearm_pivot: Node3D
var _right_forearm_pivot: Node3D
var _left_leg_pivot: Node3D
var _right_leg_pivot: Node3D
var _walk_phase := 0.0
var _gesture_phase := 0.0
var _locomotion := 0.0
var _idle_blend := 0.0

func setup(level: Node, interactable_script: Script, record: Dictionary, accent_color: Color, seed: int) -> void:
    if _hip != null:
        return
    var palette := _palette(seed, accent_color)
    _build_rig(level, interactable_script, record, palette)

func apply_motion(locomotion: float, idle_blend: float, delta: float) -> void:
    _locomotion = lerpf(_locomotion, clampf(locomotion, 0.0, 1.0), clampf(delta * 9.0, 0.0, 1.0))
    _idle_blend = lerpf(_idle_blend, clampf(idle_blend, 0.0, 1.0), clampf(delta * 4.5, 0.0, 1.0))
    _walk_phase += delta * lerpf(0.9, 2.25, _locomotion)
    _gesture_phase += delta * 0.55

    var walk_sin := sin(_walk_phase * TAU)
    var leg_swing := deg_to_rad(walk_sin * 22.0 * _locomotion)
    var arm_swing := deg_to_rad(-walk_sin * 17.0 * _locomotion)
    var idle_wave := sin(_gesture_phase * TAU) * _idle_blend

    if _left_leg_pivot != null:
        _left_leg_pivot.rotation.x = leg_swing
    if _right_leg_pivot != null:
        _right_leg_pivot.rotation.x = -leg_swing
    if _left_arm_pivot != null:
        _left_arm_pivot.rotation = Vector3(arm_swing + deg_to_rad(-8.0 * _idle_blend), 0.0, deg_to_rad(-4.0))
    if _right_arm_pivot != null:
        _right_arm_pivot.rotation = Vector3(-arm_swing + deg_to_rad(-12.0 * _idle_blend + 5.0 * idle_wave), 0.0, deg_to_rad(4.0))
    if _left_forearm_pivot != null:
        _left_forearm_pivot.rotation.x = deg_to_rad(-9.0 + 4.0 * _locomotion)
    if _right_forearm_pivot != null:
        _right_forearm_pivot.rotation.x = deg_to_rad(-9.0 + 4.0 * _locomotion + 10.0 * maxf(idle_wave, 0.0))
    if _head != null:
        _head.position.y = 0.18 + 0.018 * _locomotion * walk_sin
        _head.rotation.y = deg_to_rad(5.0 * idle_wave)
    if _torso != null:
        _torso.rotation.x = deg_to_rad(2.5 * _locomotion - 3.0 * _idle_blend)
    if _hip != null:
        _hip.position.y = 0.95 + 0.015 * _locomotion * absf(walk_sin)

func _build_rig(level: Node, interactable_script: Script, record: Dictionary, palette: Dictionary) -> void:
    var rig_root := Node3D.new()
    rig_root.name = "ResidentRigRoot"
    add_child(rig_root)

    _hip = Node3D.new()
    _hip.name = "Hip"
    _hip.position = Vector3(0.0, 0.95, 0.0)
    rig_root.add_child(_hip)

    _torso = _cube(_hip, "Torso", Vector3(0.0, 0.18, 0.0), Vector3(0.44, 0.74, 0.22), _dict_color(palette, "shirt"), true, level, interactable_script, record)
    _cube(_hip, "Pelvis", Vector3(0.0, -0.2, 0.0), Vector3(0.42, 0.26, 0.22), _dict_color(palette, "pants"), false)

    var neck := Node3D.new()
    neck.name = "Neck"
    neck.position = Vector3(0.0, 0.67, 0.0)
    _hip.add_child(neck)

    _head = _cube(neck, "Head", Vector3(0.0, 0.18, 0.0), Vector3(0.30, 0.36, 0.28), _dict_color(palette, "skin"), false)
    _cube(_head, "Hair", Vector3(0.0, 0.18, 0.0), Vector3(0.31, 0.12, 0.29), _dict_color(palette, "hair"), false)
    _cube(_head, "Face", Vector3(0.0, 0.13, 0.147), Vector3(0.16, 0.06, 0.02), Color(0.18, 0.15, 0.13), false)

    _left_arm_pivot = _limb_pivot(_hip, "LeftArmPivot", Vector3(-0.29, 0.44, 0.0))
    _cube(_left_arm_pivot, "LeftUpperArm", Vector3(0.0, -0.24, 0.0), Vector3(0.14, 0.48, 0.14), _dict_color(palette, "shirt"), false)
    _left_forearm_pivot = _limb_pivot(_left_arm_pivot, "LeftForearmPivot", Vector3(0.0, -0.46, 0.0))
    _cube(_left_forearm_pivot, "LeftForearm", Vector3(0.0, -0.18, 0.0), Vector3(0.12, 0.36, 0.12), _dict_color(palette, "skin"), false)

    _right_arm_pivot = _limb_pivot(_hip, "RightArmPivot", Vector3(0.29, 0.44, 0.0))
    _cube(_right_arm_pivot, "RightUpperArm", Vector3(0.0, -0.24, 0.0), Vector3(0.14, 0.48, 0.14), _dict_color(palette, "shirt"), false)
    _right_forearm_pivot = _limb_pivot(_right_arm_pivot, "RightForearmPivot", Vector3(0.0, -0.46, 0.0))
    _cube(_right_forearm_pivot, "RightForearm", Vector3(0.0, -0.18, 0.0), Vector3(0.12, 0.36, 0.12), _dict_color(palette, "skin"), false)

    _left_leg_pivot = _limb_pivot(_hip, "LeftLegPivot", Vector3(-0.12, -0.34, 0.0))
    _cube(_left_leg_pivot, "LeftLeg", Vector3(0.0, -0.34, 0.0), Vector3(0.16, 0.68, 0.16), _dict_color(palette, "pants"), false)
    _cube(_left_leg_pivot, "LeftFoot", Vector3(0.0, -0.72, 0.09), Vector3(0.18, 0.10, 0.30), _dict_color(palette, "shoes"), false)

    _right_leg_pivot = _limb_pivot(_hip, "RightLegPivot", Vector3(0.12, -0.34, 0.0))
    _cube(_right_leg_pivot, "RightLeg", Vector3(0.0, -0.34, 0.0), Vector3(0.16, 0.68, 0.16), _dict_color(palette, "pants"), false)
    _cube(_right_leg_pivot, "RightFoot", Vector3(0.0, -0.72, 0.09), Vector3(0.18, 0.10, 0.30), _dict_color(palette, "shoes"), false)

    var privacy_badge := _cube(_torso, "PrivacyBadge", Vector3(0.0, 0.02, 0.125), Vector3(0.16, 0.09, 0.025), _dict_color(palette, "accent"), false)
    privacy_badge.name = "ArchetypePrivacyBadge"

func _cube(parent: Node3D, node_name: String, local_position: Vector3, size: Vector3, color: Color, inspectable: bool, level: Node = null, interactable_script: Script = null, record: Dictionary = {}) -> Node3D:
    var body := StaticBody3D.new()
    body.name = node_name
    body.position = local_position
    parent.add_child(body)

    var mesh_instance := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = size
    mesh_instance.mesh = mesh
    mesh_instance.material_override = _material(color)
    body.add_child(mesh_instance)

    if inspectable:
        var collision := CollisionShape3D.new()
        var shape := BoxShape3D.new()
        shape.size = size
        collision.shape = shape
        body.add_child(collision)
        if interactable_script != null and level != null:
            body.set_script(interactable_script)
            body.call("setup", level, "resident", record)

    return body

func _limb_pivot(parent: Node3D, node_name: String, local_position: Vector3) -> Node3D:
    var pivot := Node3D.new()
    pivot.name = node_name
    pivot.position = local_position
    parent.add_child(pivot)
    return pivot

func _palette(seed: int, accent_color: Color) -> Dictionary:
    var skin_values := [
        Color(0.78, 0.62, 0.48),
        Color(0.66, 0.48, 0.35),
        Color(0.88, 0.72, 0.58),
        Color(0.54, 0.36, 0.26),
        Color(0.74, 0.56, 0.42),
        Color(0.92, 0.78, 0.63)
    ]
    var shirt_values := [
        Color(0.28, 0.40, 0.56),
        Color(0.45, 0.33, 0.52),
        Color(0.38, 0.50, 0.34),
        Color(0.56, 0.39, 0.32),
        Color(0.32, 0.49, 0.52),
        accent_color.darkened(0.08)
    ]
    var hair_values := [
        Color(0.22, 0.15, 0.11),
        Color(0.12, 0.10, 0.09),
        Color(0.42, 0.30, 0.20),
        Color(0.58, 0.48, 0.34),
        Color(0.18, 0.17, 0.16),
        Color(0.35, 0.22, 0.16)
    ]
    var variant: int = int(abs(seed) % skin_values.size())
    return {
        "skin": skin_values[variant],
        "shirt": shirt_values[abs(seed + 2) % shirt_values.size()],
        "pants": Color(0.17, 0.21, 0.29).lightened(float(abs(seed) % 3) * 0.05),
        "hair": hair_values[abs(seed + 4) % hair_values.size()],
        "shoes": Color(0.11, 0.12, 0.14),
        "accent": accent_color.lightened(0.12)
    }

func _dict_color(source: Dictionary, key: String) -> Color:
    var value: Variant = source.get(key, Color.WHITE)
    if typeof(value) == TYPE_COLOR:
        return value
    return Color.WHITE

func _material(color: Color) -> StandardMaterial3D:
    var mat := StandardMaterial3D.new()
    mat.albedo_color = color
    mat.roughness = 0.82
    return mat
