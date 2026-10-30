import type { GameState } from './types';

export function meetSmith(S: GameState) {
  S.flags.met_smith = true;          // read below: paid off
  S.flags.helped_widow = true;       // never read: consequence without payoff
  S.flags.debts++;                   // a counter is a write, not a read
}

export function smithGreeting(S: GameState): string {
  if (S.flags.met_smith) return 'Back again?';
  if (S.flags.knows_tunel) return 'The tunnel...';   // typo: never set
  return 'Who are you?';
}
