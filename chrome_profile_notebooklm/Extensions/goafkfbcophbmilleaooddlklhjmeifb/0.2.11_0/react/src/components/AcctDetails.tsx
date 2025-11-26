import React from "react";

import { Box, IconButton, Tooltip, Typography } from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";

interface AcctDetailsProps {
  marginDebitBalance: number;
  accountId: string;
  accountName: string;
  withdrawTotal: number;
  withdrawMargin: number;
  isIra: boolean;
  boxSpreadDebitBalance: number;
}

function AcctDetails(props: AcctDetailsProps) {
  const {
    marginDebitBalance,
    accountId,
    accountName,
    withdrawTotal,
    withdrawMargin,
    isIra,
    boxSpreadDebitBalance,
  } = props;

  if (isIra) {
    // tell users that IRA accounts are not supported
    return (
      <>
        <Box
          display={"flex"}
          flexDirection={"row"}
          width={"100%"}
          gap={1}
          marginBottom={1}
        >
          <Typography>{accountName}</Typography>
          <Tooltip title={accountId}>
            <IconButton size={"small"} sx={{ padding: 0 }}>
              <InfoIcon sx={{ width: "18px", height: "18px" }} />
            </IconButton>
          </Tooltip>
        </Box>
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
          width={"100%"}
        >
          <Typography color={"#65727b"}>
            Retirement accounts are not eligible.
          </Typography>
        </Box>
      </>
    );
  }

  return (
    <Box gap={0.5} display={"flex"} flexDirection={"column"}>
      <Box display={"flex"} flexDirection={"row"} width={"100%"} gap={1}>
        <Typography>{accountName}</Typography>
        <Tooltip title={accountId}>
          <IconButton size={"small"} sx={{ padding: 0 }}>
            <InfoIcon sx={{ width: "18px", height: "18px" }} />
          </IconButton>
        </Tooltip>
      </Box>
      <Box
        display={"flex"}
        flexDirection={"row"}
        justifyContent={"space-between"}
        width={"100%"}
      >
        <Typography color={"#65727b"}>Cash</Typography>
        <Typography color={"#65727b"}>
          {Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
          }).format(withdrawTotal - withdrawMargin)}
        </Typography>
      </Box>
      <Box
        display={"flex"}
        flexDirection={"row"}
        justifyContent={"space-between"}
        width={"100%"}
      >
        <Typography color={"#65727b"}>Margin loan balance</Typography>
        <Typography color={"#65727b"}>
          {Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
          }).format(marginDebitBalance)}
        </Typography>
      </Box>
      <Typography>With SyntheticFi</Typography>
      <Box marginLeft={1}>
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
          width={"100%"}
        >
          <Typography color={"#65727b"}>Loan balance</Typography>
          <Typography color={"#65727b"}>
            {Intl.NumberFormat("en-US", {
              style: "currency",
              currency: "USD",
            }).format(boxSpreadDebitBalance)}
          </Typography>
        </Box>
        <Box
          display={"flex"}
          flexDirection={"row"}
          justifyContent={"space-between"}
          width={"100%"}
        >
          <Typography color={"#65727b"}>Available credit</Typography>
          <Typography color={"#65727b"}>
            {Intl.NumberFormat("en-US", {
              style: "currency",
              currency: "USD",
            }).format(
              // withdrawMargin: additional amount that users can withdraw
              // marginDebitBalance: margin loan can be refinanced
              withdrawMargin + marginDebitBalance
            )}
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}

export default AcctDetails;
