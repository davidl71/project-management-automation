import {
  ClerkProvider,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/chrome-extension";
import { useNavigate, Routes, Route, MemoryRouter } from "react-router-dom";

import Overview from "./pages/Overview";
import "./App.css";
import TopBar from "./components/TopBar";
import SchwabBorrow from "./pages/SchwabBorrow";
import SchwabReview from "./pages/SchwabReview";
import FidelityBorrow from "./pages/FidelityBorrow";
import FidelityReview from "./pages/FidelityReview";
import SignInPage from "./pages/SignInPage";
import SchwabRepay from "./pages/SchwabRepay";
import FidelityRepay from "./pages/FidelityRepay";

const publishableKey = process.env.CLERK_PUBLISHABLE_KEY || "";

function AuthMixin(props: { children: React.ReactNode }) {
  return (
    <>
      <SignedIn>{props.children}</SignedIn>
      <SignedOut>
        <SignInPage />
      </SignedOut>
    </>
  );
}

function ClerkProviderWithRoutes() {
  const navigate = useNavigate();

  return (
    <ClerkProvider
      publishableKey={publishableKey}
      routerPush={(to) => navigate(to)}
      routerReplace={(to) => navigate(to, { replace: true })}
      syncSessionWithTab
    >
      <Routes>
        <Route
          path="/"
          element={
            <AuthMixin>
              <TopBar />
              <Overview />
            </AuthMixin>
          }
        />
        <Route
          path="/login"
          element={
            <>
              <SignedIn>
                <UserButton />
              </SignedIn>
              <SignedOut>
                <SignInPage />
              </SignedOut>
            </>
          }
        />
        <Route
          path="/schwab/borrow"
          element={
            <AuthMixin>
              <TopBar />
              <SchwabBorrow />
            </AuthMixin>
          }
        />
        <Route
          path="/fidelity/borrow"
          element={
            <AuthMixin>
              <TopBar />
              <FidelityBorrow />
            </AuthMixin>
          }
        />
        <Route
          path="/schwab/review"
          element={
            <AuthMixin>
              <TopBar />
              <SchwabReview />
            </AuthMixin>
          }
        />
        <Route
          path="/schwab/repay"
          element={
            <AuthMixin>
              <TopBar />
              <SchwabRepay />
            </AuthMixin>
          }
        />
        <Route
          path="/fidelity/repay"
          element={
            <AuthMixin>
              <TopBar />
              <FidelityRepay />
            </AuthMixin>
          }
        />
        <Route
          path="/fidelity/review"
          element={
            <AuthMixin>
              <TopBar />
              <FidelityReview />
            </AuthMixin>
          }
        />
      </Routes>
    </ClerkProvider>
  );
}

function App() {
  return (
    <MemoryRouter>
      <ClerkProviderWithRoutes />
    </MemoryRouter>
  );
}

export default App;
