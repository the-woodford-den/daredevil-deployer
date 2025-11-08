import underUrl from '~/underline.svg';
import {
  Heading,
  Mark,
  Separator,
} from '@chakra-ui/react';

export function Repos() {
  return (
    <Heading size="2xl" maxW="20ch">
      <Separator />
      <Mark
        key={"index"}
        css={{
          fontStyle: "italic",
          color: "red.500",
          position: "relative",
        }}
      >
        <img
          style={{ position: "absolute", left: 0 }}
          src={underUrl}
          loading="lazy"
          alt=""
        />
      </Mark>
      <Separator />
    </Heading>
  );
}



