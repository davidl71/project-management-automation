import {
  executeFidelityRepay,
  executeFidelityTrade,
} from "./integration/fidelityTrade";
import { FidelityTradeUrl } from "./utils/constant";
import { injectScript } from "./utils/contentScript";

injectScript(chrome.runtime.getURL("/js/fidelity.js"), "body");

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  /*
  {
      platform: "fidelity",
      action: "navigate_to_trading",
  }
  */
  if (
    request.platform === "fidelity" &&
    request.action === "navigate_to_trading"
  ) {
    sendResponse({ result: "ok" });
    window.open(FidelityTradeUrl, "_self");
  }

  /*
  {
      platform: "fidelity",
      action: "execute_trade",
      data: {...BorrowData}
  }
  */
  if (request.platform === "fidelity" && request.action === "execute_trade") {
    sendResponse({ result: "ok" });
    console.log("SyntheticFi: EXECUTE TRADE");

    executeFidelityTrade(request.data, request.expirationDates);
  }

  /*
  {
      platform: "fidelity",
      action: "execute_repay",
      data: {...RepayData}
  }
  */
  if (request.platform === "fidelity" && request.action === "execute_repay") {
    sendResponse({ result: "ok" });
    console.log("SyntheticFi: EXECUTE REPAY");

    executeFidelityRepay(request.data);
  }
});
