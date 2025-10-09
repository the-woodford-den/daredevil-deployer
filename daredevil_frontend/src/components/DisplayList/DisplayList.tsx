import { List } from '@chakra-ui/react';
import { LuCircleDashed } from 'react-icons/lu';


const icons = {
  circle: <LuCircleDashed />,
}

type Params = {
  item1?: string
  item2?: string
  item3: string
  indicator: string
}

export function DisplayList({
  item1,
  item2,
  item3,
  indicator
}: Params) {

  const icon = icons[indicator as keyof typeof icons];


  return (
    <List.Root gap="2" variant="marker" align="center">
      <List.Item>
        <List.Indicator asChild color="green.500">{icon}</List.Indicator>
        <a href={`${item1}`} target="_blank">
          {item1}
        </a>
      </List.Item>
      <List.Item>
        <List.Indicator asChild color="green.500">{icon}</List.Indicator>
        {item2}
      </List.Item>
      <List.Item>
        <List.Indicator asChild color="green.500">{icon}</List.Indicator>
        {item3}
      </List.Item>
    </List.Root>
  );
}
