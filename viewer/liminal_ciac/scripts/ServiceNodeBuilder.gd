extends RefCounted
class_name ServiceNodeBuilder

const P := preload("res://scripts/CiacInteriorPrimitives.gd")

static func build(level: Node, geometry_root: Node3D, label_root: Node3D, node: Dictionary, base: Vector3, color: Color, interactable_script: Script) -> void:
    var root := Node3D.new()
    root.name = str(node.get("id", "service_node"))
    root.position = base
    root.rotation.y = _rotation_toward_center(base)
    geometry_root.add_child(root)

    var node_type := str(node.get("type", "node"))
    match node_type:
        "water":
            _water_station(root, node, level, interactable_script, color)
        "energy":
            _energy_station(root, node, level, interactable_script, color)
        "sanitation":
            _sanitation_station(root, node, level, interactable_script, color)
        "risk":
            _risk_station(root, node, level, interactable_script, color)
        _:
            _generic_station(root, node, level, interactable_script, color)

    P.label(label_root, str(node.get("label", "Service Node")), base + Vector3(0.0, 4.0, 0.0), 27)

static func _water_station(root: Node3D, node: Dictionary, level: Node, interactable_script: Script, color: Color) -> void:
    P.box(root, "WaterServicePad", Vector3(0.0, 0.06, 0.0), Vector3(11.0, 0.12, 8.5), Color(0.34, 0.42, 0.39), true)
    _canopy(root, "WaterPumpQualityCanopy", Vector3(-0.8, 3.0, 2.2), Vector3(8.7, 0.24, 4.1), Color(0.46, 0.52, 0.49))
    P.fixture_cylinder(root, level, interactable_script, "PrimaryWaterReserveTank", Vector3(-2.8, 1.55, -0.6), 1.6, 3.1, color, node, "Primary water reserve tank", "Stored reserve capacity fixture", "water.resilient_water_commons.v0_1", ["shows reserve storage separate from live source flow"], ["Tank volume is symbolic; the model ledger remains authoritative."], 32)
    P.fixture_cylinder(root, level, interactable_script, "DailyBufferTank", Vector3(1.4, 1.15, -1.2), 1.1, 2.3, color.lightened(0.18), node, "Daily water buffer tank", "Short-cycle buffer fixture", "water.resilient_water_commons.v0_1", ["makes daily drawdown/restoration behavior visible as a distinct layer"], ["Future UI should bind this to live stored/current telemetry."], 28)
    P.fixture_box(root, level, interactable_script, "WellHeadAndPump", Vector3(-4.5, 0.75, 2.6), Vector3(1.2, 1.3, 1.2), Color(0.52, 0.52, 0.48), node, "Well head and pump", "Water source fixture", "water.resilient_water_commons.v0_1", ["represents source flow before reserve refill"], ["Well safety, rights, testing, and local review remain explicit assumptions."])
    P.fixture_box(root, level, interactable_script, "WaterQualityBench", Vector3(2.8, 0.78, 2.5), Vector3(3.2, 0.42, 1.1), Color(0.42, 0.31, 0.25), node, "Water quality bench", "Testing and release fixture", "water_public_health.water_public_health_sanitation_labor_protocal_v0.active", ["connects water service to public-health verification"], ["Does not certify any water as potable."])
    P.fixture_box(root, level, interactable_script, "ReserveGaugeBoard", Vector3(5.0, 1.75, -0.6), Vector3(0.18, 1.7, 3.3), Color(0.22, 0.3, 0.34), node, "Reserve gauge board", "Storage and net-flow visibility board", "water.resilient_water_commons.v0_1", ["represents the user's need to see level, drawdown, restoration, and reserve status"], ["Future sprint should bind this to live telemetry text."])
    P.local_label(root, _resource_board_text(node, "Water", "liters"), Vector3(4.78, 2.0, -0.6), 18, Color(0.84, 0.94, 1.0), Vector3(0.0, -PI * 0.5, 0.0))
    P.box(root, "PipeToCampus", Vector3(0.0, 0.12, 4.6), Vector3(1.0, 0.12, 5.2), Color(0.26, 0.48, 0.62), true)
    P.plaque(root, level, interactable_script, "WaterModulesPlaque", Vector3(-5.0, 1.15, -2.9), node, "Modules and sources")

static func _energy_station(root: Node3D, node: Dictionary, level: Node, interactable_script: Script, color: Color) -> void:
    P.box(root, "EnergyServicePad", Vector3(0.0, 0.06, 0.0), Vector3(12.0, 0.12, 8.5), Color(0.34, 0.42, 0.39), true)
    for index in range(4):
        var x := -4.2 + float(index) * 2.8
        P.box(root, "SolarTable%d" % index, Vector3(x, 0.72, -2.5), Vector3(2.2, 0.12, 1.5), color, true)
        P.box(root, "SolarTableStand%d" % index, Vector3(x, 0.38, -2.5), Vector3(0.35, 0.65, 0.35), Color(0.42, 0.42, 0.4), true)
    _utility_shed(root, "EnergyControlKiosk", Vector3(-1.7, 0.0, 1.2), Vector3(5.6, 3.1, 3.4), Color(0.52, 0.5, 0.43))
    P.fixture_box(root, level, interactable_script, "CriticalBatteryCabinet", Vector3(-3.2, 1.25, 1.2), Vector3(2.0, 2.1, 1.5), Color(0.56, 0.56, 0.48), node, "Critical battery cabinet", "Critical-load reserve fixture", "energy.critical_load_energy_commons.v0_1", ["represents protected runtime for refrigeration, communication, lighting, and controls"], ["Battery sizing and electrical safety require engineering review."])
    P.fixture_box(root, level, interactable_script, "InverterControlCabinet", Vector3(-0.4, 1.15, 1.2), Vector3(1.5, 1.9, 1.3), Color(0.45, 0.47, 0.44), node, "Inverter control cabinet", "Energy control fixture", "energy.critical_load_energy_commons.v0_1", ["makes critical-load controls inspectable"], ["No electrical certification implied."])
    P.fixture_box(root, level, interactable_script, "CriticalLoadBoard", Vector3(3.8, 1.7, 1.2), Vector3(0.18, 1.65, 3.5), Color(0.22, 0.3, 0.34), node, "Critical load board", "Energy priority visibility board", "energy.critical_load_energy_commons.v0_1", ["shows which loads the model assumes are protected"], ["Future sprint should list actual protected loads from telemetry."])
    P.local_label(root, _resource_board_text(node, "Energy", "kWh"), Vector3(3.58, 1.98, 1.2), 18, Color(1.0, 0.94, 0.68), Vector3(0.0, -PI * 0.5, 0.0))
    P.box(root, "EnergyCableRun", Vector3(0.0, 0.12, 4.5), Vector3(1.0, 0.12, 5.0), Color(0.72, 0.58, 0.22), true)
    P.plaque(root, level, interactable_script, "EnergyModulesPlaque", Vector3(-5.3, 1.15, 2.8), node, "Modules and sources")

static func _sanitation_station(root: Node3D, node: Dictionary, level: Node, interactable_script: Script, color: Color) -> void:
    P.open_shell(root, Vector3(11.5, 3.2, 8.0), color, 0.28, 2.8, 3.2)
    P.box(root, "CleanSideMat", Vector3(-2.8, 0.12, 0.5), Vector3(4.2, 0.08, 5.0), Color(0.34, 0.45, 0.39), true)
    P.box(root, "DirtySideMat", Vector3(2.8, 0.12, 0.5), Vector3(4.2, 0.08, 5.0), Color(0.48, 0.4, 0.36), true)
    P.box(root, "CleanDirtyBarrier", Vector3(0.0, 1.25, 0.5), Vector3(0.16, 2.25, 5.3), Color(0.62, 0.58, 0.55), true)
    P.fixture_box(root, level, interactable_script, "GreywaterRouteBoard", Vector3(-5.05, 1.55, -1.2), Vector3(0.18, 1.45, 3.1), Color(0.22, 0.3, 0.34), node, "Greywater route board", "Greywater boundary visibility board", "sanitation.hygienic_circular_commons.v0_1", ["makes greywater boundaries explicit"], ["Local greywater legality and design remain unresolved until reviewed."])
    P.fixture_box(root, level, interactable_script, "BlackwaterSafetyGate", Vector3(5.05, 1.55, -1.2), Vector3(0.18, 1.45, 3.1), Color(0.22, 0.3, 0.34), node, "Blackwater safety gate", "Blackwater hazard boundary", "sanitation.hygienic_circular_commons.v0_1", ["prevents sanitation from being an invisible or casual workflow"], ["Requires professional wastewater design and worker safety protocols."])
    P.fixture_box(root, level, interactable_script, "PpeLocker", Vector3(-3.5, 1.15, 2.7), Vector3(1.2, 1.85, 1.4), Color(0.62, 0.58, 0.52), node, "Sanitation PPE locker", "Worker safety fixture", "sanitation.hygienic_circular_commons.v0_1", ["makes sanitation labor visibility and worker protection explicit"], ["Training, equipment selection, and exposure policy require review."])
    P.fixture_box(root, level, interactable_script, "HandwashStation", Vector3(-1.7, 0.85, 2.8), Vector3(1.2, 0.75, 0.9), Color(0.72, 0.72, 0.68), node, "Sanitation handwash station", "Hygiene access fixture", "sanitation.shared_bathhouse.active", ["represents toilet/hygiene access support"], ["Fixture count and accessibility need review."])
    P.fixture_box(root, level, interactable_script, "SeparatedWasteBins", Vector3(2.7, 0.72, 2.6), Vector3(2.8, 1.0, 1.1), Color(0.5, 0.5, 0.48), node, "Separated waste bins", "Waste stream separation fixture", "sanitation.hygienic_circular_commons.v0_1", ["makes waste-stream separation visible"], ["Hazardous waste rules are jurisdiction-specific."])
    P.fixture_box(root, level, interactable_script, "EmergencyFallbackCrate", Vector3(3.9, 0.72, -2.5), Vector3(1.8, 1.1, 1.2), Color(0.64, 0.48, 0.28), node, "Emergency sanitation fallback crate", "Fallback sanitation fixture", "sanitation.hygienic_circular_commons.v0_1", ["represents emergency sanitation continuity"], ["Fallback use must be time-limited and public-health reviewed."])
    P.local_label(root, _sanitation_board_text(node), Vector3(-4.82, 1.92, -1.2), 17, Color(0.9, 0.94, 0.9), Vector3(0.0, PI * 0.5, 0.0))
    P.local_label(root, _sanitation_safety_text(node), Vector3(4.82, 1.92, -1.2), 17, Color(0.96, 0.88, 0.78), Vector3(0.0, -PI * 0.5, 0.0))
    P.plaque(root, level, interactable_script, "SanitationModulesPlaque", Vector3(-5.0, 1.15, 2.6), node, "Modules and sources")

static func _risk_station(root: Node3D, node: Dictionary, level: Node, interactable_script: Script, color: Color) -> void:
    P.box(root, "RiskBoardPad", Vector3(0.0, 0.06, 0.0), Vector3(8.5, 0.12, 6.5), Color(0.34, 0.42, 0.39), true)
    _pavilion(root, "RiskGovernancePavilion", Vector3(0.0, 0.0, 0.0), Vector3(8.6, 3.2, 6.4), color.lightened(0.12))
    P.fixture_box(root, level, interactable_script, "ScenarioBoard", Vector3(0.0, 1.75, -2.1), Vector3(5.8, 1.9, 0.18), color, node, "Scenario board", "Stress-test and recovery status board", "risk_resilience.graceful_degradation_engine.v0_1", ["shows the model's scenario and recovery playbook surface"], ["Must not become opaque emergency authority."])
    P.fixture_box(root, level, interactable_script, "DependencyMapTable", Vector3(0.0, 0.72, 0.5), Vector3(4.6, 0.36, 1.8), Color(0.42, 0.31, 0.25), node, "Dependency map table", "System dependency reasoning fixture", "risk_resilience.graceful_degradation_engine.v0_1", ["makes water/energy/food/sanitation dependencies inspectable"], ["Dependency graph should be bound to model data in a future sprint."])
    P.local_label(root, _risk_board_text(node), Vector3(0.0, 2.1, -1.88), 18, Color(0.94, 0.9, 1.0))
    P.box(root, "DecisionLogBench", Vector3(0.0, 0.42, 2.2), Vector3(4.4, 0.34, 0.55), Color(0.32, 0.48, 0.47), true)
    P.plaque(root, level, interactable_script, "RiskModulesPlaque", Vector3(-3.6, 1.15, 0.2), node, "Modules and sources")

static func _generic_station(root: Node3D, node: Dictionary, level: Node, interactable_script: Script, color: Color) -> void:
    P.box(root, "GenericServicePad", Vector3(0.0, 0.06, 0.0), Vector3(7.5, 0.12, 6.0), Color(0.34, 0.42, 0.39), true)
    P.box(root, "ServiceCabinet", Vector3(0.0, 1.15, 0.0), Vector3(2.2, 1.9, 1.6), color, true)
    P.plaque(root, level, interactable_script, "ServiceModulesPlaque", Vector3(-3.0, 1.15, 0.0), node, "Modules and sources")

static func _canopy(root: Node3D, node_name: String, center: Vector3, size: Vector3, color: Color) -> void:
    P.box(root, "%sRoof" % node_name, center, size, color, true)
    var post_y := center.y * 0.5
    var post_h := center.y
    var x_half := size.x * 0.5 - 0.35
    var z_half := size.z * 0.5 - 0.35
    for x_sign in [-1.0, 1.0]:
        for z_sign in [-1.0, 1.0]:
            P.box(root, "%sPost" % node_name, center + Vector3(x_sign * x_half, -post_y, z_sign * z_half), Vector3(0.18, post_h, 0.18), Color(0.34, 0.34, 0.32), true)

static func _utility_shed(root: Node3D, node_name: String, origin: Vector3, size: Vector3, color: Color) -> void:
    var wall_h := size.y
    P.box(root, "%sFloor" % node_name, origin + Vector3(0.0, 0.08, 0.0), Vector3(size.x, 0.12, size.z), Color(0.38, 0.4, 0.38), true)
    P.box(root, "%sRoof" % node_name, origin + Vector3(0.0, wall_h + 0.12, 0.0), Vector3(size.x + 0.4, 0.24, size.z + 0.4), color.lightened(0.08), true)
    P.box(root, "%sBackWall" % node_name, origin + Vector3(0.0, wall_h * 0.5, -size.z * 0.5), Vector3(size.x, wall_h, 0.22), color, true)
    P.box(root, "%sLeftWall" % node_name, origin + Vector3(-size.x * 0.5, wall_h * 0.5, 0.0), Vector3(0.22, wall_h, size.z), color, true)
    P.box(root, "%sRightWall" % node_name, origin + Vector3(size.x * 0.5, wall_h * 0.5, 0.0), Vector3(0.22, wall_h, size.z), color, true)
    P.box(root, "%sThreshold" % node_name, origin + Vector3(0.0, 0.1, size.z * 0.5 + 0.7), Vector3(size.x * 0.55, 0.08, 1.2), Color(0.32, 0.45, 0.43), true)

static func _pavilion(root: Node3D, node_name: String, origin: Vector3, size: Vector3, color: Color) -> void:
    P.box(root, "%sBackWall" % node_name, origin + Vector3(0.0, size.y * 0.45, -size.z * 0.5), Vector3(size.x, size.y * 0.9, 0.22), color, true)
    P.box(root, "%sRoof" % node_name, origin + Vector3(0.0, size.y + 0.18, 0.0), Vector3(size.x + 0.55, 0.28, size.z + 0.55), color.lightened(0.12), true)
    var x_half := size.x * 0.5 - 0.3
    var z_front := size.z * 0.5 - 0.3
    for x_sign in [-1.0, 1.0]:
        P.box(root, "%sFrontPost" % node_name, origin + Vector3(x_sign * x_half, size.y * 0.5, z_front), Vector3(0.22, size.y, 0.22), Color(0.34, 0.34, 0.32), true)

static func _rotation_toward_center(base: Vector3) -> float:
    if absf(base.x) >= absf(base.z):
        if base.x < 0.0:
            return PI * 0.5
        return -PI * 0.5
    if base.z > 0.0:
        return PI
    return 0.0

static func _resource_board_text(node: Dictionary, title: String, fallback_unit: String) -> String:
    var metrics := _dict_value(node, "metrics")
    var unit := str(metrics.get("unit", fallback_unit))
    var status := str(metrics.get("status", "unknown")).to_upper()
    var current := _number(metrics.get("current", metrics.get("stored", 0.0)), 1)
    var capacity := _number(metrics.get("capacity", 0.0), 1)
    var ratio := float(metrics.get("current_ratio", 0.0)) * 100.0
    var net := _signed_number(metrics.get("net_per_day", metrics.get("daily_net", 0.0)), 2)
    var floor_value := _number(metrics.get("reserve_floor", 0.0), 1)
    var text := "%s %s\n%s / %s %s\nnet/day %s\nreserve floor %s" % [title, status, current, capacity, unit, net, floor_value]
    if metrics.has("critical_load_runtime_hours"):
        text += "\ncritical runtime %sh" % _number(metrics.get("critical_load_runtime_hours", 0.0), 0)
    elif ratio > 0.0:
        text += "\ncurrent %.0f%%" % ratio
    return text

static func _sanitation_board_text(node: Dictionary) -> String:
    var fields := _dict_value(_dict_value(node, "metrics"), "fields")
    return "SANITATION %s\ntoilet/hygiene %s\ngreywater boundary %s\nwaste separation %s" % [
        str(_dict_value(node, "metrics").get("status", "unknown")).to_upper(),
        _yes_no(fields.get("toilet_hygiene_access_supported", false)),
        _yes_no(fields.get("greywater_boundary_defined", false)),
        _yes_no(fields.get("waste_stream_separation_supported", false))
    ]

static func _sanitation_safety_text(node: Dictionary) -> String:
    var fields := _dict_value(_dict_value(node, "metrics"), "fields")
    return "SAFETY\nblackwater path %s\nworker safety %s\nfallback %s" % [
        _yes_no(fields.get("blackwater_path_defined", false)),
        _yes_no(fields.get("worker_safety_training_supported", false)),
        _yes_no(fields.get("emergency_sanitation_fallback_supported", false))
    ]

static func _risk_board_text(node: Dictionary) -> String:
    var metrics := _dict_value(node, "metrics")
    return "RISK / GOVERNANCE\ncapability %s\nmodules %d\nscenario review active" % [
        str(metrics.get("capability_status", metrics.get("status", "unknown"))).to_upper(),
        _array_value(node, "module_refs").size()
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

static func _yes_no(value: Variant) -> String:
    return "yes" if bool(value) else "no"

static func _number(value: Variant, decimals: int) -> String:
    var numeric := float(value)
    return "%.*f" % [decimals, numeric]

static func _signed_number(value: Variant, decimals: int) -> String:
    var numeric := float(value)
    var sign := "+" if numeric >= 0.0 else ""
    return "%s%.*f" % [sign, decimals, numeric]
