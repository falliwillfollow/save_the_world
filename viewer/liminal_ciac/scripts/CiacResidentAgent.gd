extends Node3D
class_name CiacResidentAgent

var _home := Vector3.ZERO
var _task := Vector3.ZERO
var _task_idle_anchor := Vector3.ZERO
var _phase: float = 0.0
var _speed: float = 0.035
var _avatar: Node = null
var _last_locomotion := 0.0
var _last_idle := 0.0

func setup_route(home_position: Vector3, task_position: Vector3, task_idle_anchor: Vector3, speed: float, phase: float) -> void:
    _home = home_position
    _task = task_position
    _task_idle_anchor = task_idle_anchor
    _speed = speed
    _phase = phase
    position = _home

func bind_avatar(avatar: Node) -> void:
    _avatar = avatar

func _process(delta: float) -> void:
    _phase = fmod(_phase + delta * _speed, 1.0)
    var previous := position
    var idle_blend := 0.0

    if _phase < 0.34:
        var t_out := smoothstep(0.0, 0.34, _phase)
        position = _home.lerp(_task, t_out)
    elif _phase < 0.64:
        idle_blend = 1.0
        var idle_t := (_phase - 0.34) / 0.3
        var idle_offset := Vector3(cos(idle_t * TAU) * 0.45, 0.0, sin(idle_t * TAU) * 0.35)
        position = _task_idle_anchor + idle_offset
    else:
        var t_home := smoothstep(0.64, 1.0, _phase)
        position = _task.lerp(_home, t_home)

    var direction := position - previous
    var locomotion := clampf(direction.length() / maxf(delta * 1.2, 0.001), 0.0, 1.0)
    if direction.length() > 0.01:
        rotation.y = atan2(direction.x, direction.z)
    else:
        locomotion = 0.0
    _last_locomotion = lerpf(_last_locomotion, locomotion, clampf(delta * 8.0, 0.0, 1.0))
    _last_idle = lerpf(_last_idle, idle_blend, clampf(delta * 5.0, 0.0, 1.0))
    if _avatar != null and _avatar.has_method("apply_motion"):
        _avatar.apply_motion(_last_locomotion, _last_idle, delta)
