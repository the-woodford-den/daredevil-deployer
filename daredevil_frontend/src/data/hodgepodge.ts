import { type ReactNode } from "react";

export interface WebLinks {
  id: string;
  icon?: ReactNode;
  iconClass?: string;
  text?: string;
  url?: string;
}

export interface EventItem {
  id: string;
  event: string;
}

