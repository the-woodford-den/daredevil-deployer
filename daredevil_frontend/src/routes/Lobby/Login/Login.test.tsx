import { render } from "!/utils";
import { describe, it, expect } from 'vitest';
import { Login } from "./Login";

describe(Login, () => {
  it('should be in the document', async () => {
    const { getByText } = render(<Login />);

    const element = getByText(/Daredevil Login/i);
    expect(element).toBeInTheDocument();
  });
});

