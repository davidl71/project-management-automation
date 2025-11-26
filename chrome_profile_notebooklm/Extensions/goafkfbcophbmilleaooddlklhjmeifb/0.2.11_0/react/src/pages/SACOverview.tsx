import React from "react";

import RefreshIcon from "@mui/icons-material/Refresh";
import {
  Box,
  Button,
  CircularProgress,
  FormControl,
  IconButton,
  InputLabel,
  LinearProgress,
  MenuItem,
  Paper,
  Select,
  setRef,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@clerk/chrome-extension";
import OrderDetails from "../components/OrderDetails";
import CurrencyInput from "react-currency-input-field";
import ProposalDetails from "../components/ProposalDetails";
import {
  calculatePrice,
  differenceInDays,
  getBestOptionsForLoanDuration,
} from "../utils/optionsPicker";
import dayjs from "dayjs";
import { calculateBoxSpreadTargetSize } from "../utils/contentScript";
import { getStrikePriceTargets } from "../utils/strikePricePicker";
import { settlementDateDuration } from "../utils/date";
import { DateOptions } from "../components/DateOptions";

// For Schwab Advisor Center

function SACOverview() {
  const { isSignedIn, userId, isLoaded, getToken } = useAuth();

  //const [loading, setLoading] = React.useState(false);

  const [orderStatus, setOrderStatus] = React.useState<any>(null);

  const [account, setAccount] = React.useState("");
  const [firm, setFirm] = React.useState("");

  // Example: {first_name: 'Natanel', last_name: 'Malkoukian', account_number: '9058-9413', advisor: 'ablewealth.co'}
  const [pgAccounts, setPgAccounts] = React.useState<any[]>([]);

  const [borrowAmount, setBorrowAmount] = React.useState<number | null>(null);

  const [periodInDays, setPeriodInDays] = React.useState<number | null>(null);

  const [orderLoadingIds, setOrderLoadingIds] = React.useState<number[]>([]);

  const [refreshing, setRefreshing] = React.useState(false);

  React.useEffect(() => {
    chrome.storage.local.get(["sac_order_status"]).then((result) => {
      setOrderStatus(result.sac_order_status);
      setOrderLoadingIds([]);
      setRefreshing(false);
    });
    chrome.storage.onChanged.addListener((changes, namespace) => {
      for (let [key, { newValue }] of Object.entries(changes)) {
        if (key === "sac_order_status") {
          setOrderStatus(newValue);
          setOrderLoadingIds([]);
          setRefreshing(false);
        }
      }
    });
  }, []);

  React.useEffect(() => {
    const fetchAccount = async () => {
      if (isLoaded && isSignedIn) {
        // attempt to store the balance
        const token = await getToken();

        if (token) {
          const resp = await fetch(
            "https://app.syntheticfi.com/api/advisor/accounts",
            {
              method: "GET",
              cache: "no-cache",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            }
          );

          if (resp.ok) {
            const data = await resp.json();

            console.log("accounts", data);

            setPgAccounts(data.data);
          } else {
            console.error(`Failed to load accounts from Postgresql`);
            throw new Error("Failed to load accounts");
          }
        }
      }
    };

    fetchAccount();
  }, [isSignedIn, isLoaded, userId, getToken]);

  const advisors = pgAccounts
    .map(function (account) {
      return account.advisor;
    })
    .filter(function (advisor, index, self) {
      return self.indexOf(advisor) === index;
    });

  const orders = orderStatus?.Orders ? orderStatus.Orders : [];

  // box spread orders are 4 entries with the same LinkId. We want to group them together.
  const groupedOrders = orders
    .filter((o: any) => o.LinkId !== null)
    .reduce((acc: any, order: any) => {
      // acc is a map from LinkId to an array of orders
      const linkId = order.LinkId;

      if (!acc[linkId]) {
        acc[linkId] = [];
      }

      acc[linkId].push(order);

      return acc;
    }, {});

  const fourLegOrders = Object.values(groupedOrders).filter(
    (group: any) => group.length === 4
  );

  // TODO: we treat each of them as a box. not sure if this is the best idea
  const boxSpreadOrders = fourLegOrders.map((group: any) => {
    // limit price can be found from each leg
    const limitPrice = parseFloat(group[0].LimitPrice);

    const status = group[0].Status;

    var quantity;

    if (status === "Filled") {
      quantity = parseInt(group[0].Quantity.replace(" cts", ""));
    } else {
      quantity = parseInt(group[0].LeavesQuantity);
    }

    // grab 5000.00 from "SPX 09/20/2024 5000.00 P"
    const strikePrices = group.map((order: any) =>
      parseFloat(order.Symbol.split(" ")[2])
    );

    const strikePrice1 = Math.min(...strikePrices);
    const strikePrice2 = Math.max(...strikePrices);

    const expDate = group[0].Symbol.split(" ")[1] as string; // MM/DD/YYYY

    const accountId = group[0].AccountId.replace("-", "");
    const shortOrderId = group[0].OrderId;
    const expandedOrderId = group[0].OrderId;

    return {
      limitPrice,
      quantity,
      strikePrice1,
      strikePrice2,
      expDate,
      accountId,
      shortOrderId,
      expandedOrderId,
      status,
    };
  });

  /*if (loading) {
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
  }*/

  const refreshOrderStatus = async () => {
    setRefreshing(true);

    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    await chrome.tabs.sendMessage(tab.id!, {
      platform: "sac",
      action: "refresh_order_status",
    });
  };

  const placeOrder = async () => {
    const optionsToUse = getBestOptionsForLoanDuration(periodInDays!);
    if (optionsToUse == null) {
      console.error("No options to use");
      return;
    }

    const { symbol, date } = optionsToUse;

    const formattedDate = dayjs(date).format("MM/DD/YYYY");

    const boxSizeTarget = await calculateBoxSpreadTargetSize(
      borrowAmount!,
      periodInDays!
    );

    const { quantity, strikePrice2Target, strikePrice1 } =
      getStrikePriceTargets(boxSizeTarget);

    // round strikePrice2Target to the nearest 5
    const strikePrice2 = Math.round(strikePrice2Target / 5) * 5;

    console.log("strikePrice2 calculations:", strikePrice2Target, strikePrice2);

    const today = new Date();
    today.setDate(today.getDate() + periodInDays!);

    const limitPrice = calculatePrice(
      periodInDays!,
      strikePrice2 - strikePrice1,

      settlementDateDuration(formattedDate)
    );

    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    await chrome.tabs.sendMessage(tab.id!, {
      platform: "sac",
      action: "trade",
      data: {
        accountId: account,
        expDate: formattedDate,
        strike1: strikePrice1,
        strike2: strikePrice2,
        limitPrice: limitPrice,
        quantity: quantity,
      },
    });

    await new Promise((resolve) => setTimeout(resolve, 2000));
    await refreshOrderStatus();
  };

  const cancelOrder = async (orderToBeChanged: any) => {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    console.log("send order cancel", {
      accountId: orderToBeChanged.accountId,
      orderId: orderToBeChanged.shortOrderId,
      expandedOrderId: orderToBeChanged.expandedOrderId,
    });

    await chrome.tabs.sendMessage(tab.id!, {
      platform: "sac",
      action: "cancel_order",
      data: {
        accountId: orderToBeChanged.accountId,
        orderId: orderToBeChanged.shortOrderId,
        expandedOrderId: orderToBeChanged.expandedOrderId,
      },
    });

    // wait 1 second for the order cancel to process
    await new Promise((resolve) => setTimeout(resolve, 1000));
    await refreshOrderStatus();
  };

  const decreseCreditAmountPerTick = async (orderToBeChanged: any) => {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    const cancelOrderResp = await chrome.tabs.sendMessage(tab.id!, {
      platform: "sac",
      action: "cancel_order",
      data: {
        accountId: orderToBeChanged.accountId,
        orderId: orderToBeChanged.shortOrderId,
        expandedOrderId: orderToBeChanged.expandedOrderId,
      },
    });

    if (
      cancelOrderResp?.resp
        ?.SucessOrders /* this is a typo in the Schwab system */ === 1 &&
      cancelOrderResp?.resp?.FailureOrders === 0
    ) {
      // wait 1 second for the order cancel to process
      await new Promise((resolve) => setTimeout(resolve, 1000));

      await chrome.tabs.sendMessage(tab.id!, {
        platform: "sac",
        action: "trade",
        data: {
          accountId: orderToBeChanged.accountId,
          expDate: orderToBeChanged.expDate,
          strike1: orderToBeChanged.strikePrice1,
          strike2: orderToBeChanged.strikePrice2,
          limitPrice: orderToBeChanged.limitPrice - 0.05, // TODO: remove magic number
          quantity: orderToBeChanged.quantity,
        },
      });

      await new Promise((resolve) => setTimeout(resolve, 1000));
    } else {
      console.error(
        "Failed to cancel order. Is it filled or already cancelled?"
      );
      console.error("Cancel order response", cancelOrderResp);
    }

    await refreshOrderStatus();
  };

  const decreseCreditAmountPerBp = async (orderToBeChanged: any) => {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    const cancelOrderResp = await chrome.tabs.sendMessage(tab.id!, {
      platform: "sac",
      action: "cancel_order",
      data: {
        accountId: orderToBeChanged.accountId,
        orderId: orderToBeChanged.shortOrderId,
        expandedOrderId: orderToBeChanged.expandedOrderId,
      },
    });

    if (
      cancelOrderResp?.resp
        ?.SucessOrders /* this is a typo in the Schwab system */ === 1 &&
      cancelOrderResp?.resp?.FailureOrders === 0
    ) {
      // wait 1 second for the order cancel to process
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const repayAmount = Math.abs(
        (orderToBeChanged.strikePrice2 - orderToBeChanged.strikePrice1) * 100
      );
      const creditAmount = orderToBeChanged.limitPrice * 100;

      const expDate = dayjs(orderToBeChanged.expDate, "MM/DD/YYYY");
      const dateDifference = Math.abs(
        differenceInDays(new Date(), expDate.toDate())
      );

      const currentInterestRate =
        (Math.pow(
          1 + (repayAmount - creditAmount) / creditAmount,
          1 / dateDifference
        ) -
          1) *
        360;

      const newRate = currentInterestRate + 0.0001; // 1bps

      // calculate new limit price
      const newLimitPrice =
        repayAmount / Math.pow(1 + newRate / 360, dateDifference) / 100;

      // round up to the nearest 0.05
      const roundedLimitPrice = Math.ceil(newLimitPrice * 20) / 20;

      const newOrderPrice = Math.min(
        roundedLimitPrice,
        orderToBeChanged.limitPrice - 0.05
      );

      await chrome.tabs.sendMessage(tab.id!, {
        platform: "sac",
        action: "trade",
        data: {
          accountId: orderToBeChanged.accountId,
          expDate: orderToBeChanged.expDate,
          strike1: orderToBeChanged.strikePrice1,
          strike2: orderToBeChanged.strikePrice2,
          limitPrice: newOrderPrice,
          quantity: orderToBeChanged.quantity,
        },
      });

      await new Promise((resolve) => setTimeout(resolve, 1000));
    } else {
      console.error(
        "Failed to cancel order. Is it filled or already cancelled?"
      );
      console.error("Cancel order response", cancelOrderResp);
    }

    await refreshOrderStatus();
  };

  const today = dayjs().startOf("day");
  const minDate = today.add(15, "day");
  const maxDate = today.add(7, "year");

  return (
    <Box
      display={"flex"}
      flexWrap={"wrap"}
      flexDirection={"column"}
      margin={1}
      paddingRight={"20px"}
      boxSizing={"border-box"}
      gap={1}
      maxWidth={"100%"}
    >
      <Typography variant={"h5"}>Schwab Advisor Center</Typography>
      <FormControl fullWidth>
        <InputLabel>Firm</InputLabel>
        <Select
          value={firm}
          label="Firm"
          onChange={(event) => {
            console.log("value", event.target.value);
            setFirm(event.target.value as string);
          }}
        >
          <MenuItem value={"syntheticfi"}>SyntheticFi Internal</MenuItem>
          {advisors.map((advisor) => (
            <MenuItem value={advisor}>{advisor}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl fullWidth>
        <InputLabel>Account</InputLabel>
        <Select
          value={account}
          label="Account"
          onChange={(event) => {
            console.log("value", event.target.value);
            setAccount(event.target.value);
          }}
        >
          {pgAccounts
            .filter((account) => account.advisor === firm)
            .map((account) => (
              <MenuItem value={account.account_number.replace("-", "")}>
                {account.account_number} {account.first_name}{" "}
                {account.last_name}
              </MenuItem>
            ))}
          {firm === "syntheticfi" && (
            <MenuItem value={"95634901"}>9563-4901 YUCHENG YANG TTEE</MenuItem>
          )}
          {firm === "syntheticfi" && (
            <MenuItem value={"59629588"}>5962-9588 YUCHENG YANG</MenuItem>
          )}
          {firm === "syntheticfi" && (
            <MenuItem value={"35715277"}>
              3571-5277 Converge Fashion LLC
            </MenuItem>
          )}

          {firm === "syntheticfi" && (
            <MenuItem value={"37281067"}>
              3728-1067 Converge Fashion LLC
            </MenuItem>
          )}
          {firm === "syntheticfi" && (
            <MenuItem value={"08768959"}>
              0876-8959 Main SL Master (Block Trade)
            </MenuItem>
          )}
          {firm === "syntheticfi" && (
            <MenuItem value={"08793808"}>
              0879-3808 Main IA Master (Block Trade)
            </MenuItem>
          )}
          {firm === "syntheticfi" && (
            <MenuItem value={"79864709"}>7986-4709 JOHN SCHLICHTING</MenuItem>
          )}
        </Select>
        <Box display="flex" flexDirection="column" marginTop={1}>
          <Typography>Amount to borrow</Typography>
          <CurrencyInput
            name="borrowAmount"
            prefix="$"
            decimalsLimit={2}
            placeholder="$100,000"
            value={borrowAmount ? borrowAmount.toString() : undefined}
            onValueChange={(value, name) => {
              value
                ? setBorrowAmount(parseFloat(value))
                : setBorrowAmount(null);
            }}
            allowNegativeValue={false}
            style={{
              border: "1px solid #ced4da",
              padding: "16.5px 0px 16.5px 14px",
              borderRadius: "4px",
              fontSize: "16px",
            }}
          />
        </Box>
      </FormControl>
      <FormControl fullWidth>
        <Typography>Expected payback date</Typography>
        <DateOptions
          periodInDays={periodInDays ? periodInDays : undefined}
          setPeriodInDays={(periodInDays: number) => {
            setPeriodInDays(periodInDays);
          }}
          minDate={minDate}
          maxDate={maxDate}
        />
      </FormControl>
      {borrowAmount && periodInDays && (
        <ProposalDetails
          borrowAmount={borrowAmount}
          periodInDays={periodInDays}
        />
      )}
      <Button
        variant="contained"
        onClick={placeOrder}
        disabled={!account || !firm}
      >
        Place order
      </Button>
      <Box
        display={"flex"}
        flexDirection={"row"}
        justifyContent={"space-between"}
        marginTop={2}
      >
        <Typography variant={"h6"}>Open orders</Typography>
        {refreshing ? (
          <CircularProgress />
        ) : (
          <IconButton onClick={refreshOrderStatus}>
            <RefreshIcon />
          </IconButton>
        )}
      </Box>

      {boxSpreadOrders
        .sort((a, b) => {
          if (b.status.localeCompare(a.status) === 0) {
            // break tie with account ID
            return a.accountId.localeCompare(a.accountId);
          } else {
            return b.status.localeCompare(a.status);
          }
        })
        .map((order: any, index: number) => (
          <Paper
            key={index}
            sx={{
              width: "100%",
              padding: 1,
              marginTop: 1,
              marginBottom: 1,
            }}
          >
            <OrderDetails
              key={index}
              {...order}
              decreasePriceCallbackByTick={async () => {
                setOrderLoadingIds([...orderLoadingIds, order.shortOrderId]);
                await decreseCreditAmountPerTick(order);
              }}
              decreasePriceByBpCallback={async () => {
                setOrderLoadingIds([...orderLoadingIds, order.shortOrderId]);
                await decreseCreditAmountPerBp(order);
              }}
              cancelOrderCallback={async () => {
                setOrderLoadingIds([...orderLoadingIds, order.shortOrderId]);
                await cancelOrder(order);
              }}
              loading={orderLoadingIds.includes(order.shortOrderId)}
            />
          </Paper>
        ))}
    </Box>
  );
}

export default SACOverview;
