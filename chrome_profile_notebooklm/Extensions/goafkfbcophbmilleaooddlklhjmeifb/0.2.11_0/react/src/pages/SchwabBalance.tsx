import React from "react";

import {
  Box,
  Button,
  CircularProgress,
  Paper,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import AcctDetails from "../components/AcctDetails";
import { useAuth } from "@clerk/chrome-extension";
//import { usePostHog } from "posthog-js/react";
import { extractSchwabMarginInfos } from "../utils/balance";
import { OrderDetails } from "../integration/schwabTrade";

function SchwabBalance() {
  const navigate = useNavigate();
  const { isSignedIn, userId, isLoaded, getToken } = useAuth();
  const [schwabBalance, setSchwabBalance] = React.useState<any[]>([]);

  const [loading, setLoading] = React.useState(false);

  //const posthog = usePostHog();

  React.useEffect(() => {
    chrome.storage.local.get(["schwab_balance"]).then((result) => {
      if (result.schwab_balance) {
        setSchwabBalance(result.schwab_balance);
      }
    });
    chrome.storage.onChanged.addListener((changes, namespace) => {
      for (let [key, { newValue }] of Object.entries(changes)) {
        if (key === "schwab_balance" && newValue) {
          setSchwabBalance(newValue);
        }
      }
    });
  }, []);

  React.useEffect(() => {
    // receive review_trade event and navigate to review page
    chrome.runtime.onMessage.addListener(function (
      request,
      sender,
      sendResponse
    ) {
      /*
      {
          platform: "schwab",
          action: "review_repay",
          data: {...OrderDetails}
      }
      */
      console.log("request body", request);
      if (request.platform === "schwab" && request.action === "review_repay") {
        console.log("SyntheticFi: REVIEW TRADE");
        sendResponse({ result: "ok" });

        const data: OrderDetails = request?.data;

        const interestExpense = data.upfrontCash + data.costBasis!; // cost basis is a negative number

        navigate(
          `/schwab/repay?account=${data.accountId}&cashToRepay=${data.upfrontCash}&interestExpense=${interestExpense}`
        );
      }
    });
  }, [navigate]);

  /*React.useEffect(() => {
    if (isLoaded && isSignedIn) {
      posthog?.identify(userId);
    }
  }, [isLoaded, isSignedIn, posthog, userId]);*/

  React.useEffect(() => {
    const saveSchwabBalance = async () => {
      const token = await getToken();

      const resp = await fetch(
        "https://app.syntheticfi.com/api/chrome/balance",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            id: userId,
            platform: "schwab",
            data: schwabBalance,
          }),
        }
      );

      if (resp.ok) {
        console.log("Schwab balance saved successfully to SyntheticFi");
      } else {
        console.error("Failed to save schwab balance");
      }
    };

    if (isLoaded && isSignedIn && schwabBalance.length > 0) {
      // attempt to store the balance
      saveSchwabBalance();
    }
  }, [getToken, isLoaded, isSignedIn, schwabBalance, userId]);

  const schwabMarginInfo = extractSchwabMarginInfos(schwabBalance);

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          width: "100vw",
          position: "fixed",
          top: 0,
          left: 0,
        }}
      >
        <CircularProgress />
        <Typography>Generating order preview...</Typography>
      </Box>
    );
  }

  return (
    <Box display={"flex"} flexWrap={"wrap"} margin={1}>
      <Typography variant={"h5"}>Schwab Margin Details</Typography>
      {schwabMarginInfo.length === 0 && (
        <Box marginTop="1rem">
          <Typography variant={"h6"} color={"#65727b"}>
            To get started, log in to your Schwab account to see details
          </Typography>
        </Box>
      )}
      {schwabMarginInfo.map((info) => {
        return (
          <Paper
            key={info.accountId}
            sx={{
              width: "100%",
              padding: 1,
              marginTop: 1,
              marginBottom: 1,
            }}
          >
            <AcctDetails {...info} />
            {info.isIra ? (
              <></>
            ) : (
              <>
                {info.optionsLevel === "2" || info.optionsLevel === "3" ? (
                  <Box
                    display={"flex"}
                    flexDirection={"row"}
                    justifyContent={"space-between"}
                    width={"100%"}
                    marginTop={1}
                  >
                    <Button
                      variant={"outlined"}
                      color={"primary"}
                      sx={{ textTransform: "none" }}
                      onClick={() =>
                        navigate(`/schwab/borrow?account=${info.accountId}`)
                      }
                    >
                      Borrow with SyntheticFi
                    </Button>
                    <Button
                      variant={"outlined"}
                      color={"primary"}
                      disabled={info.boxSpreadDebitBalance <= 0}
                      sx={{ textTransform: "none" }}
                      onClick={async () => {
                        setLoading(true);

                        chrome.storage.local.set({
                          schwab_repay: {
                            expirationDate: info.boxExpirationDate,
                            quantity: info.boxQuantity,
                            strikePrice1: info.strikePrice1?.toString(),
                            strikePrice2: info.strikePrice2?.toString(),
                            accountId: info.accountId,
                            accountName: info.accountName,
                            costBasis: info.costBasis,
                          },
                        });

                        const [tab] = await chrome.tabs.query({
                          active: true,
                          currentWindow: true,
                        });

                        await chrome.tabs.sendMessage(tab.id!, {
                          platform: "schwab",
                          action: "navigate_to_trading",
                        });
                      }}
                    >
                      Repay
                    </Button>
                  </Box>
                ) : (
                  <Box
                    display={"flex"}
                    flexDirection={"column"}
                    justifyContent={"space-between"}
                    width={"100%"}
                    marginTop={1}
                    gap={1}
                  >
                    <Button
                      variant={"outlined"}
                      color={"primary"}
                      sx={{ textTransform: "none" }}
                      onClick={() =>
                        window.open(
                          "https://client.schwab.com/app/service/margin-options/#/"
                        )
                      }
                    >
                      Apply for options level 2
                    </Button>
                    <Typography color={"#65727b"}>
                      To use SyntheticFi, you must be approved for options level
                      2 or higher.
                    </Typography>
                  </Box>
                )}
              </>
            )}
          </Paper>
        );
      })}
    </Box>
  );
}

export default SchwabBalance;
