import {
  executeSchwabRepay,
  executeSchwabTrade,
} from "./integration/schwabTrade";
import { SchwabTradeUrl } from "./utils/constant";
import { injectScript } from "./utils/contentScript";

// Content script for Schwab

// Inject script to extract the balance information
// We need to inject it because we need to use auth metadata to get the balance info
injectScript(chrome.runtime.getURL("/js/schwab.js"), "body");

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  /*
  {
      platform: "schwab",
      action: "navigate_to_trading",
  }
  */
  if (
    request.platform === "schwab" &&
    request.action === "navigate_to_trading"
  ) {
    sendResponse({ result: "ok" });
    window.open(SchwabTradeUrl, "_self");
  }

  /*
  {
      platform: "schwab",
      action: "execute_trade",
      data: {...BorrowData}
  }
  */
  if (request.platform === "schwab" && request.action === "execute_trade") {
    sendResponse({ result: "ok" });
    console.log("SyntheticFi: EXECUTE TRADE");

    executeSchwabTrade(request.data);
  }

  /*
  {
      platform: "schwab",
      action: "execute_repay",
      data: {...RepayData}
  }
  */
  if (request.platform === "schwab" && request.action === "execute_repay") {
    sendResponse({ result: "ok" });
    console.log("SyntheticFi: EXECUTE REPAY");

    executeSchwabRepay(request.data);
  }
});
