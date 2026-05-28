extends StaticBody3D
class_name CiacStructureInteractable

@export var prompt: String = "Inspect CIaC structure"

var level: Node
var record_kind: String = "structure"
var record: Dictionary = {}

func setup(owner_level: Node, kind: String, source_record: Dictionary) -> void:
    level = owner_level
    record_kind = kind
    record = source_record
    var display_label := str(record.get("label", "CIaC element"))
    if record_kind == "vertical_access":
        prompt = display_label
    else:
        prompt = "Inspect %s" % display_label

func interact(actor: Node) -> void:
    if record_kind == "vertical_access" and level and level.has_method("use_vertical_access"):
        level.use_vertical_access(record, actor)
        return
    if level and level.has_method("show_record_inspection"):
        level.show_record_inspection(record_kind, record, actor)
