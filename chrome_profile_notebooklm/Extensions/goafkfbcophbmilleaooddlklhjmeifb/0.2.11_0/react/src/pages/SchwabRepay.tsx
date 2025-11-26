import React from "react";
import { Box, IconButton, Paper, Tooltip, Typography } from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";

import { useSearchParams } from "react-router-dom";
import AcctDetails from "../components/AcctDetails";
import { extractSchwabMarginInfos } from "../utils/balance";
import { ExecuteTradePlaceholder } from "../components/ExecuteTradePlaceholder";

/* /schwab/repay?account={accountId}&cashToRepay={number}&interestExpense={number} */

const schwabFees = 2.44 + 2.6;

function SchwabRepay() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [schwabBalance, setSchwabBalance] = React.useState<any[]>([]);

  const accountId = searchParams.get("account");
  const cashToRepay = searchParams.get("cashToRepay");
  const interestExpense = searchParams.get("interestExpense");

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

  if (!accountId || !cashToRepay || !interestExpense) {
    return <Typography>Error: Missing query parameters</Typography>;
  }

  const schwabMarginInfo = extractSchwabMarginInfos(schwabBalance);

  const relevantMarginInfo = schwabMarginInfo.find(
    (acct) => acct.accountId === accountId
  );

  var marginLoanCreated = 0;
  if (relevantMarginInfo) {
    const cash =
      relevantMarginInfo.withdrawTotal - relevantMarginInfo.withdrawMargin;
    marginLoanCreated = parseFloat(cashToRepay) + schwabFees - cash;
  }

  return (
    <Box display={"flex"} flexWrap={"wrap"} margin={1}>
      <Typography variant={"h5"}>Early repayment details</Typography>
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
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
          padding: 1,
          width: "100%",
        }}
      >
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
          width={"100%"}
        >
          <Typography color={"#65727b"}>Amount to pay off the loan</Typography>
          <Typography>
            {(parseFloat(cashToRepay) + schwabFees).toLocaleString("en-US", {
              style: "currency",
              currency: "USD",
              maximumFractionDigits: 2,
            })}
          </Typography>
        </Box>
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
          width={"100%"}
        >
          <Typography color={"#65727b"}>Total loan expenses</Typography>
          <Typography>
            {(parseFloat(interestExpense) + schwabFees).toLocaleString(
              "en-US",
              {
                style: "currency",
                currency: "USD",
                maximumFractionDigits: 2,
              }
            )}
          </Typography>
        </Box>
        {marginLoanCreated > 0 && (
          <Box
            display={"flex"}
            flexDirection={"row"}
            justifyContent={"space-between"}
            width={"100%"}
          >
            <Typography color={"#65727b"}>
              Will take out margin loan
              <Tooltip
                title={
                  "You must take out a margin loan because you don't have enough cash to repay the loan."
                }
              >
                <IconButton size={"small"}>
                  <InfoIcon sx={{ width: "18px", height: "18px" }} />
                </IconButton>
              </Tooltip>
            </Typography>
            <Typography color={"#ff465d"}>
              {marginLoanCreated.toLocaleString("en-US", {
                style: "currency",
                currency: "USD",
                maximumFractionDigits: 2,
              })}
            </Typography>
          </Box>
        )}
      </Paper>
      <ExecuteTradePlaceholder />
    </Box>
  );
}

export default SchwabRepay;
