import React from "react";

import { Box, CircularProgress } from "@mui/material";
import SchwabBalance from "./SchwabBalance";
import FidelityBalance from "./FidelityBalance";
import Placeholder from "./Placeholder";
import SACOverview from "./SACOverview";

function getDomain(url: string): string {
  try {
    const parsedUrl = new URL(url);
    return parsedUrl.hostname;
  } catch (error) {
    console.error("Invalid URL:", error);
    return "";
  }
}

function Overview() {
  const [currentTab, setCurrentTab] = React.useState<string | undefined>(
    undefined
  );

  React.useEffect(() => {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      // since only one tab should be active and in the current window at once
      // the return variable should only have one entry
      const activeTab = tabs[0];

      const tabUrl = activeTab.url;

      setCurrentTab(tabUrl);
    });
  }, []);

  if (!currentTab) {
    return (
      <>
        <CircularProgress />
      </>
    );
  }

  const domain = getDomain(currentTab);

  return (
    <Box display={"flex"}>
      {domain === "client.schwab.com" && <SchwabBalance />}
      {domain === "digital.fidelity.com" && <FidelityBalance />}
      {domain === "si2.schwabinstitutional.com" && <SACOverview />}
      {domain !== "client.schwab.com" &&
        domain !== "digital.fidelity.com" &&
        domain !== "si2.schwabinstitutional.com" && <Placeholder />}
    </Box>
  );
}

export default Overview;
