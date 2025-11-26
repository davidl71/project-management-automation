import dayjs from "dayjs";
import {
  getBestOptionsForLoanDuration,
  getInterestRateBySymbol,
} from "./optionsPicker";
import { getSettlementDate } from "./date";

export function injectScript(file: any, node: any) {
  var th = document.getElementsByTagName(node)[0];
  var s = document.createElement("script");
  s.setAttribute("type", "text/javascript");
  s.setAttribute("src", file);
  th.appendChild(s);
}

export function selectOption(element: any, value: any) {
  element.value = value;
  element.dispatchEvent(
    new Event("change", {
      bubbles: true,
      cancelable: true,
    })
  );
}

export function findEarliestDateIndexAfterNdays(dates: string[], N: number) {
  const currentDate = new Date();
  let earliestDateIndex = -1;

  for (let i = 0; i < dates.length; i++) {
    const dateString = dates[i];
    const parts = dateString.split("/");
    const date = new Date(
      parseInt(parts[2]),
      parseInt(parts[0]) - 1,
      parseInt(parts[1])
    ); // Month is 0-based

    const daysDifference = Math.floor(
      (date.valueOf() - currentDate.valueOf()) / (1000 * 60 * 60 * 24)
    );

    if (
      daysDifference >= N &&
      (earliestDateIndex === -1 || date < new Date(dates[earliestDateIndex]))
    ) {
      earliestDateIndex = i;
    }
  }

  return earliestDateIndex;
}

export function findIndexSmallestLargerNumber(numbers: number[], N: number) {
  let smallestLargerNumberIndex = -1;

  for (let i = 0; i < numbers.length; i++) {
    if (
      numbers[i] > N &&
      (smallestLargerNumberIndex === -1 ||
        numbers[i] < numbers[smallestLargerNumberIndex])
    ) {
      smallestLargerNumberIndex = i;
    }
  }

  return smallestLargerNumberIndex;
}

export function findNearestNumberIdx(numbers: number[], N: number) {
  // find the nearest number in the array
  let nearestNumberIndex = 0;
  let nearestNumber = numbers[0];
  let minDiff = Math.abs(nearestNumber - N);

  for (let i = 1; i < numbers.length; i++) {
    const diff = Math.abs(numbers[i] - N);
    if (diff < minDiff) {
      minDiff = diff;
      nearestNumber = numbers[i];
      nearestNumberIndex = i;
    }
  }

  return nearestNumberIndex;
}

// expirationDate format: M/D/YYYY
export async function calculateBoxSpreadTargetSize(
  borrowAmount: number,
  periodRequested: number
) {
  const spxContractsResult = await chrome.storage.local.get(["spx_contracts"]);
  if (spxContractsResult.spx_contracts) {
    const { data, timestamp } = spxContractsResult.spx_contracts;
    // check if the timestamp is over 1 days old
    if (timestamp && Date.now() - timestamp <= 24 * 60 * 60 * 1000 && data) {
      const spxContracts = data;
      return calculateBoxSpreadTargetSizeWithContractDate(
        borrowAmount,
        periodRequested,
        spxContracts
      );
    }
  }

  console.log("fall back to old way of calculation; no spx_contracts data");

  // fallback to old way of calculation
  return borrowAmount;
}

export function calculateBoxSpreadTargetSizeWithContractDate(
  borrowAmount: number,
  periodInDays: number, // requested period
  spxContracts: any // chrome.storage.spx_contracts
) {
  const optionsToUse = getBestOptionsForLoanDuration(periodInDays);
  if (optionsToUse == null) {
    throw new Error("No options to use");
  }

  const { symbol, date } = optionsToUse;
  const rates = getInterestRateBySymbol(symbol);
  if (rates == null) {
    throw new Error(`No interest rate data for symbol ${symbol}`);
  }

  const { bid, ask, mid } = rates;

  const period = Math.abs(
    dayjs(getSettlementDate(date)).diff(getSettlementDate(new Date()), "days")
  ); // loan duration

  const expDateString = dayjs(date).format("M/D/YYYY");

  const idealBoxSpreadSize = borrowAmount * Math.pow(1 + mid / 360, period);

  const boxQuantity = Math.ceil(idealBoxSpreadSize / 200000);

  if (spxContracts[expDateString]) {
    // find box spread that is closest to the ideal size
    const strikes = spxContracts[expDateString].filter((s: number) => s > 5000); // [5000, 5050, ...]
    const boxSizeOptions = strikes.map((s: number) => 100 * (s - 5000));

    const actualBoxSize = boxSizeOptions.reduce((prev: number, curr: number) =>
      Math.abs(curr - idealBoxSpreadSize / boxQuantity) <
      Math.abs(prev - idealBoxSpreadSize / boxQuantity)
        ? curr
        : prev
    );

    return actualBoxSize * boxQuantity;
  } else {
    // fallback if we cannot fetch from server
    console.warn("fall back to hard-coded calculation");

    // we will show strike difference of $5. In practice, it may not be possible since small strikes
    // are only available near the SPX index value.
    return Math.floor(idealBoxSpreadSize / 500) * 500;
  }
}
