import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DNS,
  sendDefaultPii: true
});

export { Sentry };

