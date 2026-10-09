extends Node
## Dialogue bridge.

func change_morale(n: int) -> void:
	GameState.morale += n

func set_flag(flag_name: String) -> void:
	GameState.set_flag(flag_name, true)

func check_flag(flag_name: String) -> bool:
	return GameState.check_flag(flag_name)
