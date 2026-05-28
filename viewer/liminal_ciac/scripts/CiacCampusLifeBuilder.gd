extends RefCounted
class_name CiacCampusLifeBuilder

const P := preload("res://scripts/CiacInteriorPrimitives.gd")
const AGENT_SCRIPT := preload("res://scripts/CiacResidentAgent.gd")
const AVATAR_SCRIPT := preload("res://scripts/CiacResidentAvatar.gd")

static func build(level: Node, geometry_root: Node3D, label_root: Node3D, manifest: Dictionary, location_positions: Dictionary, interactable_script: Script) -> void:
    var events: Array = _array_value(manifest, "daily_events")
    if events.is_empty():
        return
    var residents_by_id := _residents_by_id(manifest)

    var root := Node3D.new()
    root.name = "CiacCampusLife"
    geometry_root.add_child(root)

    var count := mini(events.size(), 12)
    for index in range(count):
        var event_value: Variant = events[index]
        if typeof(event_value) != TYPE_DICTIONARY:
            continue
        var event: Dictionary = event_value
        var resident: Dictionary = _dict_value(residents_by_id, str(event.get("resident_id", "")))
        _spawn_event_agent(root, label_root, level, event, resident, location_positions, interactable_script, index)

static func _spawn_event_agent(root: Node3D, label_root: Node3D, level: Node, event: Dictionary, resident: Dictionary, location_positions: Dictionary, interactable_script: Script, index: int) -> void:
    var location_id := str(event.get("location_id", ""))
    var home_id := str(resident.get("home_structure_id", ""))
    var home_position := _location_position(location_positions, home_id)
    if home_position == Vector3.ZERO:
        home_position = _dict_to_vec3(resident.get("position", {}))

    var task_position := _location_position(location_positions, location_id) + _task_offset(str(event.get("type", "")), index)
    var idle_anchor := task_position + Vector3(0.0, 0.0, 0.8)
    var home_offset := _home_offset(index)
    home_position += home_offset

    var agent := Node3D.new()
    agent.name = str(resident.get("id", "resident_routine_%d" % index))
    agent.set_script(AGENT_SCRIPT)
    agent.call("setup_route", home_position, task_position, idle_anchor, 0.026 + float(index % 5) * 0.004, float(index) / maxf(float(count_hint()), 1.0))
    root.add_child(agent)

    var resident_record := _resident_record(event, resident, home_id, location_id)
    var avatar := Node3D.new()
    avatar.name = "ResidentAvatar"
    avatar.set_script(AVATAR_SCRIPT)
    avatar.call("setup", level, interactable_script, resident_record, _color_for_event(str(event.get("type", ""))), index + int(abs(hash(str(resident.get("id", ""))))))
    agent.add_child(avatar)
    agent.call("bind_avatar", avatar)

static func count_hint() -> int:
    return 12

static func _resident_record(event: Dictionary, resident: Dictionary, home_id: String, location_id: String) -> Dictionary:
    var label := "%s - %s" % [str(resident.get("label", "Resident")), str(event.get("label", "Daily routine"))]
    return {
        "id": "%s.%s" % [str(resident.get("id", "resident")), str(event.get("id", "event"))],
        "label": label,
        "type": "resident_routine",
        "archetype": str(resident.get("archetype", "unknown")),
        "resident_id": str(resident.get("id", "")),
        "event_id": str(event.get("id", "")),
        "event_type": str(event.get("type", "")),
        "current_routine": str(event.get("label", "Daily routine")),
        "time": str(event.get("time", "")),
        "duration_minutes": int(event.get("duration_minutes", 0)),
        "home_structure_id": home_id,
        "location_id": location_id,
        "privacy": str(resident.get("privacy", "archetype_only")),
        "module_refs": _array_value(event, "module_refs"),
        "model_effects": [
            "visualizes an archetypal daily event from the manifest",
            "connects resident home, task destination, and module refs in the walkable world",
            "uses a procedural privacy-preserving resident avatar rather than a personal identity model"
        ],
        "operating_notes": [
            "Resident identity remains archetype-level only.",
            "Motion is a lightweight route visualization, not a full schedule/pathfinding simulation.",
            "Avatar clothing and skin/hair palettes are randomized for legibility and should not be read as demographic modeling."
        ]
    }

static func _location_position(location_positions: Dictionary, location_id: String) -> Vector3:
    var value: Variant = location_positions.get(location_id, Vector3.ZERO)
    if typeof(value) == TYPE_VECTOR3:
        return value
    return Vector3.ZERO

static func _event_offset(index: int) -> Vector3:
    var ring := float(index % 4)
    var lane := float(index / 4)
    var angle := ring * TAU / 4.0 + lane * 0.45
    var radius := 2.6 + lane * 0.7
    return Vector3(cos(angle) * radius, 0.0, sin(angle) * radius)

static func _home_offset(index: int) -> Vector3:
    var angle := float(index % 6) * TAU / 6.0
    return Vector3(cos(angle) * 1.2, 0.0, sin(angle) * 1.2)

static func _task_offset(event_type: String, index: int) -> Vector3:
    var lateral := -1.5 + float(index % 4)
    match event_type:
        "care":
            return Vector3(1.8, 0.0, -1.6)
        "commons_labor", "food":
            return Vector3(-2.2 + lateral * 0.35, 0.0, -2.1)
        "maintenance", "learning":
            return Vector3(2.4 + lateral * 0.25, 0.0, 1.2)
        "passion_time":
            return Vector3(-2.4 + lateral * 0.3, 0.0, 0.4)
        "rest":
            return Vector3(2.4 + lateral * 0.25, 0.0, 2.1)
        "social":
            return Vector3(-1.0 + lateral * 0.35, 0.0, 1.7)
        "governance":
            return Vector3(3.0, 0.0, -2.4)
        _:
            return _event_offset(index) * 0.45

static func _color_for_event(event_type: String) -> Color:
    match event_type:
        "care":
            return Color(0.76, 0.34, 0.48)
        "commons_labor", "maintenance", "food":
            return Color(0.82, 0.58, 0.28)
        "passion_time", "learning":
            return Color(0.34, 0.62, 0.62)
        "rest":
            return Color(0.46, 0.54, 0.68)
        "social", "governance":
            return Color(0.64, 0.52, 0.76)
        _:
            return Color(0.72, 0.72, 0.66)

static func _array_value(source: Dictionary, key: String) -> Array:
    var value: Variant = source.get(key, [])
    if typeof(value) == TYPE_ARRAY:
        return value
    return []

static func _residents_by_id(manifest: Dictionary) -> Dictionary:
    var result := {}
    for resident in _array_value(manifest, "residents"):
        if typeof(resident) == TYPE_DICTIONARY:
            var resident_id := str(resident.get("id", ""))
            if not resident_id.is_empty():
                result[resident_id] = resident
    return result

static func _dict_value(source: Dictionary, key: String) -> Dictionary:
    var value: Variant = source.get(key, {})
    if typeof(value) == TYPE_DICTIONARY:
        return value
    return {}

static func _dict_to_vec3(value: Variant) -> Vector3:
    if typeof(value) != TYPE_DICTIONARY:
        return Vector3.ZERO
    return Vector3(
        float(value.get("x", 0.0)),
        float(value.get("y", 0.0)),
        float(value.get("z", 0.0))
    )
