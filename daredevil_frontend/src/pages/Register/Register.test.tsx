import { render } from "!/utils";
import { describe, it, expect } from 'vitest';
import { Register } from "./Register";

describe(Register, () => {
  it('should be in the document', async () => {
    const { getByText } = render(<Register />);

    const element = getByText(/Create Daredevil User/i);
    expect(element).toBeInTheDocument();
  });
});

