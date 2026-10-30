import type { GameState, Hero } from './types';
import { addGold } from './rules';

/* S.morale -= 3;  (block comment, must not count) */
export function resolveWave(S: GameState, heroes: Hero[]) {
  addGold(S, 10);
  S.walls.gate.hp -= 2;        // nested write -> walls
  S.flags['won_wave'] = true;  // index write -> flags
  for (const h of heroes) h.loyalty--;
  // S.morale = 0;  line comment, must not count
}

// a local helper that happens to share a name with Array.prototype.push
const push = (S: GameState, id: string) => { S.flags[id] = true; };
export function markWave(S: GameState) { push(S, 'marked'); }
