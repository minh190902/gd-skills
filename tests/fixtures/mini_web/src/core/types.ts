/** Whole-run state. */
export interface GameState {
  gold: number;
  morale: number;
  /** story flags */
  flags: Record<string, boolean>;
  log: string[];
  walls: { gate: { hp: number } };
  unusedCounter?: number;
}

export interface Hero {
  name: string;
  loyalty: number;
}
