import { Button, IconButton, LinearProgress, Typography } from "@mui/material";
import { Box } from "@mui/system";
import { settlementDateDuration } from "../utils/date";

interface OrderDetailsProps {
  limitPrice: number;
  quantity: number;
  strikePrice1: number;
  strikePrice2: number;
  expDate: string;
  accountId: string;
  shortOrderId: string;
  expandedOrderId: string;
  status: string;

  cancelOrderCallback: () => Promise<void>;
  decreasePriceCallbackByTick: () => Promise<void>;

  decreasePriceByBpCallback?: () => Promise<void>;

  loading: boolean;
}

function OrderDetails(props: OrderDetailsProps) {
  const {
    limitPrice,
    quantity,
    strikePrice1,
    strikePrice2,
    expDate, // MM/DD/YYYY
    accountId,
    shortOrderId,
    expandedOrderId,
    status,
    cancelOrderCallback,
    decreasePriceCallbackByTick,
    decreasePriceByBpCallback,
    loading,
  } = props;

  const creditAmount = limitPrice * quantity * 100;
  const repayAmount = (strikePrice2 - strikePrice1) * quantity * 100;

  const dateDifference = settlementDateDuration(expDate);

  // daily compounding, 360 day as a year
  const interestRate =
    (Math.pow(
      1 + (repayAmount - creditAmount) / creditAmount,
      1 / dateDifference
    ) -
      1) *
    360;

  return (
    <Box gap={0.5} display={"flex"} flexDirection={"column"}>
      <Box display={"flex"} flexDirection={"row"} width={"100%"} gap={1}>
        <Typography>Account: {accountId}</Typography>
      </Box>
      <Box
        display={"flex"}
        flexDirection={"row"}
        justifyContent={"space-between"}
        width={"100%"}
      >
        <Typography color={"#65727b"}>Loan amount</Typography>
        <Typography color={"#65727b"}>
          {Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
          }).format(creditAmount)}
        </Typography>
      </Box>
      <Box
        display={"flex"}
        flexDirection={"row"}
        justifyContent={"space-between"}
        width={"100%"}
      >
        <Typography color={"#65727b"}>Implied interest rate</Typography>
        <Typography color={"#65727b"}>
          {(interestRate * 100).toFixed(2)}%
        </Typography>
      </Box>
      {status === "Filled" ? (
        <>
          <Box
            display={"flex"}
            flexDirection={"row"}
            justifyContent={"space-between"}
          >
            <Typography color={"#65727b"}>Status:</Typography>
            <Typography color={"#15803d"}>Filled</Typography>
          </Box>
        </>
      ) : loading ? (
        <LinearProgress style={{ marginTop: "12px", marginBottom: "12px" }} />
      ) : (
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
        >
          <Button variant="outlined" onClick={decreasePriceCallbackByTick}>
            Bump 0.05
          </Button>
          <Button variant="outlined" onClick={decreasePriceByBpCallback}>
            Bump 1bp
          </Button>
          <Button
            variant="outlined"
            color="error"
            onClick={cancelOrderCallback}
          >
            Cancel
          </Button>
        </Box>
      )}
    </Box>
  );
}

export default OrderDetails;
