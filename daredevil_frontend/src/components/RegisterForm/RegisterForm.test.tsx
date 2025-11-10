import { render } from '!/utils';
import { describe, it, expect } from 'vitest';
import { RegisterForm } from './RegisterForm';

describe(RegisterForm, () => {
  it('has two inputs with two labels', async () => {
    const { getByText } = render(<RegisterForm />);

    const label1 = getByText(/github username/i);
    const label2 = getByText(/daredevil password/i);

    expect(label1).toBeInTheDocument();
    expect(label2).toBeInTheDocument();
  });
});

