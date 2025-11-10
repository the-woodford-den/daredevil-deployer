export type ApiError =
  | { type: 'NETWORK_ERROR'; message: string }
  | { type: 'NOT_FOUND'; message: string }
  | { type: 'UNAUTHORIZED'; message: string }
  | { type: 'UNKNOWN_ERROR'; message: string };

export type ErrorState = {
  isError: boolean;
  status: undefined | number;
  detail: undefined | string;
  setError: (error: ErrorState) => void;
  unsetError: (error: ErrorState) => void;
}

