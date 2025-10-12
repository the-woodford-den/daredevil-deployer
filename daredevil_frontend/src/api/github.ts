import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type GithubAppResponse,
  type GithubTokenResponse,
  type GithubInstallResponse
} from "@/data";

export const getInstallation = (username: string): ResultAsync<GithubInstallResponse, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    username: username
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/find-install-id?${params}`).then(async (response) => {
      if (!response.ok) {
        throw {
          type: 'NETWORK_ERROR', message: 'No Tokens....'
        };
      }

      const installResponse = await response.json();
      const installObject = {
        account: installResponse.account,
        events: installResponse.events,
        appId: installResponse.app_id,
        appSlug: installResponse.app_slug,
        accessTokensUrl: installResponse.access_tokens_url,
        htmlUrl: installResponse.html_url,
        repositoriesUrl: installResponse.repositories_url,
      } as GithubInstallResponse;

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

export const getAnApp = (slug: string): ResultAsync<GithubAppResponse, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    app_slug: slug,
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/get-an-app?${params}`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'No Tokens....'
          };
        }
        const appResponse = await response.json();
        const appObject = {
          id: appResponse.id,
          clientId: appResponse.client_id,
          nodeId: appResponse.node_id,
          owner: appResponse.owner,
          name: appResponse.name,
          description: appResponse.description,
          externalUrl: appResponse.external_url,
          htmlUrl: appResponse.html_url,
          createdAt: appResponse.created_at,
          updatedAt: appResponse.updated_at,
          permissions: appResponse.permissions,
          events: appResponse.events,
          token: appResponse.token,
          expires_at: appResponse.expires_at
        } as GithubAppResponse;

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

