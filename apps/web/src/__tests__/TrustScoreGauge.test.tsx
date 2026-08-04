import React from 'react';
import { render, screen } from '@testing-library/react';
import { TrustScoreGauge } from '../components/common/TrustScoreGauge';

describe('TrustScoreGauge Component', () => {
  it('renders score value and accessible role/aria-label', () => {
    render(<TrustScoreGauge score={94} status="TRUSTED" />);

    const gaugeImg = screen.getByRole('img', {
      name: /Trust score 94 out of 100, status TRUSTED/i,
    });
    expect(gaugeImg).toBeInTheDocument();
    expect(screen.getByText('94')).toBeInTheDocument();
    expect(screen.getByText('TRUSTED')).toBeInTheDocument();
  });

  it('renders dangerous score tier correctly', () => {
    render(<TrustScoreGauge score={15} status="DANGEROUS" />);

    expect(screen.getByText('15')).toBeInTheDocument();
    expect(screen.getByText('DANGEROUS')).toBeInTheDocument();
  });
});
