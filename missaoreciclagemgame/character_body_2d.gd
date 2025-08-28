extends CharacterBody2D

@export var speed: float = 200.0
var trash_types: Array[String] = ["vidro", "metal", "papel", "organico", "plastico"]
var current_index: int = 0
var current_trash_type: String = trash_types[current_index]

func _physics_process(delta: float) -> void:
	var direction := Input.get_axis("ui_left", "ui_right")
	velocity.x = direction * speed
	move_and_slide()

	if Input.is_action_just_pressed("switch_bin"):
		current_index = (current_index + 1) % trash_types.size()
		current_trash_type = trash_types[current_index]
		update_bin_sprite()

func update_bin_sprite() -> void:
	# Troca sprite da lixeira com base no tipo
	$Sprite2D.texture = load("res://assets/bins/" + current_trash_type + ".png")
