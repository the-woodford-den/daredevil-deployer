import { ResultAsync } from "neverthrow";
import {
  type ApiError,
  type GithubApp
} from "@/data";

export const getGithubApp = (appSlug: string): ResultAsync<GithubApp, ApiError> => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const params = new URLSearchParams({
    app_slug: appSlug
  });

  return ResultAsync.fromPromise(
    fetch(`${backendUrl}/github/get-app?${params}`)
      .then(async (response) => {
        if (!response.ok) {
          throw {
            type: 'NETWORK_ERROR', message: 'No Github App Found....'
          };
        }
        const ghAppResponse = await response.json();
        const appObject = {
          id: ghAppResponse.id,
          slug: ghAppResponse.slug,
          nodeId: ghAppResponse.node_id,
          clientId: ghAppResponse.client_id,
          name: ghAppResponse.name,
          externalUrl: ghAppResponse.external_url,
          htmlUrl: ghAppResponse.html_url,
          createdAt: ghAppResponse.created_at,
          updatedAt: ghAppResponse.updated_at,
          githubAppId: ghAppResponse.github_app_id
        } as GithubApp;
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
