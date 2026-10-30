import type { GameState } from '../core/types';

export function restore(S: GameState, raw: GameState) {
  S.gold = raw.gold; S.morale = raw.morale; S.flags = raw.flags;
}
