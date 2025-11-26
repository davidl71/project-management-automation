import {
  Box,
  CircularProgress,
  IconButton,
  Paper,
  Tooltip,
  Typography,
} from "@mui/material";

import InfoIcon from "@mui/icons-material/Info";

import {
  getBestOptionsForLoanDuration,
  getInterestRateBySymbol,
} from "../utils/optionsPicker";
import React from "react";
import { useAuth } from "@clerk/chrome-extension";
import dayjs from "dayjs";
import { getSettlementDate } from "../utils/date";

export interface ProposalDetailsProps {
  borrowAmount: number;
  periodInDays: number;
}

function ProposalDetails(props: ProposalDetailsProps) {
  const { borrowAmount, periodInDays } = props;
  const { isSignedIn, userId, isLoaded, getToken } = useAuth();

  const [spxContracts, setSpxContracts] = React.useState<any>({});
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    /* data structure
    {
      timestamp: ...,
      data: {...}
    } */
    chrome.storage.local.get(["spx_contracts"]).then(async (result) => {
      if (result.spx_contracts) {
        const { data, timestamp } = result.spx_contracts;
        // check if the timestamp is over 1 days old
        if (
          timestamp &&
          Date.now() - timestamp <= 24 * 60 * 60 * 1000 &&
          data
        ) {
          console.log("use cached SPX box data", result);
          setSpxContracts(data);
          setLoading(false);
          return;
        }
      }

      const token = await getToken();

      // load data from app.syntheticfi.com
      try {
        const resp = await fetch(
          "https://app.syntheticfi.com/api/chrome/contracts",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await resp.json();

        setSpxContracts(data);
        chrome.storage.local.set({
          spx_contracts: {
            timestamp: Date.now(),
            data,
          },
        });
        console.log("fetched SPX box data", data);
      } catch (error) {
        console.error(
          "Error fetching spx contracts from server; using pre-cached data",
          error
        );
      } finally {
        setLoading(false);
      }
    });
  }, [getToken]);

  if (loading) {
    return (
      <Box
        display={"flex"}
        flexDirection={"column"}
        alignItems={"center"}
        justifyContent={"center"}
      >
        <CircularProgress />
      </Box>
    );
  }

  // TODO: refactor and dedup with calculateBoxSpreadTargetSizeWithContractDate
  const optionsToUse = getBestOptionsForLoanDuration(periodInDays);
  if (optionsToUse == null) {
    console.error("No options to use");

    return (
      <Box display={"flex"} flexDirection={"column"} gap={2}>
        <Typography>
          We do not recommend borrowing for {periodInDays} days.
        </Typography>
        <Typography>
          Box spread strategies are exposed to interest rate risk and involves
          commissions and fees. We recommend borrowing between one month and one
          year.
        </Typography>
      </Box>
    );
  }

  const { symbol, date } = optionsToUse;
  const rates = getInterestRateBySymbol(symbol);
  if (rates == null) {
    console.error("No interest rate data for symbol", symbol);

    return (
      <Box display={"flex"} flexDirection={"column"} gap={2}>
        <Typography>
          Error: We do not have market data for the options we want to use.
        </Typography>
        <Typography>
          Contact us at support@syntheticfi.com for support.
        </Typography>
      </Box>
    );
  }
  const { bid, ask, mid } = rates;
  const period = Math.abs(
    dayjs(getSettlementDate(date)).diff(getSettlementDate(new Date()), "days")
  ); // loan duration

  const expDateString = dayjs(date).format("M/D/YYYY");
  const idealBoxSpreadSize = borrowAmount * Math.pow(1 + mid / 360, period);

  const boxQuantity = Math.ceil(idealBoxSpreadSize / 200000);

  var actualBoxSpreadSize: number;

  if (spxContracts[expDateString]) {
    // find box spread that is closest to the ideal size
    const strikes = spxContracts[expDateString].filter((s: number) => s > 5000); // [5000, 5050, ...]
    const boxSizeOptions = strikes.map((s: number) => 100 * (s - 5000));

    actualBoxSpreadSize = boxSizeOptions.reduce((prev: number, curr: number) =>
      Math.abs(curr - idealBoxSpreadSize / boxQuantity) <
      Math.abs(prev - idealBoxSpreadSize / boxQuantity)
        ? curr
        : prev
    );
  } else {
    // fallback if we cannot fetch from server
    console.warn("fall back to hard-coded calculation");

    // we will show strike difference of $5. In practice, it may not be possible since small strikes
    // are only available near the SPX index value.
    actualBoxSpreadSize =
      Math.floor(idealBoxSpreadSize / boxQuantity / 500) * 500;
  }

  const upfrontCash =
    (actualBoxSpreadSize / Math.pow(1 + mid / 360, period)) * boxQuantity;

  return (
    <Paper
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
        padding: 1,
        marginLeft: 1,
        marginRight: 1,
      }}
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
        <Typography>{(mid * 100).toFixed(2)}%</Typography>
      </Box>
      <Box
        display={"flex"}
        flexDirection={"row"}
        justifyContent={"space-between"}
        width={"100%"}
      >
        <Typography color={"#65727b"}>Cash released today</Typography>
        <Typography>
          {upfrontCash.toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 0,
          })}
        </Typography>
      </Box>
      <Box>
        <Typography color={"#65727b"}>
          On {date.toLocaleDateString()}, you may renew strategy, or repay{" "}
          {(actualBoxSpreadSize * boxQuantity).toLocaleString("en-US", {
            style: "currency",
            currency: "USD",
            maximumFractionDigits: 0,
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
  );
}

export default ProposalDetails;
