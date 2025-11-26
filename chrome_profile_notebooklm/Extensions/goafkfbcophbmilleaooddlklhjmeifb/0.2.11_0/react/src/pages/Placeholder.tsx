import React from "react";

import { Box, Paper, Typography, styled } from "@mui/material";

import LockIcon from "@mui/icons-material/Lock";
import AssuredWorkloadIcon from "@mui/icons-material/AssuredWorkload";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: "center",
  justifyContent: "space-between",
  display: "flex",
  flexDirection: "column",
  color: theme.palette.text.primary,
  gap: "1rem",
  fontSize: "1.2rem",
  minHeight: "110px",
  maxHeight: "110px",
  cursor: "pointer",
  width: "90%",
  paddingLeft: "1rem",
  paddingRight: "1rem",
  marginRight: "auto",
  marginLeft: 0,
}));

function Placeholder() {
  return (
    <Box
      display={"flex"}
      flexDirection={"column"}
      flexWrap={"wrap"}
      marginTop={1}
      marginBottom={1}
      marginLeft={2}
      marginRight={2}
      width={"100%"}
    >
      <Typography variant={"h5"}>Supported platforms</Typography>
      <Box
        display={"flex"}
        flexDirection={"column"}
        flexWrap={"wrap"}
        margin={1}
        gap={2}
        alignItems={"center"}
      >
        <Item
          onClick={() => {
            chrome.tabs.create({
              url: "https://client.schwab.com/Areas/Access/Login",
            });
          }}
        >
          <img
            src={"/schwab.png"}
            alt="Charles Schwab"
            height={60}
            style={{ alignSelf: "center" }}
          />
          Charles Schwab
        </Item>
        <Item
          onClick={() => {
            chrome.tabs.create({
              url: "https://digital.fidelity.com/prgw/digital/login/full-page",
            });
          }}
        >
          <img
            src={"/fidelity.png"}
            alt="Fidelity"
            height={60}
            style={{ alignSelf: "center" }}
          />
          Fidelity
        </Item>
      </Box>
      <Paper
        sx={{
          border: 1,
          borderColor: "grey.500",
          borderRadius: "10px",
          padding: 1,
          marginTop: 2,
          marginBottom: 1,
        }}
      >
        <Typography gutterBottom>Safety and Privacy</Typography>
        <Box display={"flex"} flexDirection={"column"} gap={"0.5rem"}>
          <Typography color={"#65727b"} display={"inline-block"}>
            <LockIcon sx={{ height: "16px" }} />
            We never access login credentials.
          </Typography>
          <Typography color={"#65727b"} display={"inline-block"}>
            <AssuredWorkloadIcon sx={{ height: "16px" }} />
            We will never sell your data.
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
}

export default Placeholder;
