import { render } from "!/utils";
import { describe, it, expect } from 'vitest';
import { Cloud } from "./Cloud";

describe(Cloud, () => {
  it('should be in the document', async () => {
    const { getByText } = render(<Cloud />);

    const element = getByText(/Daredevil Deployer/i);
    expect(element).toBeInTheDocument();

  });
});

