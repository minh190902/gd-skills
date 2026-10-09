class_name UnitData
extends Resource

@export var hp: int = 10
@export_range(0, 100) var loyalty: int = 50

func hurt(n: int) -> void:
	hp -= n
