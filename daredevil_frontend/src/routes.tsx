import type { RouteConfig } from "@react-router/dev/routes";
import App from './App';
import { Error404 } from '@/pages/error';
import { Cloud, Console, Repos } from '@/pages/cloud';
import { Login, Register } from '@/pages/user';


export default [
  {
    path: "/",
    lazy: () => import("./routes/layout").then(convert),
    Component: Layout,
    children: [
      {
        index: true,
        lazy: () => import("./routes/lobby").then(convert),
        Component: Lobby,
        children: [
          {
            path: "login",
            lazy: () => import("./routes/login").then(convert),
            Component: Login,
          },
          {
            path: "register",
            lazy: () => import("./routes/register").then(convert),
            Component: Register,
          },
        ],
      },
      {
        path: "about",
        lazy: () => import("./routes/about").then(convert),
        loader: aboutLoader,
        Component: About,
      },
      {
        path: "user",
        lazy: () => import("./routes/user").then(convert),
        Component: User,
        children: [
          {
            path: ":username",
            lazy: () => import("./routes/user/profile").then(convert),
            Component: Profile,
          },
        ],
      },
      {
        path: 'cloud',
        lazy: () => import("./routes/cloud").then(convert),
        Component: Cloud,
        children: [
          {
            path: 'console',
            lazy: () => import("./routes/cloud/console").then(convert),
            Component: Console,
          },
          {
            path: 'repos',
            lazy: () => import("./routes/cloud/repos").then(convert),
            Component: Repos,
          },
        ],
      },
    ],
  },
  {
    path: '*',
    lazy: () => import("./routes/error").then(convert),
    Component: Error404,
  },
] satisfies RouteConfig;

