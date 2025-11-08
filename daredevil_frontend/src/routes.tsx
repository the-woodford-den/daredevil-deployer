import type { RouteConfig } from "@react-router/dev/routes";
import { About, Catch, Cloud, Layout, Lobby, User } from '@/routes';
import { Console, Repos } from '@/routes/Cloud';
import { Login, Register } from '@/routes/Lobby';
import { Profile } from '@/routes/User';


export default [
  {
    path: "/",
    file: "./routes/Layout",
    Component: Layout,
    children: [
      {
        index: true,
        file: "./routes/Lobby",
        Component: Lobby,
        children: [
          {
            path: "login",
            file: "./routes/Login",
            Component: Login,
          },
          {
            path: "register",
            file: "./routes/Register",
            Component: Register,
          },
        ],
      },
      {
        path: "about",
        file: "./routes/About",
        loader: aboutLoader,
        Component: About,
      },
      {
        path: "user",
        file: "./routes/User",
        Component: User,
        children: [
          {
            path: ":username",
            file: "./routes/User/Profile",
            Component: Profile,
          },
        ],
      },
      {
        path: 'cloud',
        file: "./routes/Cloud",
        Component: Cloud,
        children: [
          {
            path: 'console',
            file: "./routes/cloud/Console",
            Component: Console,
          },
          {
            path: 'repos',
            file: "./routes/cloud/Repos",
            Component: Repos,
          },
        ],
      },
    ],
  },
  {
    path: '*',
    file: "./routes/Catch",
    Component: Catch,
  },
] satisfies RouteConfig;

