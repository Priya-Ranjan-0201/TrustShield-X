import { getScoreMeta } from '../utils/score';

describe('getScoreMeta Utility', () => {
  it('returns TRUSTED for scores >= 90', () => {
    const meta = getScoreMeta(95);
    expect(meta.status).toBe('TRUSTED');
    expect(meta.colorHex).toBe('#10B981');
    expect(meta.iconName).toBe('ShieldCheck');
  });

  it('returns LOW RISK for scores between 70 and 89', () => {
    const meta = getScoreMeta(80);
    expect(meta.status).toBe('LOW RISK');
    expect(meta.colorHex).toBe('#3B82F6');
  });

  it('returns DANGEROUS for scores < 30', () => {
    const meta = getScoreMeta(12);
    expect(meta.status).toBe('DANGEROUS');
    expect(meta.colorHex).toBe('#EF4444');
    expect(meta.iconName).toBe('ShieldX');
  });
});
