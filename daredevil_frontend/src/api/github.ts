import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type AppItemResponse,
  type InstallRecordResponse
} from "@/data";


// TODO Fix Routing
// Routing does not match backend
export const searchAppInstallations = (username: string): ResultAsync<InstallRecordResponse, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    username: username
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/app/installations/search?${params}`).then(async (response) => {
      if (!response.ok) {
        throw {
          type: 'NETWORK_ERROR', message: 'No Tokens....'
        };
      }

      const installResponse = await response.json();
      const installObject = installResponse as InstallRecordResponse;

      console.log(installResponse);
      return installObject;
    }),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

export const searchAppRecord = (slug: string): ResultAsync<AppItemResponse, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    slug: slug,
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/app/search?${params}`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'No Tokens....'
          };
        }
        const appResponse = await response.json();
        const appObject = appResponse as AppItemResponse;

        console.log(appResponse);
        return appObject;
      }),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

