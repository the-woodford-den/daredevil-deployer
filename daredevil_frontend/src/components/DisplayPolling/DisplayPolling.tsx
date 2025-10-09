import { useEffect, useState } from 'react';
import { List } from '@chakra-ui/react';
import { LuSquirrel } from 'react-icons/lu';


const icons = {
  squirrel: <LuSquirrel />,
}

type Params = {
  clientId: string;
  indicator: string;
}

export function DisplayPolling({
  clientId,
  indicator
}: Params) {
  const [pollMessage, setPollMessage] = useState()
  const icon = icons[indicator as keyof typeof icons];
  const ws_base = import.meta.env.VITE_WS_BACKEND_URL;
  const ws_path = `/github/poll-create-token/${clientId}`;

  useEffect(() => {
    const ws = new WebSocket(`${ws_base}${ws_path}`);

    ws.addEventListener("open", () => {
      console.log("WebSocket connected");
    });

    ws.addEventListener("message", (msg) => {
      console.log("WebSocket message received:", msg.data);
      setPollMessage(msg.data);
    });

    ws.addEventListener("error", (error) => {
      console.error("WebSocket error:", error);
    });

    ws.addEventListener("close", () => {
      console.log("WebSocket closed");
    });

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [clientId])


  return (
    <List.Root gap="2" variant="marker" align="center">
      <List.Item>
        <List.Indicator asChild color="green.500">{icon}</List.Indicator>
        {pollMessage}
      </List.Item>
    </List.Root>
  );
}

