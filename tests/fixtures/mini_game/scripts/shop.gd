extends Node
## Shop: spends gold, price depends on morale.

func buy() -> void:
	var price := 10 if GameState.morale > 40 else 15
	GameState.gold -= price  # pay
