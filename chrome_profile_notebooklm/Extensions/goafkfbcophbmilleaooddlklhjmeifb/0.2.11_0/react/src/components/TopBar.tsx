import React, { useEffect } from "react";

import { Box, CircularProgress, Link, styled } from "@mui/material";

import {
  SignInButton,
  SignOutButton,
  SignedIn,
  SignedOut,
  UserButton,
  useUser,
} from "@clerk/chrome-extension";
//import { usePostHog } from "posthog-js/react";

function TopBar() {
  const { isSignedIn, user, isLoaded } = useUser();

  /*const posthog = usePostHog();

  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      posthog.reset();
    }
  }, [isLoaded, isSignedIn, posthog]);*/

  const StyledSignIn = styled(SignInButton)(({ theme }) => ({
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.common.white,
    "&:hover": {
      backgroundColor: theme.palette.primary.dark,
    },
    padding: "6px 16px",
    borderRadius: theme.shape.borderRadius,
    border: 0,
    minWidth: "64px",
    fontSize: "0.875rem",
    boxShadow:
      "0px 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0px rgba(0,0,0,0.14),0px 1px 5px 0px rgba(0,0,0,0.12)",
  }));

  const StyledSignoutButton = styled(SignOutButton)(({ theme }) => ({
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.common.white,
    "&:hover": {
      backgroundColor: theme.palette.primary.dark,
    },
    padding: "6px 16px",
    borderRadius: theme.shape.borderRadius,
    border: 0,
    minWidth: "64px",
    fontSize: "0.875rem",
    boxShadow:
      "0px 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0px rgba(0,0,0,0.14),0px 1px 5px 0px rgba(0,0,0,0.12)",
  }));

  return (
    <Box
      padding={"16px"}
      display={"flex"}
      flexDirection={"row"}
      justifyContent={"space-between"}
      height={"30px"}
      boxShadow={"0 2px 16px 0 #0000001a"}
    >
      {isLoaded ? (
        <>
          <SignedOut>
            <StyledSignIn mode="modal" />
          </SignedOut>
          <SignedIn>
            <StyledSignoutButton />
          </SignedIn>
        </>
      ) : (
        <CircularProgress />
      )}
      <Box alignContent={"center"}>
        <Link
          target="_blank"
          rel="noopener noreferrer"
          href={"https://syntheticfi.com"}
        >
          <img
            height={"30px"}
            src={chrome.runtime.getURL("SyntheticFi_with_text.png")}
            alt={"logo"}
          />
        </Link>
      </Box>
    </Box>
  );
}

export default TopBar;
