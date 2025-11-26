import dayjs from "dayjs";

function getMidnight(date: Date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

// MM/DD/YYYY
// calculate the number of days between the input date and today for settlement purposes
// handle T + 1 as needed
export function settlementDateDuration(dateString: string) {
  // Get today's date
  const today = new Date();

  const optionSettlement = getSettlementDate(
    dayjs(dateString, "MM/DD/YYYY").toDate()
  );
  const tradeSettlement = getSettlementDate(getMidnight(today));

  const period = Math.abs(
    dayjs(optionSettlement).diff(tradeSettlement, "days")
  ); // loan duration

  return period;
}

// MM/DD/YYYY to M/D/YYYY
export function removeDateLeadingZeros(dateString: string) {
  // Parse the date string using dayjs
  const date = dayjs(dateString, "MM/DD/YYYY");

  // Format the date without leading zeros
  const formattedDate = date.format("M/D/YYYY");

  return formattedDate;
}

const holidays = [
  "01/01/2025", // New Year's Day
  "01/20/2025", // Martin Luther King Jr. Day
  "02/17/2025", // Presidents' Day
  "04/18/2025", // Good Friday (Bond Market)
  "05/26/2025", // Memorial Day
  "06/19/2025", // Juneteenth National Independence Day
  "07/04/2025", // Independence Day
  "09/01/2025", // Labor Day
  "10/13/2025", // Columbus Day (Bond Market)
  "11/11/2025", // Veterans Day (Bond Market)
  "11/27/2025", // Thanksgiving Day
  "12/25/2025", // Christmas Day
  "01/01/2026", // New Year's Day
  "01/19/2026", // Martin Luther King Jr. Day
  "02/16/2026", // Presidents' Day
  "04/03/2026", // Good Friday (Bond Market)
  "05/25/2026", // Memorial Day
  "06/19/2026", // Juneteenth National Independence Day
  "07/03/2026", // Independence Day (Observed, as July 4 is a Saturday)
  "09/07/2026", // Labor Day
  "10/12/2026", // Columbus Day (Bond Market)
  "11/11/2026", // Veterans Day (Bond Market)
  "11/26/2026", // Thanksgiving Day
  "12/25/2026", // Christmas Day
];

function addBusinessDays(startDate: Date, days: number): Date {
  let currentDate = new Date(startDate);

  while (days > 0) {
    currentDate.setDate(currentDate.getDate() + 1);
    // Check if current day is a business day (not a Saturday or Sunday)
    if (
      currentDate.getDay() !== 0 &&
      currentDate.getDay() !== 6 &&
      !holidays.includes(dayjs(currentDate).format("MM/DD/YYYY"))
    ) {
      days--;
    }
  }

  return currentDate;
}

export function getSettlementDate(
  tradeDate: Date,
  settlementDays: number = 1
): Date {
  return addBusinessDays(tradeDate, settlementDays);
}
