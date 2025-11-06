import { render } from "!/utils";
import { describe, it, expect } from 'vitest';
import { Lobby } from "./Lobby";

describe(Lobby, () => {
  it('should be in the document', async () => {
    const { getByText } = render(<Lobby />);

    const element = getByText(/Daredevil Deployer/i);
    expect(element).toBeInTheDocument();

  });
});


{/* <GridItem colSpan={4} pt="3"> */ }
{/*   <Flex direction="column"> */ }
{/*     <Box */ }
{/*       p="4" */ }
{/*       w="100%" */ }
{/*       _hover={{ bg: "var(--chakra-colors-fg-muted)", color: "black" }} */ }
{/*     > */ }
{/*       <Flex align="center" justify="center" gap="16"> */ }
{/*         <Text textStyle="4xl">Welcome Welcome Welcome</Text> */ }
{/*         <Code>FastAPI, React.js, Github API</Code> */ }
{/*       </Flex> */ }
{/*     </Box> */ }
{/*   </Flex> */ }
{/* </GridItem> */ }

