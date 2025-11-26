import React from "react";

import {
  Box,
  Button,
  CircularProgress,
  Paper,
  Typography,
} from "@mui/material";
import AcctDetails from "../components/AcctDetails";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@clerk/chrome-extension";
import { extractFidelityMarginInfo } from "../utils/balance";
//import { usePostHog } from "posthog-js/react";
import { OrderDetails } from "../integration/fidelityTrade";
import dayjs from "dayjs";

function convertToCSV(objArray: any, fields: any) {
  const array = Array.isArray(objArray) ? objArray : JSON.parse(objArray);

  // Map the data and convert to CSV rows using only the selected fields
  const csvRows = array.map((item: any) => {
    return fields.map((field: any) => item[field]).join(",");
  });

  // Combine headers (the selected fields) and rows
  const csvString = [fields.join(","), ...csvRows].join("\n");

  return csvString;
}

function calculateLoan(
  total: number,
  annualRate: number,
  days: number
): number {
  // Convert annual rate to daily compounding rate
  const dailyRate = Math.pow(1 + annualRate / 360, days) - 1;

  // Calculate the loan amount
  const loan = total / (1 + dailyRate);

  return loan;
}

function findClosestExpBestAsk(days: number, data: any[]) {
  return data
    .filter((item) => item.bestAsk !== 0 && item.bestAsk !== null) // Filter objects where bestAsk is not 0 or null
    .reduce((closest, item) => {
      // Find the object with daysUntilExp closest to the given number
      return Math.abs(item.daysUntilExp - days) <
        Math.abs(closest.daysUntilExp - days)
        ? item
        : closest;
    });
}

function FidelityBalance() {
  const navigate = useNavigate();
  const { isSignedIn, userId, isLoaded, getToken } = useAuth();
  const [fidelityBalance, setFidelityBalance] = React.useState<any>({});

  const [loading, setLoading] = React.useState(false);

  //const posthog = usePostHog();

  React.useEffect(() => {
    chrome.storage.local.get(["fidelity_balance"]).then((result) => {
      if (result.fidelity_balance) {
        setFidelityBalance(result.fidelity_balance);
      }
    });

    chrome.storage.onChanged.addListener((changes, namespace) => {
      for (let [key, { newValue }] of Object.entries(changes)) {
        if (key === "fidelity_balance" && newValue) {
          setFidelityBalance(newValue);
        }
      }
    });
  }, []);

  /*React.useEffect(() => {
    if (isLoaded && isSignedIn) {
      posthog?.identify(userId);
    }
  }, [isLoaded, isSignedIn, posthog, userId]);*/

  React.useEffect(() => {
    const saveFidelityBalance = async () => {
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
            platform: "fidelity",
            data: fidelityBalance,
          }),
        }
      );

      if (resp.ok) {
        console.log("Fidelity balance saved successfully to SyntheticFi");
      } else {
        console.error("Failed to save fidelity balance");
      }
    };

    if (isLoaded && isSignedIn && Object.keys(fidelityBalance).length > 0) {
      // attempt to store the balance
      saveFidelityBalance();
    }
  }, [fidelityBalance, getToken, isLoaded, isSignedIn, userId]);

  React.useEffect(() => {
    // receive review_trade event and navigate to review page
    chrome.runtime.onMessage.addListener(function (
      request,
      sender,
      sendResponse
    ) {
      /*
      {
          platform: "fidelity",
          action: "review_repay",
          data: {...OrderDetails}
      }
      */
      console.log("request body", request);
      if (
        request.platform === "fidelity" &&
        request.action === "review_repay"
      ) {
        console.log("SyntheticFi: REVIEW TRADE");
        sendResponse({ result: "ok" });

        const data: OrderDetails = request?.data;

        const interestExpense = data.upfrontCash + data.costBasis!; // cost basis is a negative number

        navigate(
          `/fidelity/repay?account=${data.accountId}&cashToRepay=${data.upfrontCash}&interestExpense=${interestExpense}`
        );
      }
    });
  }, [navigate]);

  const fidelityMarginInfo = extractFidelityMarginInfo(fidelityBalance);

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
      <Typography variant={"h5"}>Fidelity Margin Details</Typography>
      {fidelityMarginInfo.length === 0 && (
        <Box marginTop="1rem">
          <Typography variant={"h6"} color={"#65727b"}>
            To get started, log in to your Fidelity account to see details
          </Typography>
        </Box>
      )}
      {fidelityMarginInfo.map((info) => {
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
                    navigate(`/fidelity/borrow?account=${info.accountId}`)
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
                      fidelity_repay: {
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
                      platform: "fidelity",
                      action: "navigate_to_trading",
                    });
                  }}
                >
                  Repay
                </Button>
                <Button
                  variant={"outlined"}
                  color={"primary"}
                  disabled={info.boxSpreadDebitBalance <= 0}
                  sx={{ textTransform: "none" }}
                  onClick={async () => {
                    /*
                    [
                      {
                        "date": "10/31/2024",
                        "daysUntilSettlement": 18,
                        "daysUntilExp": 20,
                        "bestBid": 0.10984154925283818,
                        "bestAsk": 0
                      },
                      {
                        "date": "11/1/2024",
                        "daysUntilSettlement": 21,
                        "daysUntilExp": 21,
                        "bestBid": 0.1723327066178637,
                        "bestAsk": 0
                      }
                    ]
                    */
                    var bestRatesByDate: any;

                    try {
                      const resp = await fetch(
                        "https://app.syntheticfi.com/api/cob/rates",
                        {
                          headers: {
                            "Content-Type": "application/json",
                          },
                        }
                      );

                      const data = await resp.json();

                      bestRatesByDate = data.data;

                      console.log("fetched SPX box data", data);
                    } catch (error) {
                      console.error(
                        "Error fetching spx contracts from server; using pre-cached data",
                        error
                      );
                    } finally {
                      setLoading(false);
                    }

                    // Fields to include in CSV
                    const fields = [
                      "expirationDate",
                      "amountToPayAtExpiration",
                      "cashReceivedAtTradeOpen",
                      "quantity",
                      "strikePrice1",
                      "strikePrice2",
                      "interestChargesUntilExpiration",
                      "markToMarketValue",
                      "interestChargesAccurred",
                    ];

                    /*
                    {
                      "expirationDate": "AUG 30, 2024",
                      "boxSize": 50000,
                      "costBasisSum": -10000,
                      "quantity": 1,
                      "strikePrice1": 5000,
                      "strikePrice2": 5500,
                    }*/

                    const normalizedBoxGroups = info.allBoxGroups.map(
                      (boxGroup: any) => {
                        const targetDate = dayjs("AUG 30 2024", "MMM DD YYYY");

                        // Get today's date
                        const today = dayjs();

                        // Calculate the difference in days
                        const differenceInDays = Math.abs(
                          targetDate.diff(today, "day")
                        );

                        const bestAsk = findClosestExpBestAsk(
                          differenceInDays,
                          bestRatesByDate
                        )?.bestAsk;

                        var markToMarket: any;
                        if (bestAsk) {
                          markToMarket = calculateLoan(
                            boxGroup.boxSize,
                            bestAsk,
                            differenceInDays
                          );
                        } else {
                          markToMarket = -1;
                        }

                        return {
                          expirationDate: boxGroup.expirationDate.replace(
                            ",",
                            ""
                          ),
                          amountToPayAtExpiration: boxGroup.boxSize,
                          cashReceivedAtTradeOpen: -boxGroup.costBasisSum,
                          quantity: boxGroup.quantity,
                          strikePrice1: boxGroup.strikePrice1,
                          strikePrice2: boxGroup.strikePrice2,
                          interestChargesUntilExpiration:
                            boxGroup.costBasisSum + boxGroup.boxSize,
                          markToMarketValue: markToMarket,
                          interestChargesAccurred:
                            markToMarket === -1
                              ? -1
                              : markToMarket + boxGroup.costBasisSum,
                        };
                      }
                    );

                    const content = convertToCSV(normalizedBoxGroups, fields);

                    // Create a Blob with the content as plain text
                    const blob = new Blob([content], { type: "text/plain" });
                    const link = document.createElement("a");
                    link.href = URL.createObjectURL(blob);
                    link.download = "analysis.csv";

                    document.body.appendChild(link);

                    link.click();

                    document.body.removeChild(link);
                  }}
                >
                  Analyze
                </Button>
              </Box>
            )}
          </Paper>
        );
      })}
    </Box>
  );
}

export default FidelityBalance;
