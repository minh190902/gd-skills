extends Node

func new_game() -> void:
	GameState.reset_game()
	SaveLoadManager.load_game({})
