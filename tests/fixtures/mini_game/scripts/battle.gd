extends Node
## Battle: rewards gold, hurts units, lowers loyalty.

func resolve(unit: UnitData) -> void:
	unit.loyalty -= 5
	unit.hurt(1)
	GameState.add_gold(5)
	if GameState.check_flag("helped"):
		unit.loyalty += 1
	# GameState.morale = 0   (commented out: must not count)
