import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Input } from '../components/ui/Input';

describe('Input Component', () => {
  it('renders label and handles typing', async () => {
    render(<Input label="Email Address" placeholder="Enter email" />);

    const input = screen.getByPlaceholderText('Enter email');
    expect(input).toBeInTheDocument();

    await userEvent.type(input, 'test@truthshield.gov.in');
    expect(input).toHaveValue('test@truthshield.gov.in');
  });

  it('renders error message when error prop is passed', () => {
    render(<Input label="Password" error="Password must be at least 10 characters." />);

    expect(screen.getByText('Password must be at least 10 characters.')).toBeInTheDocument();
  });
});
