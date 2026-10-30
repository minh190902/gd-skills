import type { GameState } from '../core/types';

export class Hud {
  constructor(private game: { state: GameState }) {}

  render(): string {
    const s = this.game.state as GameState;
    const parts: string[] = [];
    parts.push('hud');   // a method call, not the battle helper
    return `${s.gold} gold, morale ${s.morale}, gate ${s.walls.gate.hp}`;
  }
}
