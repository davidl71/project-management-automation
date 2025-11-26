import React from "react";

import dayjs from "dayjs";

import {
  Box,
  Button,
  CircularProgress,
  InputLabel,
  Paper,
  Typography,
} from "@mui/material";
import { useNavigate, useSearchParams } from "react-router-dom";
import AcctDetails from "../components/AcctDetails";

import CurrencyInput from "react-currency-input-field";
import ProposalDetails from "../components/ProposalDetails";
import { OrderDetails } from "../integration/schwabTrade";
import { useAuth } from "@clerk/chrome-extension";
import { saveTrade } from "../utils/saveData";
import { extractFidelityMarginInfo } from "../utils/balance";
import { DateOptions } from "../components/DateOptions";

/* /fidelity/borrow?account={accountId} */

// TODO: merge common pieces between SchwabBorrow and FidelityBorrow
function FidelityBorrow() {
  const navigate = useNavigate();

  const today = dayjs().startOf("day");

  const [loading, setLoading] = React.useState(false);
  const [fidelityBalance, setFidelityBalance] = React.useState<any>({});
  const { isSignedIn, userId, isLoaded, getToken } = useAuth();

  const [formData, setFormData] = React.useState({
    borrowAmount: "",
    periodInDays: "",
    // Add more fields as needed
  });

  const normalizedFormData = {
    borrowAmount: parseInt(formData.borrowAmount) || undefined,
    periodInDays: parseInt(formData.periodInDays) || undefined,
  };

  const cannotContinue =
    normalizedFormData.borrowAmount === undefined ||
    normalizedFormData.periodInDays === undefined ||
    normalizedFormData.periodInDays > 370 ||
    normalizedFormData.periodInDays < 25;

  const [searchParams, setSearchParams] = useSearchParams();

  const accountId = searchParams.get("account");

  React.useEffect(() => {
    chrome.storage.local.get(["fidelity_balance"]).then((result) => {
      setFidelityBalance(result.fidelity_balance);
    });
    chrome.storage.onChanged.addListener((changes, namespace) => {
      for (let [key, { newValue }] of Object.entries(changes)) {
        if (key === "fidelity_balance") {
          setFidelityBalance(newValue);
        }
      }
    });

    // receive review_trade event and navigate to review page
    chrome.runtime.onMessage.addListener(function (
      request,
      sender,
      sendResponse
    ) {
      /*
      {
          platform: "fidelity",
          action: "review_trade",
          data: {...OrderDetails}
      }
      */
      console.log("request body", request);
      if (
        request.platform === "fidelity" &&
        request.action === "review_trade"
      ) {
        console.log("SyntheticFi: REVIEW TRADE");
        sendResponse({ result: "ok" });

        const data: OrderDetails = request?.data;

        navigate(
          `/fidelity/review?account=${accountId}&expiration=${data.expirationDate}&upfrontCash=${data.upfrontCash}&repaymentAmount=${data.repaymentAmount}`
        );
      }
    });
  }, [accountId, navigate]);

  const fidelityMarginInfo = extractFidelityMarginInfo(fidelityBalance);

  const relevantMarginInfo = fidelityMarginInfo.find(
    (acct) => acct.accountId === accountId
  );

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log(formData);

    setLoading(true);

    // save the order to local storage
    chrome.storage.local.set({
      fidelity_borrow: {
        ...normalizedFormData,
        accountId: relevantMarginInfo?.accountId,
        accountName: relevantMarginInfo?.accountName,
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

    if (isLoaded && isSignedIn) {
      // attempt to store the balance
      const token = await getToken();
      const data = {
        ...normalizedFormData,
        accountId: relevantMarginInfo?.accountId,
        accountName: relevantMarginInfo?.accountName,
      };
      if (token) {
        await saveTrade("fidelity", data, token, userId);
      }
    }
  };

  const exceedCreditLimit =
    normalizedFormData.borrowAmount &&
    relevantMarginInfo?.withdrawTotal &&
    relevantMarginInfo?.withdrawMargin &&
    normalizedFormData.borrowAmount >
      relevantMarginInfo?.withdrawMargin +
        relevantMarginInfo?.marginDebitBalance;

  const formComponent = (
    <form
      onSubmit={handleSubmit}
      style={{
        borderColor: "FFFFFF",
        width: "100%",
        marginLeft: 2,
        marginRight: 2,
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "space-between",
          flexDirection: "column",
          gap: 2,
          margin: 2,
        }}
      >
        <Box display="flex" flexDirection="column">
          <InputLabel>Borrow amount</InputLabel>
          <CurrencyInput
            name="borrowAmount"
            prefix="$"
            decimalsLimit={2}
            placeholder="$100,000"
            value={formData.borrowAmount}
            onValueChange={(value, name) => {
              handleChange({ target: { name, value } });
            }}
            allowNegativeValue={false}
            style={{
              border: "1px solid #ced4da",
              padding: "16.5px 0px 16.5px 14px",
              borderRadius: "4px",
              fontSize: "16px",
            }}
          />
          {exceedCreditLimit ? (
            <Typography color={"#ff465d"}>
              Amount exceeds available credit limit
            </Typography>
          ) : (
            <></>
          )}
        </Box>
        <Box>
          <InputLabel>Expected payback date</InputLabel>
          <DateOptions
            periodInDays={
              formData.periodInDays
                ? parseInt(formData.periodInDays)
                : undefined
            }
            setPeriodInDays={(periodInDays: number) => {
              setFormData({
                ...formData,
                periodInDays: periodInDays.toString(),
              });
            }}
          />
        </Box>
      </Box>
      {!cannotContinue ? (
        <>
          <ProposalDetails
            borrowAmount={normalizedFormData.borrowAmount!}
            periodInDays={normalizedFormData.periodInDays!}
          />
        </>
      ) : (
        <></>
      )}
      <Button
        type="submit"
        variant="contained"
        disabled={cannotContinue}
        style={{
          marginTop: 20,
          marginLeft: "auto",
          marginRight: "auto",
          minWidth: "20%",
          alignSelf: "center",
          display: "block",
        }}
      >
        Preview
      </Button>
    </form>
  );

  return (
    <Box display={"flex"} flexWrap={"wrap"} margin={1}>
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
      {loading ? (
        <Box
          display={"flex"}
          justifyContent={"center"}
          alignContent={"center"}
          width={"100%"}
          marginTop={1}
        >
          <CircularProgress />
          <Typography alignSelf={"center"}>
            Generating order preview...
          </Typography>
        </Box>
      ) : (
        formComponent
      )}
    </Box>
  );
}

export default FidelityBorrow;
