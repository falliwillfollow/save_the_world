extends RefCounted
class_name CiacSpatialScale

const MIN_HUMAN_WIDTH := 8.0
const MIN_HUMAN_DEPTH := 7.0
const MIN_HUMAN_HEIGHT := 3.2

static func structure_size(record: Dictionary, base_size: Vector3) -> Vector3:
    var structure_type := str(record.get("type", "structure"))
    var occupancy := _occupancy(record)
    var factor := clampf(sqrt(maxf(float(occupancy), 1.0) / 12.0), 1.0, 2.1)
    var result := Vector3(
        maxf(base_size.x, MIN_HUMAN_WIDTH),
        maxf(base_size.y, MIN_HUMAN_HEIGHT),
        maxf(base_size.z, MIN_HUMAN_DEPTH)
    )

    match structure_type:
        "common_house":
            result.x = maxf(base_size.x * 2.1, 28.0)
            result.y = maxf(base_size.y, _height_for_floors(_floor_count(structure_type)))
            result.z = maxf(base_size.z * 2.2, 22.0)
        "residential_pod":
            result.x = maxf(base_size.x * 1.8, 18.0)
            result.y = maxf(base_size.y, _height_for_floors(_floor_count(structure_type)))
            result.z = maxf(base_size.z * 1.7, 14.0)
        "quiet_studio":
            result.x = maxf(base_size.x * 1.8, 15.0)
            result.y = maxf(base_size.y, _height_for_floors(_floor_count(structure_type)))
            result.z = maxf(base_size.z * 1.8, 12.0)
        "care_room":
            result.x = maxf(base_size.x * 1.9, 14.0)
            result.y = maxf(base_size.y, _height_for_floors(_floor_count(structure_type)))
            result.z = maxf(base_size.z * 1.8, 12.0)
        "food_commons":
            result.x = maxf(base_size.x * 1.8, 22.0)
            result.y = maxf(base_size.y, _height_for_floors(_floor_count(structure_type)))
            result.z = maxf(base_size.z * 1.9, 16.0)
        "protein_commons":
            result.x = maxf(base_size.x * 1.9, 18.0)
            result.y = maxf(base_size.y, _height_for_floors(_floor_count(structure_type)))
            result.z = maxf(base_size.z * 1.9, 13.0)
        "social_cultural":
            result.x = maxf(base_size.x * 1.8, 17.0)
            result.y = maxf(base_size.y, _height_for_floors(_floor_count(structure_type)))
            result.z = maxf(base_size.z * 1.8, 12.0)
        "maintenance_shop":
            result.x = maxf(base_size.x * 1.7, 18.0)
            result.y = maxf(base_size.y, _height_for_floors(_floor_count(structure_type)))
            result.z = maxf(base_size.z * 1.7, 14.0)
        _:
            result.x = maxf(result.x, base_size.x * minf(factor, 1.45))
            result.z = maxf(result.z, base_size.z * minf(factor, 1.45))

    return result

static func scale_record(record: Dictionary) -> Dictionary:
    var structure_type := str(record.get("type", "structure"))
    var occupancy := _occupancy(record)
    var policy := _capacity_policy(structure_type)
    var capacity := int(policy.get("capacity", 10))
    var soft_threshold := int(policy.get("soft_threshold", 8))
    var hard_threshold := int(policy.get("hard_threshold", 14))
    var utilization := 0.0
    if capacity > 0:
        utilization = float(occupancy) / float(capacity)

    var status := "pass"
    if occupancy > hard_threshold:
        status = "fail"
    elif occupancy > soft_threshold or utilization >= 0.85:
        status = "warn"

    return {
        "structure_id": str(record.get("id", "")),
        "label": str(record.get("label", record.get("id", "Structure"))),
        "type": structure_type,
        "occupancy": occupancy,
        "modeled_capacity": capacity,
        "soft_threshold": soft_threshold,
        "hard_threshold": hard_threshold,
        "utilization": utilization,
        "status": status,
        "strategy": str(policy.get("strategy", "review")),
        "floor_count": _floor_count(structure_type),
        "vertical_program": _vertical_program(structure_type),
        "recommendation": _recommendation(status, str(policy.get("strategy", "review"))),
        "research_basis": str(policy.get("research_basis", "Capacity policy needs research-backed review."))
    }

static func _floor_count(structure_type: String) -> int:
    match structure_type:
        "common_house":
            return 3
        "residential_pod":
            return 2
        "food_commons":
            return 2
        "protein_commons":
            return 2
        "quiet_studio":
            return 2
        "care_room":
            return 2
        "social_cultural":
            return 2
        "maintenance_shop":
            return 2
        _:
            return 1

static func _height_for_floors(floors: int) -> float:
    return 0.55 + float(maxi(floors, 1)) * 3.15

static func _vertical_program(structure_type: String) -> String:
    match structure_type:
        "common_house":
            return "ground floor public commons, upper floor assembly/study, roof terrace"
        "residential_pod":
            return "ground floor lounge/hygiene, upper floor private retreat rooms"
        "food_commons":
            return "ground floor dining and prep, upper floor pantry/admin/teaching kitchen"
        "protein_commons":
            return "ground floor production, upper floor review lab and equipment controls"
        "quiet_studio":
            return "ground floor library studio, upper floor quiet carrels and recovery rooms"
        "care_room":
            return "ground floor reception and continuity care, upper floor consult/recovery rooms"
        "social_cultural":
            return "ground floor gathering, upper floor maker/story rooms"
        "maintenance_shop":
            return "ground floor repair bay, upper mezzanine parts and asset records"
        _:
            return "single-level civic function"

static func _capacity_policy(structure_type: String) -> Dictionary:
    match structure_type:
        "residential_pod":
            return {
                "capacity": 12,
                "soft_threshold": 10,
                "hard_threshold": 14,
                "strategy": "duplicate as small-house cluster",
                "research_basis": "Residential pods stay small to protect privacy, mental recovery, and social legibility."
            }
        "common_house":
            return {
                "capacity": 35,
                "soft_threshold": 28,
                "hard_threshold": 45,
                "strategy": "expand shared commons before duplicating",
                "research_basis": "A campus common house can scale as a student-union-like social core, but crowding must stay voluntary and low-pressure."
            }
        "food_commons":
            return {
                "capacity": 18,
                "soft_threshold": 14,
                "hard_threshold": 24,
                "strategy": "expand dining and prep node",
                "research_basis": "Food commons can scale by equipment, seating, and delivery flow before a full duplicate is needed."
            }
        "protein_commons":
            return {
                "capacity": 8,
                "soft_threshold": 6,
                "hard_threshold": 12,
                "strategy": "expand equipment bay or add satellite production",
                "research_basis": "Specialized production should scale around equipment throughput and reviewable public-health controls."
            }
        "care_room":
            return {
                "capacity": 6,
                "soft_threshold": 4,
                "hard_threshold": 10,
                "strategy": "duplicate as care satellite",
                "research_basis": "Care rooms should remain calm, private, and close enough to residents for dignified continuity."
            }
        "social_cultural":
            return {
                "capacity": 18,
                "soft_threshold": 14,
                "hard_threshold": 26,
                "strategy": "expand with high, medium, and low-stimulation rooms",
                "research_basis": "Belonging spaces need multiple social intensities so expansion does not become compulsory crowding."
            }
        "maintenance_shop":
            return {
                "capacity": 6,
                "soft_threshold": 5,
                "hard_threshold": 10,
                "strategy": "expand service edge and tool staging",
                "research_basis": "Maintenance centralizes tools and repair flow, while keeping labor visibility explicit."
            }
        "quiet_studio":
            return {
                "capacity": 8,
                "soft_threshold": 6,
                "hard_threshold": 12,
                "strategy": "add quiet rooms before enlarging the same room",
                "research_basis": "Quiet, study, and recovery spaces lose function when noise and interruption rise."
            }
        _:
            return {
                "capacity": 10,
                "soft_threshold": 8,
                "hard_threshold": 14,
                "strategy": "review",
                "research_basis": "No type-specific scaling policy is attached yet."
            }

static func _recommendation(status: String, strategy: String) -> String:
    match status:
        "pass":
            return "Within modeled capacity; current footprint can remain stable at this population."
        "warn":
            return "Approaching the soft threshold; use the stated strategy before the next population increase."
        "fail":
            return "Past the hard threshold; redesign, expand, or duplicate before treating this scale as coherent."
        _:
            return "Review capacity assumptions before promoting this structure."

static func _occupancy(record: Dictionary) -> int:
    var state_value: Variant = record.get("state", {})
    if typeof(state_value) != TYPE_DICTIONARY:
        return 1
    var state: Dictionary = state_value
    return int(state.get("occupancy", state.get("residents_served", 1)))
