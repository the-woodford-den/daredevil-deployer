import { type RouteConfig } from "@react-router/dev/routes";
import { flatRoutes } from "@react-router/fs-routes";

export default flatRoutes({
  rootDirectory: "pages/",
}) satisfies RouteConfig;

//
// import {
//   type RouteConfig,
//   route,
//   index,
//   layout
// } from "@react-router/dev/routes";
//
// export default [
//   layout("./routes/Layout", [
//     index("./routes/Lobby"),
//     route("login", "./routes/Lobby/Login"),
//     route("register", "./routes/Lobby/Register"),
//     route("about", "./routes/About"),
//     route("user", "./routes/User", [
//       route(":username", "./routes/User/Profile"),
//     ]),
//     route("cloud", "./routes/Cloud", [
//       route("console", "./routes/Cloud/Console"),
//       route("repos", "./routes/Cloud/Repos"),
//     ]),
//   ]),
//   route("*", "./routes/Catch"),
// ] satisfies RouteConfig;
//
