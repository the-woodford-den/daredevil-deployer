import React from "react";
import ReactDOM from "react-dom/client";
import { HydratedRouter } from "react-router-dom";
import { Sentry } from "config";


function convert(m: any) {
  let {
    clientLoader,
    clientAction,
    default: Component,
    ...rest
  } as m;
  return {
    ...rest,
    loader: clientLoader,
    action: clientAction,
    Component,
  };
}


ReactDOM.hydrateRoot(
  document,
  <React.StrictMode>
    <HydratedRouter />
  </React.StrictMode>
);

// const onUncaughtError: Sentry.reactErrorHandler((error, errorInfo) => {
//   console.warn('Uncaught error', error, errorInfo.componentStack);
// }),
// onCaughtError: Sentry.reactErrorHandler(),
// onRecoverableError: Sentry.reactErrorHandler(),

