// given a desired loan duration (starting from today), find the best SPX options contracts expiration date

const expirationDates: {
  [key: string]: Date;
} = {
  "SPX 20DEC24": new Date(2024, 11, 20),
  "SPX 17JAN25": new Date(2025, 0, 17),
  "SPX 21FEB25": new Date(2025, 1, 21),
  "SPX 21MAR25": new Date(2025, 2, 21),
  "SPX 17APR25": new Date(2025, 3, 17),
  "SPX 16MAY25": new Date(2025, 4, 16),
  "SPX 20JUN25": new Date(2025, 5, 20),
  "SPX 18JUL25": new Date(2025, 6, 18),
  "SPX 15AUG25": new Date(2025, 7, 15),
  "SPX 19SEP25": new Date(2025, 8, 19),
  "SPX 17OCT25": new Date(2025, 9, 17),
  "SPX 21NOV25": new Date(2025, 10, 21),
  "SPX 19DEC25": new Date(2025, 11, 19),
  "SPX 16JAN26": new Date(2026, 0, 16),
  "SPX 20FEB26": new Date(2026, 1, 20),
  "SPX 20MAR26": new Date(2026, 2, 20),
  "SPX 18JUN26": new Date(2026, 5, 18),
  "SPX 18DEC26": new Date(2026, 11, 18),
  "SPX 17DEC27": new Date(2027, 11, 17),
  "SPX 15DEC28": new Date(2028, 11, 15),
  "SPX 21DEC29": new Date(2029, 11, 21),
  "SPX 20DEC30": new Date(2030, 11, 20),
};

// manually updated 2/23/2025
// [bid, ask, mid]
const interestRate: {
  [expirationDays: number]: number[];
} = {
  30: [0.044, 0.044, 0.044],
  112: [0.044, 0.044, 0.044],
  322: [0.042, 0.042, 0.042],
  500: [0.042, 0.042, 0.042],
  800: [0.043, 0.043, 0.043],
  1100: [0.042, 0.042, 0.042],
  1200: [0.042, 0.042, 0.042],
};

export function differenceInDays(date1: Date, date2: Date): number {
  const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
  const diffInTime = date2.getTime() - date1.getTime();
  return Math.round(diffInTime / oneDay);
}

// TODO: refactor to use chrome.storage.local.spx_contracts
export function getInterestRateBySymbol(symbol: string): {
  bid: number;
  ask: number;
  mid: number;
} | null {
  const contractDate = expirationDates[symbol];
  if (!contractDate) {
    return null;
  }

  const days = Math.abs(differenceInDays(new Date(Date.now()), contractDate));

  let closestKey: number = Number(Object.keys(interestRate)[0]);
  let minDiff = Math.abs(closestKey - days);

  for (const key in interestRate) {
    const diff = Math.abs(Number(key) - days);
    if (diff < minDiff) {
      minDiff = diff;
      closestKey = Number(key);
    }
  }

  const rates = interestRate[closestKey];

  return {
    bid: rates[0],
    ask: rates[1],
    mid: rates[2],
  };
}

export function getBestOptionsForLoanDuration(
  loanDuration: number
): { date: Date; symbol: string } | null {
  const current = Date.now();

  const daysFromExpirationDate = Object.entries(expirationDates)
    .map(([contract, expirationDate]) => {
      return {
        contract,
        days: differenceInDays(new Date(current), expirationDate),
      };
    })
    .filter((contract) => contract.days >= loanDuration)
    .sort((a, b) => a.days - b.days);

  if (daysFromExpirationDate.length === 0) {
    return null;
  }

  const bestContract = daysFromExpirationDate[0];

  return {
    symbol: bestContract.contract,
    date: expirationDates[bestContract.contract],
  };
}

export function calculatePrice(
  periodInDays: number, // this is used to search for the options contract by expiration date
  boxStrikeDifference: number,
  period: number // period in days: this needs to be between the settlement days
) {
  const optionsToUse = getBestOptionsForLoanDuration(periodInDays);
  if (optionsToUse == null) {
    console.error("No options to use");

    throw new Error("No options to use");
  }

  const { symbol, date } = optionsToUse;
  const rates = getInterestRateBySymbol(symbol);
  if (rates == null) {
    console.error("No interest rate data for symbol", symbol);

    throw new Error("No interest rate data for symbol");
  }
  const { bid, ask, mid } = rates;

  const actualBoxSpreadSize = boxStrikeDifference * 100;
  const upfrontCash = actualBoxSpreadSize / Math.pow(1 + mid / 360, period);

  const limitOrderTarget = upfrontCash / 100.0;

  // round limit order to the cloest .05
  const limitOrder = Math.ceil(limitOrderTarget * 20) / 20;
  return limitOrder;
}
