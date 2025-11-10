import React from 'react';
import { ChakraProvider, defaultSystem } from "@chakra-ui/react";
import { render as rtlRender } from "@testing-library/react";
import { MemoryRouter } from 'react-router-dom';

export function render(ui: React.ReactElement) {
  return rtlRender(ui, {
    wrapper: ({ children }) => (
      <ChakraProvider value={defaultSystem}>
        <MemoryRouter>
          {children}
        </MemoryRouter>
      </ChakraProvider>
    ),
  });
};

