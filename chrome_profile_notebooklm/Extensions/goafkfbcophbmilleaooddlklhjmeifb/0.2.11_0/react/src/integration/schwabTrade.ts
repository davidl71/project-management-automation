import {
  findEarliestDateIndexAfterNdays,
  selectOption,
  findNearestNumberIdx,
  calculateBoxSpreadTargetSize,
} from "../utils/contentScript";
import { settlementDateDuration, removeDateLeadingZeros } from "../utils/date";
import { calculatePrice } from "../utils/optionsPicker";
import { getStrikePriceTargets } from "../utils/strikePricePicker";

import {
  BrowserClient,
  defaultStackParser,
  getDefaultIntegrations,
  makeFetchTransport,
  Scope,
} from "@sentry/browser";

// filter integrations that use the global variable
const integrations = getDefaultIntegrations({}).filter((defaultIntegration) => {
  return !["BrowserApiErrors", "Breadcrumbs", "GlobalHandlers"].includes(
    defaultIntegration.name
  );
});

const client = new BrowserClient({
  dsn: "https://5776c83a92371eb813815cd148b33460@o4508474674249728.ingest.us.sentry.io/4508487299432448",
  transport: makeFetchTransport,
  stackParser: defaultStackParser,
  integrations: integrations,
});

const scope = new Scope();
scope.setClient(client);

client.init(); // initializing has to be done after setting the client on the scope

export interface BorrowData {
  accountId: string;
  accountName: string;
  borrowAmount: number;
  periodInDays: number;
}

export interface RepayData {
  accountId: string;
  accountName: string;
  expirationDate: string; // M/D/YYYY
  strikePrice1: string; // lower. e.g. "5000"
  strikePrice2: string; // higher. e.g. "5100"
  quantity: number;
  costBasis: number; // e.g. 9,500
}

export interface OrderDetails {
  expirationDate: string; // M/D/YYYY

  // this means the size of the order
  upfrontCash: number;

  // size of the box
  repaymentAmount: number;

  accountId: string;
  accountName: string;

  // repay only
  costBasis?: number | undefined;
}

function selectAccount(borrowData: { accountId: string; accountName: string }) {
  const accountLinks = document.querySelectorAll(
    'a[name="&lid=lc_account_selector"]'
  );

  const accountLink = Array.from(accountLinks).find((element) => {
    const accountName = element.querySelector(
      ".sdps-account-selector__left-col"
    )?.textContent;
    const accountNumberLastDigits = element.querySelector(
      ".sdps-account-selector__right-col"
    )?.textContent;

    return (
      accountName === borrowData.accountName &&
      accountNumberLastDigits === `…${borrowData.accountId.slice(-3)}`
    );
  });

  if (!accountLink) {
    console.error("Account not found - cannot continue");
    return;
  }

  // @ts-ignore
  accountLink.click();
}

async function inputOrder(
  borrowData?: BorrowData | undefined,
  repayData?: RepayData | undefined
): Promise<OrderDetails | undefined> {
  if (!borrowData && !repayData) {
    throw new Error("Either borrowData or repayData must be provided");
  }

  const legIds = ["01", "02", "03", "04"];

  const quantityElements = legIds.map((id) => {
    const result = document.querySelector(
      `input[id="ordernumber${id}inputqty-stepper-input"]`
    );
    if (!result) {
      console.error(
        `Quantity element for leg ${id} not found - cannot continue`
      );
      throw new Error(
        `Quantity element for leg ${id} not found - cannot continue`
      );
    }
    return result;
  });

  const expirationElements = Array.from(
    document.querySelectorAll(`select[aria-label="expiration"]`).values()
  );
  if (!expirationElements || expirationElements.length !== 4) {
    console.error(`Expiration element not found - cannot continue`);
    throw new Error(`Expiration element not found - cannot continue`);
  }

  const expirationOptions = Array.from(
    expirationElements[0].querySelectorAll("option")
  ).map((option: any) => option.value);

  var expirationIdx: number | undefined;

  if (borrowData) {
    // find expiration option that is closest, but bigger than periodInDays
    expirationIdx = findEarliestDateIndexAfterNdays(
      expirationOptions,
      borrowData.periodInDays
    );
    expirationElements.forEach((element: any) => {
      selectOption(element, expirationOptions[expirationIdx!]);
    });
  } else if (repayData) {
    // repayData.expirationDate is in MM/DD/YYYY format
    // Schwab expect the value to be in M/D/YYYY format
    // TODO: fix it
    expirationElements.forEach((element: any) => {
      selectOption(element, removeDateLeadingZeros(repayData.expirationDate));
    });
  }
  const strikeElements = Array.from(
    document.querySelectorAll(`select[aria-label="Strike Price"]`).values()
  );
  if (!strikeElements || strikeElements.length !== 4) {
    console.error(`Strike element not found - cannot continue`);
    throw new Error(`Strike element not found - cannot continue`);
  }
  const strikeOptions = Array.from(
    strikeElements[0].querySelectorAll("option")
  ).map((option) => option.value);

  const strikePrice1 = "5000"; // we hard code this one for now
  var strikePrice2;

  var quantity: number = 1;

  if (borrowData) {
    const boxSizeTarget = await calculateBoxSpreadTargetSize(
      borrowData.borrowAmount,
      borrowData.periodInDays
    );

    // TODO: we are not using strikePrice1 here
    const strikeTarget = getStrikePriceTargets(boxSizeTarget);
    quantity = strikeTarget.quantity;
    const strikePrice2Target = strikeTarget.strikePrice2Target;

    const strikePrice2Idx = findNearestNumberIdx(
      strikeOptions.map((option) => parseInt(option)),
      strikePrice2Target
    );

    strikePrice2 = strikeOptions[strikePrice2Idx];

    selectOption(strikeElements[0], strikePrice1);
    selectOption(strikeElements[1], strikePrice2);
    selectOption(strikeElements[2], strikePrice1);
    selectOption(strikeElements[3], strikePrice2);
  } else if (repayData) {
    quantity = repayData.quantity;

    selectOption(strikeElements[0], repayData.strikePrice1);
    selectOption(strikeElements[1], repayData.strikePrice2);
    selectOption(strikeElements[2], repayData.strikePrice1);
    selectOption(strikeElements[3], repayData.strikePrice2);
  }

  quantityElements.forEach((element) => {
    const inputEvent = new Event("input", {
      bubbles: true,
      cancelable: true,
    });
    // @ts-ignore
    element.value = quantity;

    element.dispatchEvent(inputEvent);
  });

  const callOrPutElements = Array.from(
    document.querySelectorAll(`select[aria-label="contract"]`).values()
  );
  const contractIds = expirationElements.map((element: any) => {
    // onchange attribute example: mctordleg3461bcc2.updateStrike(this)
    const onchange = element.getAttribute("onchange");
    if (!onchange) {
      console.error("onchange attribute not found - cannot continue");
      throw new Error("onchange attribute not found - cannot continue");
    }
    return onchange.split(".")[0];
  });

  const buyOrSellOpenCloseElements = contractIds.map((id: any) =>
    document.querySelector(
      `select[onchange="${id}.handleInputChange(false, true)"]`
    )
  );

  selectOption(callOrPutElements[0], "C");
  selectOption(callOrPutElements[1], "C");
  selectOption(callOrPutElements[2], "P");
  selectOption(callOrPutElements[3], "P");

  await new Promise((resolve) => setTimeout(resolve, 1000));

  if (borrowData) {
    // 201 = Buy to open, 203 = Sell to open
    selectOption(buyOrSellOpenCloseElements[0], 203);
    selectOption(buyOrSellOpenCloseElements[1], 201);
    selectOption(buyOrSellOpenCloseElements[2], 201);
    selectOption(buyOrSellOpenCloseElements[3], 203);
  } else if (repayData) {
    // 202 = Buy to close, 204 = Sell to close
    selectOption(buyOrSellOpenCloseElements[0], 202);
    selectOption(buyOrSellOpenCloseElements[1], 204);
    selectOption(buyOrSellOpenCloseElements[2], 204);
    selectOption(buyOrSellOpenCloseElements[3], 202);
  }

  await new Promise((resolve) => setTimeout(resolve, 1000));

  const priceSelect = document.querySelector(
    'select[aria-label="order type Dropdown"]'
  );
  if (!priceSelect) {
    console.error("Price select not found - cannot continue");
    return;
  }

  const limitInput = document.getElementById("limitprice0-stepper-input");

  if (!limitInput) {
    console.error("Limit input not found - cannot continue");
    return;
  }

  var limitPrice: string = "0.00";

  if (borrowData && strikePrice2 && expirationIdx) {
    selectOption(priceSelect, "201" /* Net credit */);

    limitPrice = calculatePrice(
      borrowData.periodInDays,
      parseInt(strikePrice2) - parseInt(strikePrice1),
      settlementDateDuration(expirationOptions[expirationIdx])
    ).toFixed(2);

    // @ts-ignore
    limitInput.value = limitPrice;
  } else if (repayData) {
    selectOption(priceSelect, "202" /* Net debit */);

    limitPrice = calculatePrice(
      settlementDateDuration(repayData.expirationDate),
      parseInt(repayData.strikePrice2) - parseInt(repayData.strikePrice1),
      settlementDateDuration(repayData.expirationDate)
    ).toFixed(2);

    // @ts-ignore
    limitInput.value = limitPrice;
  }

  limitInput.dispatchEvent(
    new Event("change", {
      bubbles: true,
      cancelable: true,
    })
  );
  limitInput.dispatchEvent(
    new Event("input", {
      bubbles: true,
      cancelable: true,
    })
  );

  if (borrowData && strikePrice2 && expirationIdx) {
    return {
      expirationDate: expirationOptions[expirationIdx],
      upfrontCash: parseFloat(limitPrice) * 100 * quantity,
      repaymentAmount:
        (parseInt(strikePrice2) - parseInt(strikePrice1)) * 100 * quantity,
      accountId: borrowData.accountId,
      accountName: borrowData.accountName,
    };
  } else if (repayData) {
    return {
      expirationDate: removeDateLeadingZeros(repayData.expirationDate),
      upfrontCash: parseFloat(limitPrice) * 100 * quantity,
      repaymentAmount:
        (parseInt(repayData.strikePrice2) - parseInt(repayData.strikePrice1)) *
        100 *
        quantity,
      accountId: repayData.accountId,
      accountName: repayData.accountName,
      costBasis: repayData.costBasis,
    };
  }
}

export async function executeSchwabTrade(borrowData: BorrowData) {
  /* Example input:
  {
    accountId: string;
    accountName: string;
    borrowAmount: number;
    periodInDays: number;
  }*/
  try {
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Step 1: make sure we have the right account selected
    selectAccount(borrowData);

    // wait for page to update
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Step 2: pick the symbol; we use the custom event to select the $SPX symbol
    const tradeOrder = document.querySelector("mc-trade-order");

    if (!tradeOrder) {
      console.error("Trade order not found - cannot continue");
      return;
    }

    tradeOrder.dispatchEvent(
      new CustomEvent("symbolChanged", {
        detail: {
          symbol: ["$SPX", "undefined"],
          isTab: false,
          isSymbolFound: true,
        },
        bubbles: true,
      })
    );

    const fourLeg = document.querySelector(
      "[onclick*=\".changeStrategy(this, 'Custom 4 Leg')\"]"
    );
    if (!fourLeg) {
      console.error("4 leg not found - cannot continue");
    }

    // @ts-ignore
    fourLeg.click();

    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Step 3: input the order
    const orderDetails = await inputOrder(borrowData, undefined);

    if (!orderDetails) {
      console.error("Order details not found - cannot continue");
      return;
    }

    // Step 4: submit the order
    // TODO: update the limit order price
    const reviewButton: HTMLButtonElement | null = document.querySelector(
      "button.mcaio-order--reviewbtn"
    );
    if (!reviewButton) {
      console.error("Review button not found - cannot continue");
      return;
    }
    reviewButton.click();

    // Step 5: update the chrome extension by sending it a message
    const response = await chrome.runtime.sendMessage({
      platform: "schwab",
      action: "review_trade",
      data: orderDetails,
    });
    console.log("response", response);
  } catch (error) {
    scope.captureException(error);
  }
}

export async function executeSchwabRepay(repayData: RepayData) {
  /* Example input:
  {
    accountId: string;
    accountName: string;
    maturityDate: string; // MM/DD/YYYY
    strikePrice1: number; // lower
    strikePrice2: number; // higher
    quantity: number;
  }*/
  try {
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Step 1: make sure we have the right account selected
    selectAccount(repayData);

    // wait for page to update
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Step 2: pick the symbol; we use the custom event to select the $SPX symbol
    const tradeOrder = document.querySelector("mc-trade-order");

    if (!tradeOrder) {
      console.error("Trade order not found - cannot continue");
      return;
    }

    tradeOrder.dispatchEvent(
      new CustomEvent("symbolChanged", {
        detail: {
          symbol: ["$SPX", "undefined"],
          isTab: false,
          isSymbolFound: true,
        },
        bubbles: true,
      })
    );

    const fourLeg = document.querySelector(
      "[onclick*=\".changeStrategy(this, 'Custom 4 Leg')\"]"
    );
    if (!fourLeg) {
      console.error("4 leg not found - cannot continue");
    }

    // @ts-ignore
    fourLeg.click();

    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Step 3: input the order
    const orderDetails = await inputOrder(undefined, repayData);

    if (!orderDetails) {
      console.error("Order details not found - cannot continue");
      return;
    }

    // Step 4: submit the order
    // TODO: update the limit order price
    const reviewButton: HTMLButtonElement | null = document.querySelector(
      "button.mcaio-order--reviewbtn"
    );
    if (!reviewButton) {
      console.error("Review button not found - cannot continue");
      return;
    }
    reviewButton.click();

    // Step 5: update the chrome extension by sending it a message
    // TODO: update order message type
    const response = await chrome.runtime.sendMessage({
      platform: "schwab",
      action: "review_repay",
      data: orderDetails,
    });
    console.log("response", response);
  } catch (error) {
    scope.captureException(error);
  }
}
