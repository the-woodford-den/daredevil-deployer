import { createContext } from "react";
import type { User } from '@/tipos/user';

export const userContext = createContext<User | null>(null);

