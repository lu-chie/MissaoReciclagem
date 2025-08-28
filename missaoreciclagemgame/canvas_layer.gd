extends CanvasLayer

var score: int = 0
var lives: int = 3

func add_score(value: int) -> void:
	score += value
	$ScoreLabel.text = "Pontos: " + str(score)

func remove_life(value: int) -> void:
	lives -= value
	$LivesLabel.text = "Vidas: " + str(lives)
	if lives <= 0:
		game_over()

func game_over() -> void:
	get_tree().paused = true
	$ScoreLabel.text += "\nGAME OVER"
