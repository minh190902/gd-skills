extends Node

func load_game(data: Dictionary) -> void:
	GameState.gold = data.gold
	GameState.morale = data.morale
