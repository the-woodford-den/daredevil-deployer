import { createSystem, defaultConfig } from "@chakra-ui/react"

export const system = createSystem(defaultConfig, {
  theme: {
    tokens: {
      fonts: {
        body: { value: "'Bricolage Grotesque', serif" },
        heading: { value: "'Bricolage Grotesque', serif" },
      },
    },
  },
})
