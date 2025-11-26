import { SchwabTradeUrl, FidelityTradeUrl } from "./utils/constant";

chrome.runtime.onMessageExternal.addListener(function (
  request,
  sender,
  sendResponse
) {
  console.log("Receive message", request);

  if (request.type === "fidelity_balance") {
    chrome.storage.local.set({ fidelity_balance: request.data }).then(() => {
      console.log("Saved fidelity balance");
    });
  }

  if (request.type === "schwab_balance") {
    chrome.storage.local.set({ schwab_balance: request.data }).then(() => {
      console.log("Saved schwab balance");
    });
  }
});

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (changeInfo.status === "complete" && tab.url?.includes(SchwabTradeUrl)) {
    console.log(
      "Schwab trading page loaded, check if we need to execute trade"
    );
    // check if we need to execute a trade
    chrome.storage.local.get(["schwab_borrow"]).then(async (result) => {
      if (result.schwab_borrow) {
        console.log("Send message to execute trade after 1s delay");
        await new Promise((resolve) => setTimeout(resolve, 1000));
        // send message to the content script to execute the trade
        chrome.tabs.sendMessage(tabId, {
          platform: "schwab",
          action: "execute_trade",
          data: result.schwab_borrow,
        });
        chrome.storage.local.set({ schwab_borrow: null });
      }
    });

    // check if we need to execute a repay
    chrome.storage.local.get(["schwab_repay"]).then(async (result) => {
      if (result.schwab_repay) {
        console.log("Send message to execute repay after 1s delay");
        await new Promise((resolve) => setTimeout(resolve, 1000));
        // send message to the content script to execute the trade
        chrome.tabs.sendMessage(tabId, {
          platform: "schwab",
          action: "execute_repay",
          data: result.schwab_repay,
        });
        chrome.storage.local.set({ schwab_repay: null });
      }
    });
  }

  if (changeInfo.status === "complete" && tab.url?.includes(FidelityTradeUrl)) {
    console.log(
      "Fidelity trading page loaded, check if we need to execute trade"
    );
    // check if we need to execute a trade
    chrome.storage.local.get(["fidelity_borrow"]).then(async (result) => {
      if (result.fidelity_borrow) {
        console.log("Send message to execute trade after 1s delay");

        const spxContracts = await chrome.storage.local.get(["spx_contracts"]);
        await new Promise((resolve) => setTimeout(resolve, 1000));

        if (spxContracts.spx_contracts) {
          const { data, timestamp } = spxContracts.spx_contracts;

          // check if the timestamp is over 1 days old
          if (
            timestamp &&
            Date.now() - timestamp <= 24 * 60 * 60 * 1000 &&
            data
          ) {
            chrome.tabs.sendMessage(tabId, {
              platform: "fidelity",
              action: "execute_trade",
              data: result.fidelity_borrow,
              expirationDates: Object.keys(data),
            });
          } else {
            chrome.tabs.sendMessage(tabId, {
              platform: "fidelity",
              action: "execute_trade",
              data: result.fidelity_borrow,
              expirationDates: null,
            });
          }
        } else {
          chrome.tabs.sendMessage(tabId, {
            platform: "fidelity",
            action: "execute_trade",
            data: result.fidelity_borrow,
            expirationDates: null,
          });
        }

        // send message to the content script to execute the trade
        chrome.storage.local.set({ fidelity_borrow: null });
      }
    });

    // check if we need to execute a repay
    chrome.storage.local.get(["fidelity_repay"]).then(async (result) => {
      if (result.fidelity_repay) {
        console.log("Send message to execute repay after 1s delay");
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // send message to the content script to execute the trade
        chrome.tabs.sendMessage(tabId, {
          platform: "fidelity",
          action: "execute_repay",
          data: result.fidelity_repay,
        });
        chrome.storage.local.set({ fidelity_repay: null });
      }
    });
  }
});
