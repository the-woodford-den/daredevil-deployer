import * as Sentry from "@sentry/react";

const COOKIE_NAME = import.meta.env.VITE_COOKIE_NAME;


export function parseCookies(cookieHeader: string | null): Record<string, string> {
  if (!cookieHeader) return {};

  return cookieHeader.split(';').reduce((cookies, cookie) => {
    const [name, ...rest] = cookie.trim().split('=');
    if (name && rest.length > 0) {
      cookies[name] = rest.join('=');
    }
    return cookies;
  }, {} as Record<string, string>);
}

export function getTokenFromRequest(request: Request): string | null {
  const cookieHeader = request.headers.get("Cookie");
  const cookies = parseCookies(cookieHeader);
  const token = cookies[COOKIE_NAME];

  if (!token) {
    Sentry.logger.info("No daredevil_token cookie found", { log_source: 'lib/session' });
    return null;
  }

  return token;
}

export function createSessionCookie(token: string, maxAge: number = 86400): string {
  return `${COOKIE_NAME}=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${maxAge}`;
}

export function clearSessionCookie(): string {
  return `${COOKIE_NAME}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`;
}

