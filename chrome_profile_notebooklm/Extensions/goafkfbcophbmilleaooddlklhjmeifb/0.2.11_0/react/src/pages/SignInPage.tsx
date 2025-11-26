import React from "react";

import { useSignIn } from "@clerk/chrome-extension";
import {
  Box,
  Button,
  CircularProgress,
  TextField,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

// Render the sign in form.
// Collect user's email address and send an email link with which
// they can sign in.
function SignInPage() {
  const [emailAddress, setEmailAddress] = React.useState("");
  const [expired, setExpired] = React.useState(false);
  const [askUserToCheckEmail, setAskUserToCheckEmail] = React.useState(false);

  const navigate = useNavigate();

  const { signIn, isLoaded, setActive } = useSignIn();

  if (!isLoaded || !signIn) {
    return <CircularProgress />;
  }

  const { startEmailLinkFlow } = signIn.createEmailLinkFlow();

  async function submit(e: any) {
    e.preventDefault();

    setExpired(false);
    setAskUserToCheckEmail(false);

    // Start the sign in flow, by collecting
    // the user's email address.
    const si = await signIn!.create({ identifier: emailAddress });

    // @ts-ignore
    const { emailAddressId } = si.supportedFirstFactors.find(
      (ff) => ff.strategy === "email_link" && ff.safeIdentifier === emailAddress
    );

    setAskUserToCheckEmail(true);

    // Start the email link flow.
    // Pass your app URL that users will be navigated
    // res will hold the updated sign in object.
    const res = await startEmailLinkFlow({
      emailAddressId: emailAddressId,
      redirectUrl: "https://app.syntheticfi.com/verify",
    });

    // Check the verification result.
    const verification = res.firstFactorVerification;
    if (verification.verifiedFromTheSameClient()) {
      navigate("/");
    } else if (verification.status === "expired") {
      setExpired(true);
    }

    if (res.status === "complete") {
      // Sign in is complete, we have a session.
      // Navigate to the after sign in URL.
      setActive!({
        session: res.createdSessionId,
        beforeEmit: () => navigate("/"),
      });
      return;
    }
  }

  if (expired) {
    return (
      <Box
        display={"flex"}
        flexDirection={"column"}
        margin={2}
        gap={2}
        paddingTop={"30%"}
        alignItems={"center"}
      >
        <img src="/red_cross.png" alt="email" width="80px" height="80px" />
        <Typography variant={"h6"}>Link expired</Typography>
      </Box>
    );
  }

  if (askUserToCheckEmail) {
    return (
      <Box
        display={"flex"}
        flexDirection={"column"}
        margin={2}
        gap={2}
        paddingTop={"30%"}
        alignItems={"center"}
      >
        <img src="/email_green.png" alt="email" width="80px" height="80px" />
        <Typography variant={"h6"}>Check email for login link</Typography>
      </Box>
    );
  }

  return (
    <Box
      display={"flex"}
      flexDirection={"column"}
      margin={2}
      gap={2}
      paddingTop={"30%"}
    >
      <a href="https://www.syntheticfi.com" target="_blank" rel="noreferrer">
        <img src="/SyntheticFi_with_text.png" alt="SyntheticFi" width="100%" />
      </a>
      <form onSubmit={submit}>
        <Box display={"flex"} flexDirection={"column"} gap={1}>
          <TextField
            label="Email"
            type="email"
            value={emailAddress}
            onChange={(e) => setEmailAddress(e.target.value)}
          />
          <Button type="submit" variant="contained">
            Sign in
          </Button>
        </Box>
      </form>
      <Typography color={"#65727b"}>
        Don't have an account?{" "}
        <a
          href="https://accounts.syntheticfi.com/sign-up"
          target="_blank"
          rel="noreferrer"
        >
          Sign up
        </a>
      </Typography>
    </Box>
  );
}

export default SignInPage;
