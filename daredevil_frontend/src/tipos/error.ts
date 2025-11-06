export type ApiError =
  | { type: 'NETWORK_ERROR'; message: string }
  | { type: 'NOT_FOUND'; message: string }
  | { type: 'UNAUTHORIZED'; message: string }
  | { type: 'UNKNOWN_ERROR'; message: string };

