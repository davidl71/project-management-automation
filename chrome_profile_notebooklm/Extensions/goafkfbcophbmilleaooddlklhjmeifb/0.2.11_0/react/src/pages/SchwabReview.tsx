import React from "react";
import { Box, IconButton, Paper, Tooltip, Typography } from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";

import { useSearchParams } from "react-router-dom";
import AcctDetails from "../components/AcctDetails";
import { settlementDateDuration } from "../utils/date";
import { extractSchwabMarginInfos } from "../utils/balance";
import { ExecuteTradePlaceholder } from "../components/ExecuteTradePlaceholder";

/* /schwab/review?account={accountId}&expiration={MM/DD/YYYY}&upfrontCash={number}&repaymentAmount={number} */

const schwabFees = 2.44 + 2.6;

function SchwabReview() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [schwabBalance, setSchwabBalance] = React.useState<any[]>([]);

  const accountId = searchParams.get("account");
  const expiration = searchParams.get("expiration");
  const upfrontCash = searchParams.get("upfrontCash");
  const repaymentAmount = searchParams.get("repaymentAmount");

  React.useEffect(() => {
    chrome.storage.local.get(["schwab_balance"]).then((result) => {
      setSchwabBalance(result.schwab_balance);
    });
    chrome.storage.onChanged.addListener((changes, namespace) => {
      for (let [key, { newValue }] of Object.entries(changes)) {
        if (key === "schwab_balance") {
          setSchwabBalance(newValue);
        }
      }
    });
  }, []);

  if (!accountId || !expiration || !upfrontCash || !repaymentAmount) {
    return <Typography>Error: Missing query parameters</Typography>;
  }

  const parsedUpfrontCash = parseFloat(upfrontCash);
  const upfrontCashNetOfFees = parsedUpfrontCash - schwabFees;
  const parsedRepaymentAmount = parseFloat(repaymentAmount);

  const days = settlementDateDuration(expiration);

  const interest = parsedRepaymentAmount - upfrontCashNetOfFees;

  const rate =
    (Math.pow(1 + interest / upfrontCashNetOfFees, 1 / days) - 1) * 360;

  const schwabMarginInfo = extractSchwabMarginInfos(schwabBalance);

  const relevantMarginInfo = schwabMarginInfo.find(
    (acct) => acct.accountId === accountId
  );

  return (
    <Box display={"flex"} flexWrap={"wrap"} margin={1}>
      <Typography variant={"h5"}>Review loan details</Typography>
      {relevantMarginInfo ? (
        <>
          <Paper
            key={relevantMarginInfo.accountId}
            sx={{
              width: "100%",
              border: 1,
              borderColor: "grey.500",
              borderRadius: "10px",
              padding: 1,
              marginTop: 1,
              marginBottom: 1,
            }}
          >
            <AcctDetails {...relevantMarginInfo} />
          </Paper>
        </>
      ) : (
        <></>
      )}
      <Paper
        sx={{ display: "flex", flexDirection: "column", gap: 2, padding: 1 }}
      >
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
          width={"100%"}
        >
          <Typography color={"#65727b"}>
            Estimated annualized interest rate
          </Typography>
          <Typography>{(rate * 100).toFixed(2)}%</Typography>
        </Box>
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
          width={"100%"}
        >
          <Typography color={"#65727b"}>Cash released today</Typography>
          <Typography>
            {upfrontCashNetOfFees.toLocaleString("en-US", {
              style: "currency",
              currency: "USD",
              maximumFractionDigits: 2,
            })}
          </Typography>
        </Box>
        <Box>
          <Typography color={"#65727b"}>
            On {expiration}, you may renew strategy, or repay{" "}
            {parsedRepaymentAmount.toLocaleString("en-US", {
              style: "currency",
              currency: "USD",
              maximumFractionDigits: 2,
            })}
            .
            <Tooltip
              title={
                "If not repaid or renewed, you will initiate a margin loan from Schwab and incur margin interest expenses."
              }
            >
              <IconButton size={"small"} sx={{ padding: 1 }}>
                <InfoIcon sx={{ width: "18px", height: "18px" }} />
              </IconButton>
            </Tooltip>
          </Typography>{" "}
        </Box>
      </Paper>
      <ExecuteTradePlaceholder />
    </Box>
  );
}

export default SchwabReview;
