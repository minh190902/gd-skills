import { buy } from './shop';
export function testBuy(S: any) { S.gold = 99; buy(S, 1); }
