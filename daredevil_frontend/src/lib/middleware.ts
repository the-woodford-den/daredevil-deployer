import * as Sentry from "@sentry/react";
import { redirect } from "react-router";
import { getCurrentUser } from "@/api/users";
import { userContext } from "@/context";
import type { User } from "@/tipos/user";


export async function authMiddleware({ request, context }: { request: Request; context: Map<any, any> }) {
  // Get the full Cookie header from the incoming request to forward to backend
  const cookieHeader = request.headers.get("Cookie");

  if (!cookieHeader || !cookieHeader.includes("daredevil_token")) {
    Sentry.logger.warn("No authentication token found, redirecting to login", {
      log_source: 'lib/middleware'
    });
    throw redirect("/login");
  }

  // Forward the entire cookie header to the backend API call
  const userResult = await getCurrentUser(cookieHeader);

  const user = userResult.match(
    (user: User) => {
      Sentry.logger.info(`User authenticated: ${user.username}`, {
        log_source: 'lib/middleware'
      });
      return user;
    },
    (error) => {
      Sentry.logger.error(`Authentication failed: ${error.detail}`, {
        log_source: 'lib/middleware',
        status: error.status
      });
      return null;
    }
  );

  if (!user) {
    throw redirect("/login");
  }
  context.set(userContext, user);
}

export async function timingMiddleware(_: any, next: () => Promise<void>) {
  const start = performance.now();
  await next();
  const duration = performance.now() - start;
  console.log(`Navigation took ${duration}ms`);
}

