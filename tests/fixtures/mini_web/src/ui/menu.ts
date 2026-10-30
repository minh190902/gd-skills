import type { GameState } from '../core/types';
import { buy } from '../core/shop';

// one hop to shop.buy (gold, log); morale is two hops away (buy -> addMorale) and is not counted
export function onBuyClick(S: GameState) {
  buy(S, 3);
}
