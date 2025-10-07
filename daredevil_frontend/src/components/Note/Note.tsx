import type { PropsWithChildren } from 'react';
import { FaBeer, FaRaspberryPi, FaLemon } from 'react-icons/fa';
import { GiMetroid, GiCapybara, GiRam } from 'react-icons/gi';
import reactUrl from '~/react.svg';
import rubyUrl from '~/ruby.svg';
import docsUrl from '~/documentation.svg';
import designUrl from '~/design.svg';
import megaUrl from '~/mega.png';
import {
  Avatar,
  Card,
  Flex,
  HStack,
  IconButton,
  Strong,
  Text
} from '@chakra-ui/react';


const icons = {
  capybara: <GiCapybara />,
  metroid: <GiMetroid />,
  ram: <GiRam />,
  beer: <FaBeer />,
  raspPi: <FaRaspberryPi />,
  lemon: <FaLemon />,
};

const aHash = {
  mega: { url: megaUrl, fBack: "MegaMan" },
  ruby: { url: rubyUrl, fBack: "RubyGem" },
  docs: { url: docsUrl, fBack: "Documents" },
  react: { url: reactUrl, fBack: "ReactSphere" },
  design: { url: designUrl, fBack: "DesignSystem" }
};

type Params = {
  avatar: string;
  title: string;
  button?: string;
  footer?: string;
} & PropsWithChildren

export function Note({
  avatar,
  title,
  button,
  footer,
  children
}: Params) {

  return (
    <Card.Root size="lg">
      <Card.Body gap="4" w="full">
        <HStack mb="4" gap="6">
          <Avatar.Root size="lg" shape="full">
            <Avatar.Image
              src={aHash[avatar as keyof typeof aHash].url}
            />
            <Avatar.Fallback
              name={aHash[avatar as keyof typeof aHash].fBack}
            />
          </Avatar.Root>
          <Card.Title>
            <Text fontWeight="semibold" textStyle="lg">
              {title}
            </Text>
          </Card.Title>
        </HStack>
        <HStack mb="6" gap="6">
          {button &&
            <IconButton
              aria-label={button as string}
              variant="outline"
              size="lg"
            >
              {icons[button as keyof typeof icons]}
            </IconButton>
          }
          {children}
        </HStack>
        {footer &&
          <Card.Footer unstyled={true}>
            <Flex align="center" justify="center">
              <Strong textStyle="sm">{footer}</Strong>
            </Flex>
          </Card.Footer>
        }
      </Card.Body>
    </Card.Root>
  );
}

