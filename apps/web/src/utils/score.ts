import { TrustStatus } from '../types';

export interface ScoreMeta {
  score: number;
  status: TrustStatus;
  colorHex: string;
  badgeBg: string;
  badgeText: string;
  badgeBorder: string;
  shapeSignal: string;
  iconName: 'ShieldCheck' | 'ShieldQuestion' | 'ShieldAlert' | 'AlertTriangle' | 'ShieldX';
}

export function getScoreMeta(score: number): ScoreMeta {
  if (score >= 90) {
    return {
      score,
      status: 'TRUSTED',
      colorHex: '#10B981',
      badgeBg: 'bg-emerald-500/10',
      badgeText: 'text-emerald-400',
      badgeBorder: 'border-emerald-500/30',
      shapeSignal: 'Solid ring',
      iconName: 'ShieldCheck',
    };
  } else if (score >= 70) {
    return {
      score,
      status: 'LOW RISK',
      colorHex: '#3B82F6',
      badgeBg: 'bg-blue-500/10',
      badgeText: 'text-blue-400',
      badgeBorder: 'border-blue-500/30',
      shapeSignal: 'Ring, 3/4 filled',
      iconName: 'ShieldQuestion',
    };
  } else if (score >= 50) {
    return {
      score,
      status: 'MEDIUM RISK',
      colorHex: '#F59E0B',
      badgeBg: 'bg-amber-500/10',
      badgeText: 'text-amber-400',
      badgeBorder: 'border-amber-500/30',
      shapeSignal: 'Ring, 1/2 filled',
      iconName: 'ShieldAlert',
    };
  } else if (score >= 30) {
    return {
      score,
      status: 'HIGH RISK',
      colorHex: '#F97316',
      badgeBg: 'bg-orange-500/10',
      badgeText: 'text-orange-400',
      badgeBorder: 'border-orange-500/30',
      shapeSignal: 'Ring, 1/4 filled',
      iconName: 'AlertTriangle',
    };
  } else {
    return {
      score,
      status: 'DANGEROUS',
      colorHex: '#EF4444',
      badgeBg: 'bg-red-500/10',
      badgeText: 'text-red-400',
      badgeBorder: 'border-red-500/30',
      shapeSignal: 'Near-empty ring',
      iconName: 'ShieldX',
    };
  }
}
