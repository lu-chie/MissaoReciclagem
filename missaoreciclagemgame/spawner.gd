extends Node2D

@onready var lixo_vidro = preload("res://trash_spawner.tscn")
@onready var timer = $Timer

var trash_ready = false

func _ready():
	timer.start()

func _process(_delta):
	generate_trash()

func random_pos():
	return Vector2(
		randf_range(101, 781),
		 -20
		)

func generate_trash():
	if !trash_ready:
		return
	trash_ready = false
	timer.start()
	var new_trash = lixo_vidro.instantiate() 
	new_trash.position = random_pos()
	get_parent().add_child(new_trash)
	
func _on_timer_timeout():
	trash_ready = true
