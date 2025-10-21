import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type AppItemResponse,
  type InstallRecordResponse
} from "@/data";

export const findInstallRecord = (username: string): ResultAsync<InstallRecordResponse, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    username: username
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/find-install-record?${params}`).then(async (response) => {
      if (!response.ok) {
        throw {
          type: 'NETWORK_ERROR', message: 'No Tokens....'
        };
      }

      const installResponse = await response.json();
      const installObject = {
        id: installResponse.id,
        account: installResponse.account,
        events: installResponse.events,
        appId: installResponse.app_id,
        appSlug: installResponse.app_slug,
        accessTokensUrl: installResponse.access_tokens_url,
        htmlUrl: installResponse.html_url,
        repositoriesUrl: installResponse.repositories_url,
      } as InstallRecordResponse;

      console.log(installObject);
      return installObject;
    }
    ),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

export const findAppItem = (slug: string): ResultAsync<AppItemResponse, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    app_slug: slug,
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/find-app-item?${params}`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'No Tokens....'
          };
        }
        const appResponse = await response.json();
        const appObject = appResponse as AppItemResponse;

        //   {
        //   id: appResponse.id,
        //   clientId: appResponse.client_id,
        //   nodeId: appResponse.node_id,
        //   owner: appResponse.owner,
        //   name: appResponse.name,
        //   description: appResponse.description,
        //   externalUrl: appResponse.external_url,
        //   htmlUrl: appResponse.html_url,
        //   createdAt: appResponse.created_at,
        //   updatedAt: appResponse.updated_at,
        //   permissions: appResponse.permissions,
        //   events: appResponse.events,
        //   token: appResponse.token,
        //   expires_at: appResponse.expires_at
        // }
        console.log(appObject);
        return appObject;
      }
      ),
    (error) => {
      if (error && typeof error === 'object' && 'type' in error) {
        return error as ApiError;
      }
      return { type: 'UNKNOWN_ERROR', message: String(error) };
    }
  );
};

