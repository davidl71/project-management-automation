import React from "react";

import {
  SignedIn,
  SignedOut,
  SignIn,
  SignUp,
  ClerkProvider,
  SignOutButton,
} from "@clerk/chrome-extension";
import { useNavigate, Routes, Route, MemoryRouter } from "react-router-dom";

const publishableKey = process.env.CLERK_PUBLISHABLE_KEY || "";

function ClerkProviderWithRoutes() {
  const navigate = useNavigate();

  return (
    <ClerkProvider
      publishableKey={publishableKey}
      routerPush={(to) => navigate(to)}
      routerReplace={(to) => navigate(to, { replace: true })}
    >
      <Routes>
        <Route
          path="/"
          element={
            <>
              <SignIn
                forceRedirectUrl={chrome.runtime.getURL(
                  "react/dist/index.html"
                )}
              />
              <SignOutButton />
            </>
          }
        />
      </Routes>
    </ClerkProvider>
  );
}

function LoginApp() {
  return (
    <MemoryRouter>
      <ClerkProviderWithRoutes />
    </MemoryRouter>
  );
}

export default LoginApp;
