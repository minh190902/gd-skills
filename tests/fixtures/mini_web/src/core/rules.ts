import type { GameState } from './types';

export function addGold(S: GameState, n: number): void {
  S.gold += n;
}

export const addMorale = (s: GameState, n: number) => {
  s.morale = Math.min(10, s.morale + n);
};

export function newGame(S: GameState) {
  S.gold = 0; S.morale = 5; S.log.length = 0;
}
