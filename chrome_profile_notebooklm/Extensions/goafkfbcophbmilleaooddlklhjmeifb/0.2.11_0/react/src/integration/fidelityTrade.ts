import dayjs from "dayjs";
import {
  calculateBoxSpreadTargetSize,
  findNearestNumberIdx,
} from "../utils/contentScript";
import { calculatePrice } from "../utils/optionsPicker";
import { settlementDateDuration } from "../utils/date";
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
  expirationDate: string; // JUL 25, 2024
  strikePrice1: string; // lower. e.g. "5000"
  strikePrice2: string; // higher. e.g. "5100"
  quantity: number;
  costBasis: number; // e.g. 9,500
}

export interface OrderDetails {
  expirationDate: string; // Jun 25, 2024 PM
  upfrontCash: number;
  repaymentAmount: number;

  accountId: string;
  accountName: string;

  // repay only
  costBasis?: number | undefined;
}

async function setInput(input: any, value: string) {
  input.click();

  const keyUpEvent = new KeyboardEvent("keyup", {
    key: "1",
    code: "Digit1",
    keyCode: 49,
    which: 49,
    bubbles: true,
    cancelable: true,
  });

  const inputEvent = new Event("input", {
    bubbles: true,
    cancelable: true,
  });

  const focusOutEvent = new Event("focusout", {
    bubbles: true,
    cancelable: true,
  });

  // @ts-ignore
  input.value = value;
  input.dispatchEvent(inputEvent);

  // Fidelity updates internal state on keyup event, so we need to manually trigger it
  input.dispatchEvent(keyUpEvent);

  input.dispatchEvent(focusOutEvent);
}

function selectDropdownOption(button: any, action: string) {
  button.click();

  const label = button.getAttribute("aria-labelledby");

  const dropdown = document.querySelector(`div[aria-labelledby="${label}"]`);
  if (!dropdown) {
    throw new Error("Dropdown not found");
  }

  const actionOptions: HTMLButtonElement[] = Array.from(
    dropdown.querySelectorAll('button[role="option"]')
  );

  const targetOption = actionOptions.find((option) => {
    var text = option.textContent;

    if (!text) {
      // look for span text
      const span = option.querySelector("span");
      if (span) {
        text = span.textContent;
      }
    }

    return text?.toLocaleLowerCase()?.includes(action.toLocaleLowerCase());
  });

  if (!targetOption) {
    throw new Error(`Dropdown option not found: ${action}`);
  }
  targetOption.click();
}

function extractOptions(selector: string): string[] {
  const container = document.querySelector(selector);
  if (!container) {
    throw new Error("container not found");
  }

  // Iterate over each button element within the container
  var expButtons = Array.from(container.querySelectorAll("button"));

  // Iterate over each button element
  return expButtons.map((button) => {
    var text;

    var span = button.querySelector("span");
    if (span) {
      text = span.textContent?.trim();
    } else {
      // fall back to text content of the button
      text = button.textContent?.trim();
    }

    if (!text) {
      throw new Error("Text not found");
    }
    return text;
  });
}

function extractContractOptions(selector: string): string[] {
  const container = document.querySelector(selector);
  if (!container) {
    throw new Error("container not found");
  }

  // Iterate over each button element within the container
  var expButtons = Array.from(container.querySelectorAll("button"));

  // Iterate over each button element
  return expButtons.map((button) => {
    var text = button.textContent;

    if (!text) {
      var spans = Array.from(button.querySelectorAll("span"));

      text = spans.map((s) => s.textContent?.trim()).join(" ");
    }

    if (!text) {
      throw new Error("Text not found");
    }
    return text;
  });
}

function findEarliestDateIndexAfterNDays(
  dateStrings: string[],
  N: number
): number | undefined {
  const currentDate = dayjs();
  const minDate = currentDate.add(N, "day"); // Calculate minimum date N days from today

  let earliestIndex: number | undefined;
  let earliestDate: dayjs.Dayjs | undefined;

  // Iterate through each date string
  dateStrings.forEach((dateString, index) => {
    // Parse the date string assuming format "MMM DD, YYYY"
    const parsedDate = dayjs(dateString, "MMM DD, YYYY");

    // Check if the parsed date is at least N days from today
    if (parsedDate.isAfter(minDate)) {
      // If it's the first valid date or earlier than the current earliestDate, update earliestDate and earliestIndex
      if (!earliestDate || parsedDate.isBefore(earliestDate)) {
        earliestDate = parsedDate;
        earliestIndex = index;
      }
    }
  });

  return earliestIndex;
}

async function setAccount(accountId: string) {
  const accountButton = document.getElementById("account");

  if (!accountButton) {
    throw new Error("Account button not found");
  }

  accountButton.click();

  await new Promise((resolve) => setTimeout(resolve, 100));

  // find the account in the dropdown
  const accountOptions: HTMLButtonElement[] = Array.from(
    document.querySelectorAll('button[role="option"]')
  );

  // Iterate through the buttons
  let targetButton: HTMLButtonElement | undefined = accountOptions.find(
    (button) => {
      const accountNum = button.querySelector(".accountNum")?.textContent;

      return accountNum === `(${accountId})`;
    }
  );

  if (!targetButton) {
    throw new Error("Account not found");
  }

  targetButton.click();
}

async function setSymbol() {
  const searchInput = document.getElementById("symbol_search");
  if (!searchInput) {
    throw new Error("Search input not found");
  }

  searchInput.focus();
  // @ts-ignore
  searchInput.value = ".SPX";

  let event = new Event("input", {
    bubbles: true,
    cancelable: true,
  });
  searchInput.dispatchEvent(event);
  searchInput.click();

  await new Promise((resolve) => setTimeout(resolve, 1000));

  // click on the right option
  const symbolOptions: HTMLButtonElement[] = Array.from(
    document.querySelectorAll('button[role="option"]')
  );

  // Loop through each button
  const spxOption = symbolOptions.find((button) => {
    // Check if the button contains the span with the specified text
    const span = button.querySelector(".option-item");

    return span !== null && span.textContent?.trim() === ".SPX";
  });
  if (!spxOption) {
    throw new Error("Option not found");
  }
  spxOption.click();

  const enterKeyEvent = new KeyboardEvent("keyup", {
    key: "Enter",
    code: "Enter",
    keyCode: 13, // Deprecated, but still widely used
    which: 13, // Deprecated, but still widely used
    bubbles: true, // Ensure the event bubbles up through the DOM
    cancelable: true, // Allow the event to be canceled
  });
  searchInput.dispatchEvent(enterKeyEvent);
}

async function enterOrder(
  borrowData: BorrowData,
  allowedExpDates?: string[] // ["M/D/YYYY"]
): Promise<OrderDetails> {
  const addLeg = document.getElementById("dest-add-leg");
  if (!addLeg) {
    throw new Error("Add leg button not found");
  }

  addLeg.focus();
  addLeg.click();
  addLeg.click();
  addLeg.click();

  let actionDropdownButtons = [];
  let quantityInputs = [];
  let callRadios = [];
  let putRadios = [];
  let expDropdownButtons = [];
  let strikeDropdownButtons = [];

  // Loop to populate arrays for each element type
  for (let i = 0; i <= 3; i++) {
    // Button with ID action_dropdown-i
    const actionButtonId = `action_dropdown-${i}`;
    const actionButton = document.getElementById(actionButtonId);
    if (actionButton) {
      actionDropdownButtons.push(actionButton);
    }

    // Input with ID quantity-i
    const quantityInputId = `quantity-${i}`;
    const quantityInput = document.getElementById(quantityInputId);
    if (quantityInput) {
      quantityInputs.push(quantityInput);
    }

    // Radio inputs with IDs call-i and put-i
    const callRadioId = `call-put-${i}-call`;
    const callRadio = document.getElementById(callRadioId);
    if (callRadio) {
      callRadios.push(callRadio);
    }

    const putRadioId = `call-put-${i}-put`;
    const putRadio = document.getElementById(putRadioId);
    if (putRadio) {
      putRadios.push(putRadio);
    }

    // Button with ID exp_dropdown-i
    const expButtonId = `exp_dropdown-${i}`;
    const expButton = document.getElementById(expButtonId);
    if (expButton) {
      expDropdownButtons.push(expButton);
    }

    // Button with ID strike_dropdown-i
    const strikeButtonId = `strike_dropdown-${i}`;
    const strikeButton = document.getElementById(strikeButtonId);
    if (strikeButton) {
      strikeDropdownButtons.push(strikeButton);
    }
  }

  if (
    actionDropdownButtons.length !== 4 ||
    quantityInputs.length !== 4 ||
    callRadios.length !== 4 ||
    putRadios.length !== 4 ||
    expDropdownButtons.length !== 4 ||
    strikeDropdownButtons.length !== 4
  ) {
    throw new Error("Arrays do not have a length of 4 as expected.");
  }

  // set call and put
  callRadios[0].click();
  callRadios[1].click();
  putRadios[2].click();
  putRadios[3].click();

  selectDropdownOption(actionDropdownButtons[0], "Sell To Open");
  selectDropdownOption(actionDropdownButtons[1], "Buy To Open");
  selectDropdownOption(actionDropdownButtons[2], "Buy To Open");
  selectDropdownOption(actionDropdownButtons[3], "Sell To Open");

  await new Promise((resolve) => setTimeout(resolve, 1000));

  // get all expirations
  expDropdownButtons[0].click();

  const expirationDates = extractOptions(
    'div[aria-labelledby="exp_dropdown_label-1"]'
  ).filter((date) => {
    // filter for monthly expiration dates (provided by the server)
    if (!allowedExpDates) {
      return true;
    }

    return allowedExpDates.includes(
      dayjs(date.replace("PM", "").replace("AM", "").trim()).format("M/D/YYYY")
    );
  });

  var earliestDateIndex: number | undefined = 0;

  earliestDateIndex = findEarliestDateIndexAfterNDays(
    expirationDates.map((date) =>
      date.replace("PM", "").replace("AM", "").trim()
    ),
    borrowData.periodInDays
  );

  const expDateInSchwabFormat = dayjs(
    expirationDates[earliestDateIndex ?? 0]
      .replace("PM", "")
      .replace("AM", "")
      .trim(),
    "MMM DD, YYYY hh:mm"
  ).format("MM/DD/YYYY");

  for (let i = 0; i < 4; i++) {
    selectDropdownOption(
      expDropdownButtons[i],
      expirationDates[earliestDateIndex ?? 0]
    );
  }

  await new Promise((resolve) => setTimeout(resolve, 1000));

  // get all strikes
  strikeDropdownButtons[0].click();
  await new Promise((resolve) => setTimeout(resolve, 2000));

  // example: " 5,900.00 "
  const strikeTexts = extractOptions(
    'div[aria-labelledby="strike_dropdown_label-1"]'
  );
  const parsedStrikes = strikeTexts.map((strikeText) =>
    parseFloat(strikeText.replace(/["',]/g, ""))
  );

  var strikePrice1Idx = 0;
  var strikePrice2Idx = 0;
  var limitPrice = 0;
  var boxSize = 0;

  const boxSizeTarget = await calculateBoxSpreadTargetSize(
    borrowData.borrowAmount,
    borrowData.periodInDays
  );

  const { quantity, strikePrice2Target, strikePrice1 } =
    getStrikePriceTargets(boxSizeTarget);

  quantityInputs.forEach((input) => setInput(input, quantity.toString()));

  strikePrice1Idx = parsedStrikes.indexOf(strikePrice1);

  strikePrice2Idx = findNearestNumberIdx(parsedStrikes, strikePrice2Target);
  const strikePrice2 = parsedStrikes[strikePrice2Idx];

  boxSize = (strikePrice2 - strikePrice1) * 100 * quantity;

  // Set limit order and price
  limitPrice = calculatePrice(
    borrowData.periodInDays,
    strikePrice2 - strikePrice1,
    settlementDateDuration(expDateInSchwabFormat)
  );

  selectDropdownOption(strikeDropdownButtons[0], strikeTexts[strikePrice1Idx]);

  await new Promise((resolve) => setTimeout(resolve, 500));

  selectDropdownOption(strikeDropdownButtons[1], strikeTexts[strikePrice2Idx]);

  await new Promise((resolve) => setTimeout(resolve, 500));

  selectDropdownOption(strikeDropdownButtons[2], strikeTexts[strikePrice1Idx]);

  await new Promise((resolve) => setTimeout(resolve, 500));

  selectDropdownOption(strikeDropdownButtons[3], strikeTexts[strikePrice2Idx]);

  // wait for fidelity to calculate max loss / gain
  await new Promise((resolve) => setTimeout(resolve, 2000));

  const orderTypeButton = document.getElementById("ordertype-dropdown");
  if (!orderTypeButton) {
    throw new Error("Order type button not found");
  }
  selectDropdownOption(orderTypeButton, "Net Credit");

  const limitInput = document.getElementById("dest-limitPrice");
  if (!limitInput) {
    throw new Error("Limit input not found");
  }
  setInput(limitInput, limitPrice.toFixed(2));

  return {
    expirationDate: expDateInSchwabFormat,
    upfrontCash: limitPrice * 100 * quantity,
    repaymentAmount: boxSize,
    accountId: borrowData.accountId,
    accountName: borrowData.accountName,
  };
}

async function enterRepayOrder(repayData: RepayData): Promise<OrderDetails> {
  const addLeg = document.getElementById("dest-add-leg");
  if (!addLeg) {
    throw new Error("Add leg button not found");
  }

  addLeg.focus();
  addLeg.click();
  addLeg.click();
  addLeg.click();

  let actionDropdownButtons = [];
  let quantityInputs = [];
  let ownedContracts = [];

  // Loop to populate arrays for each element type
  for (let i = 1; i <= 4; i++) {
    // Button with ID action_dropdown-i
    const actionButtonId = `action_dropdown-${i}`;
    const actionButton = document.getElementById(actionButtonId);
    if (actionButton) {
      actionDropdownButtons.push(actionButton);
    }

    // Input with ID quantity-i
    const quantityInputId = `quantity-${i}`;
    const quantityInput = document.getElementById(quantityInputId);
    if (quantityInput) {
      quantityInputs.push(quantityInput);
    }
  }

  if (actionDropdownButtons.length !== 4 || quantityInputs.length !== 4) {
    throw new Error("Arrays do not have a length of 4 as expected.");
  }

  selectDropdownOption(actionDropdownButtons[0], "Buy To Close");
  selectDropdownOption(actionDropdownButtons[1], "Sell To Close");
  selectDropdownOption(actionDropdownButtons[2], "Sell To Close");
  selectDropdownOption(actionDropdownButtons[3], "Buy To Close");

  await new Promise((resolve) => setTimeout(resolve, 1000));

  for (let i = 1; i <= 4; i++) {
    // Input with ID quantity-i
    const dropdownIds = `owned-contracts-dropdown-${i}`;
    const button = document.getElementById(dropdownIds);
    if (button) {
      ownedContracts.push(button);
    }
  }

  ownedContracts[0].click();

  const contractOptions = extractContractOptions(
    'div[aria-labelledby="ownedcontract_dropdown_label-1"]'
  );

  await new Promise((resolve) => setTimeout(resolve, 500));

  const filteredContracts = contractOptions.filter(
    (contract) =>
      contract
        .toLowerCase()
        .includes(repayData.expirationDate.replace(",", "").toLowerCase()) &&
      contract.includes("SPX") &&
      (contract.includes(repayData.strikePrice1) ||
        contract.includes(repayData.strikePrice2))
  );

  if (filteredContracts.length !== 4) {
    throw new Error("Contracts not found");
  }

  for (let i = 0; i <= 3; i++) {
    selectDropdownOption(ownedContracts[i], filteredContracts[i]);
  }

  var limitPrice = 0;
  var boxSize = 0;
  const expDateInSchwabFormat = dayjs(repayData.expirationDate).format(
    "M/D/YYYY"
  );

  // Set limit order and price
  limitPrice = calculatePrice(
    settlementDateDuration(expDateInSchwabFormat),
    parseFloat(repayData.strikePrice2) - parseFloat(repayData.strikePrice1),
    settlementDateDuration(expDateInSchwabFormat)
  );

  boxSize =
    (parseFloat(repayData.strikePrice2) - parseFloat(repayData.strikePrice1)) *
    100;

  // wait for fidelity to calculate max loss / gain
  await new Promise((resolve) => setTimeout(resolve, 2000));

  const orderTypeButton = document.getElementById("ordertype-Custom-dropdown");
  if (!orderTypeButton) {
    throw new Error("Order type button not found");
  }
  selectDropdownOption(orderTypeButton, "Net Debit");

  const limitInput = document.getElementById("dest-limitPrice");
  if (!limitInput) {
    throw new Error("Limit input not found");
  }
  setInput(limitInput, limitPrice.toFixed(2));

  return {
    expirationDate: expDateInSchwabFormat,
    upfrontCash: limitPrice * 100,
    repaymentAmount: boxSize,
    accountId: repayData.accountId,
    accountName: repayData.accountName,
    costBasis: repayData.costBasis,
  };
}

export async function executeFidelityTrade(
  borrowData: BorrowData,
  expirationDates?: string[]
) {
  try {
    // Step 1: set account
    await setAccount(borrowData.accountId);

    // Step 2: input symbol and make it 4 legs
    await setSymbol();

    // Step 3: input order details
    const orderDetails = await enterOrder(borrowData, expirationDates);

    // Step 4: submit order
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const previewButton = document.getElementById("previewButton");
    if (!previewButton) {
      throw new Error("Preview button not found");
    }
    previewButton.click();

    // Step 5: update the chrome extension by sending it a message
    const response = await chrome.runtime.sendMessage({
      platform: "fidelity",
      action: "review_trade",
      data: orderDetails,
    });
    console.log("response", response);
  } catch (error) {
    scope.captureException(error);
  }
}

export async function executeFidelityRepay(repayData: RepayData) {
  try {
    // Step 1: set account
    await setAccount(repayData.accountId);

    // Step 2: input symbol and make it 4 legs
    await setSymbol();

    // Step 3: input order details
    const orderDetails = await enterRepayOrder(repayData);

    // Step 4: submit order
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const previewButton = document.getElementById("previewButton");
    if (!previewButton) {
      throw new Error("Preview button not found");
    }
    previewButton.click();

    // Step 5: update the chrome extension by sending it a message
    const response = await chrome.runtime.sendMessage({
      platform: "fidelity",
      action: "review_repay",
      data: orderDetails,
    });
    console.log("response", response);
  } catch (error) {
    scope.captureException(error);
  }
}
