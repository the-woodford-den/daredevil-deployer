import type { Config } from "@react-router/dev/config";

export default {
  appDirectory: "./src",
  buildDirectory: "build",
  future: {
    v8_middleware: true,
  },
  ssr: true,
  prerender: ["/", "/login", "/register"],
} satisfies Config;

