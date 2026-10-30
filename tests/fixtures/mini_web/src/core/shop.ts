import type { GameState } from './types';
import { addMorale } from './rules';

export function buy(S: GameState, cost: number) {
  if (S.gold < cost) return false;
  S.gold -= cost;
  S.log.push(`bought for ${cost}`);   // mutator
  addMorale(S, 1);
  return true;
}
