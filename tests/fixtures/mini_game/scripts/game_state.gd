extends Node
## Global state.

var gold: int = 100
var morale: int = 50
var day: int = 1
var unused_counter: int = 0
var story_flags: Dictionary = {}

func add_gold(n: int) -> void:
	gold += n

func set_flag(flag_name: String, value: Variant = true) -> void:
	story_flags[flag_name] = value

func check_flag(flag_name: String) -> bool:
	return story_flags.get(flag_name, false)

func reset_game() -> void:
	gold = 100
	morale = 50
