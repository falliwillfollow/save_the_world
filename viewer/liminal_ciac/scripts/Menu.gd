extends Control

const GAME_SCENE := "res://scenes/Main.tscn"
const DEFAULT_POPULATION := 80
const MIN_POPULATION := 12
const MAX_POPULATION := 1500
const SELECTED_MANIFEST_PATH := "user://ciac_selected.world.json"

@onready var start_button: Button = $CenterContainer/Panel/VBoxContainer/StartButton
@onready var exit_button: Button = $CenterContainer/Panel/VBoxContainer/ExitButton
@onready var population_spin_box: SpinBox = $CenterContainer/Panel/VBoxContainer/PopulationSpinBox
@onready var population_slider: HSlider = $CenterContainer/Panel/VBoxContainer/PopulationSlider
@onready var scale_summary: Label = $CenterContainer/Panel/VBoxContainer/ScaleSummary
@onready var status_label: Label = $CenterContainer/Panel/VBoxContainer/StatusLabel

var _syncing_population := false

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
    population_spin_box.value_changed.connect(_on_population_spin_changed)
    population_slider.value_changed.connect(_on_population_slider_changed)
    start_button.pressed.connect(_on_start_pressed)
    exit_button.pressed.connect(_on_exit_pressed)
    _set_population(_saved_population())
    start_button.grab_focus()

func _on_start_pressed() -> void:
    var population := _current_population()
    start_button.disabled = true
    status_label.text = "Building %s-resident manifest..." % population
    await get_tree().process_frame

    var generated_path := _generate_manifest(population)
    ProjectSettings.set_setting("ciac/selected_population", population)
    if generated_path.is_empty():
        ProjectSettings.set_setting("ciac/selected_manifest_path", "")
        status_label.text = "Manifest generation failed. Starting bundled 80-resident world."
        await get_tree().create_timer(0.35).timeout
    else:
        ProjectSettings.set_setting("ciac/selected_manifest_path", generated_path)
        status_label.text = "Manifest ready."
        await get_tree().process_frame
    get_tree().change_scene_to_file(GAME_SCENE)

func _on_exit_pressed() -> void:
    get_tree().quit()

func _on_population_spin_changed(value: float) -> void:
    if _syncing_population:
        return
    _set_population(int(round(value)))

func _on_population_slider_changed(value: float) -> void:
    if _syncing_population:
        return
    _set_population(int(round(value)))

func _set_population(value: int) -> void:
    var population := clampi(value, MIN_POPULATION, MAX_POPULATION)
    _syncing_population = true
    population_spin_box.value = population
    population_slider.value = population
    _syncing_population = false
    scale_summary.text = _scale_summary_for(population)

func _current_population() -> int:
    return clampi(int(round(population_spin_box.value)), MIN_POPULATION, MAX_POPULATION)

func _saved_population() -> int:
    return clampi(int(ProjectSettings.get_setting("ciac/selected_population", DEFAULT_POPULATION)), MIN_POPULATION, MAX_POPULATION)

func _scale_summary_for(population: int) -> String:
    var people := clampi(population, MIN_POPULATION, MAX_POPULATION)
    var village_blocks := maxi(1, int(ceil(float(people) / 150.0)))
    var pods := maxi(1, int(ceil(float(people) / 12.0)))
    var commons := maxi(1, int(ceil(float(people) / 100.0)))
    var scale_class := "micro commons"
    if people > 1500:
        scale_class = "regional membrane"
    elif people > 750:
        scale_class = "town/city layer"
    elif people > 150:
        scale_class = "multi-block district"
    elif people > 20:
        scale_class = "village block"
    return "%d block%s | %d pod%s | %d commons | %s" % [
        village_blocks,
        "" if village_blocks == 1 else "s",
        pods,
        "" if pods == 1 else "s",
        commons,
        scale_class
    ]

func _generate_manifest(population: int) -> String:
    var repo_root := ProjectSettings.globalize_path("res://../..")
    var output_path := ProjectSettings.globalize_path(SELECTED_MANIFEST_PATH)
    var command := "Set-Location -LiteralPath %s; py -3.10 -m ciac export-world --runtime examples/generated/micro_commons_runtime_bundle.json --research-registry research_registry/ciac_research_registry_v0.yaml --output %s --population %d --world-id civic_floor_%d_v0" % [
        _ps_quote(repo_root),
        _ps_quote(output_path),
        population,
        population
    ]
    var args := PackedStringArray([
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        command,
    ])
    var output := []
    var exit_code := OS.execute("powershell", args, output, true)
    if exit_code != 0 or not FileAccess.file_exists(SELECTED_MANIFEST_PATH):
        push_warning("CIaC manifest generation failed (%s): %s" % [exit_code, "\n".join(output)])
        return ""
    return SELECTED_MANIFEST_PATH

func _ps_quote(value: String) -> String:
    return "'%s'" % value.replace("'", "''")
