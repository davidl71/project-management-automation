interface BoxGroup {
  expirationDate: string;
  options: any[];
  boxSize: number;
  costBasisSum: number; // this is usually a negative number
  quantity: number;
  strikePrice1: number;
  strikePrice2: number; // strikePrice2 > strikePrice1
}

function getExpDateFidelity(description: string): string | null {
  const datePattern = /([A-Za-z]{3,4})\s(\d{1,2})\s(\d{4})/;
  const match = description.match(datePattern);

  if (match) {
    const [, month, day, year] = match;
    const dateString = `${month} ${day}, ${year}`;
    return dateString;
  } else {
    return null;
  }
}

function getStrikePriceFidelity(description: string): number | null {
  const segments = description.split(" ");

  if (segments.length < 6) {
    return null;
  }

  const strikePrice = segments[4];

  return Number(strikePrice.replace(/[$,]/g, ""));
}

function extractBoxInfoFromFidelityPositions(positions: any[]): BoxGroup[] {
  /* Sample:
  [
    {
      "symbol": "-SPXW240830P5000",
      "securityType": "Option",
      "securityDescription": "SPXW AUG 30 2024 $5,000 PUT",
      "cusip": "7053959IG",
      "quantity": 1,
      "isBasketed": false,
      "securityDetail": {
        "brokerageHoldingType": "Margin",
        "isMargin": true,
        "isEligibleForLots": true
      },
      "costBasisDetail": {
        "avgCostPerShare": 8.51
      }
    },
  ]
  */

  const spxOptions = positions.filter(
    (p) =>
      p?.securityType === "Option" && p?.securityDescription?.startsWith("SPX")
  );

  const expirationDates = spxOptions.map((p) =>
    getExpDateFidelity(p.securityDescription)
  );

  // group by the options by expiration date
  const groupedByExpiration = spxOptions.reduce((acc, p) => {
    const expirationDate = expirationDates.shift();
    if (expirationDate) {
      // @ts-ignore
      if (!acc[expirationDate]) {
        // @ts-ignore
        acc[expirationDate] = [];
      }

      // @ts-ignore
      acc[expirationDate].push(p);
    }

    return acc;
  }, {});

  // we only want groups that have 4 options and the quantity add up to 0
  const boxGroups = Object.values(groupedByExpiration).filter((group: any) => {
    const totalQuantity = group
      .map((p: any) => p?.quantity)
      .reduce((a: any, b: any) => a + b, 0);

    const strikePrices = group.map((p: any) =>
      getStrikePriceFidelity(p.securityDescription)
    );

    const strikePriceSet = new Set(strikePrices);

    return (
      group.length === 4 && totalQuantity === 0 && strikePriceSet.size === 2
    );
  });

  // adding the cost basis together
  const results = boxGroups.map((group: any) => {
    const costBasisSum = group
      .map((p: any) => p?.costBasisDetail?.avgCostPerShare * p?.quantity * 100)
      .reduce((a: any, b: any) => a + b, 0);

    const expiration = getExpDateFidelity(group[0]?.securityDescription);

    const strikePrices = group.map((p: any) =>
      getStrikePriceFidelity(p.securityDescription)
    );

    const strikePriceGap =
      Math.max(...strikePrices) - Math.min(...strikePrices);

    return {
      expirationDate: expiration!,
      options: group,
      boxSize: strikePriceGap * 100 * Math.abs(group[0]?.quantity),
      costBasisSum: costBasisSum,
      quantity: Math.abs(group[0]?.quantity),
      strikePrice1: Math.min(...strikePrices),
      strikePrice2: Math.max(...strikePrices),
    };
  });

  return results;
}

// fidelityBalance is the object stored in chrome storage
export function extractFidelityMarginInfo(fidelityBalance: any) {
  const results = Object.keys(fidelityBalance).map((acctNum) => {
    const positions = fidelityBalance[acctNum]?.positions;
    const boxGroups = extractBoxInfoFromFidelityPositions(positions);

    console.log("Fidelity box groups", boxGroups);

    const boxSumBalance = boxGroups
      .map((group) => -1 * group.costBasisSum)
      .reduce((a, b) => a + b, 0);

    const balance =
      fidelityBalance[acctNum]?.brokerageAcctDetail?.recentBalanceDetail;
    const acctDetails = fidelityBalance[acctNum]?.acctDetails;

    var marginBalance = 0;

    const marketVal = balance?.acctValDetail?.marketVal;
    const netWorth = balance?.acctValDetail?.netWorth;

    if (marketVal && netWorth) {
      // margin debit balance is the amount that you owe to the broker
      // when there is excessive cash in the account, it shows up as a negative number
      marginBalance = Math.max(0, marketVal - netWorth);
    }

    var withdrawMargin = 0;
    if (
      balance?.availableToWithdrawDetail?.cashWithMargin !== undefined &&
      balance?.availableToWithdrawDetail?.cashOnly !== undefined
    ) {
      withdrawMargin =
        balance?.availableToWithdrawDetail?.cashWithMargin -
        balance?.availableToWithdrawDetail?.cashOnly;
    }

    console.log("Fidelity margin withdraw capabilities", withdrawMargin);

    return {
      isIra: acctDetails?.acctTypesIndDetail?.isRetirement,
      marginDebitBalance: marginBalance,
      accountId: acctNum,
      accountName: acctNum,
      withdrawTotal: balance?.availableToWithdrawDetail?.cashWithMargin,
      withdrawMargin: withdrawMargin,
      boxSpreadDebitBalance: boxSumBalance,

      // box spread details below
      boxExpirationDate: boxGroups[0]?.expirationDate,
      boxQuantity: boxGroups[0]?.quantity,
      strikePrice1: boxGroups[0]?.strikePrice1,
      strikePrice2: boxGroups[0]?.strikePrice2,
      costBasis: boxGroups[0]?.costBasisSum,

      allBoxGroups: boxGroups,
    };
  });

  // sort the result to put the ones with isIra = false first
  return results.sort((a, b) => {
    if (a.isIra && !b.isIra) {
      return 1;
    }

    if (!a.isIra && b.isIra) {
      return -1;
    }

    return 0;
  });
}

export function extractSchwabMarginInfos(schwabBalance: any[]) {
  const results = schwabBalance.map((balance) => {
    const optionsLevel = balance?.optionDetails?.optionsApprovalCode; // we want "2" or "3"

    var borrowedViaBox = 0.0;
    var boxExpirationDate: string | undefined = undefined;
    var boxQuantity: number | undefined = undefined;
    var strikePrice1: number | undefined = undefined;
    var strikePrice2: number | undefined = undefined;
    var costBasis: number | undefined = undefined;

    const holdings = balance?.holdings?.find(
      (group: any) => group.groupName === "Indices"
    );

    if (holdings) {
      const positions = holdings.positions.filter(
        (p: any) => p?.symbolDetail?.symbol === "$SPX" // SPX options only
      );

      // Entries example:
      /*
      {
          "quantity": -1,
          "quantityBeforeSplit": -1,
          "marginRequirement": 0,
          "intrinsicValue": 667.1999999999998,
          "inTheMoneyValue": "ITM",
          "percentageOfAccount": -6.77,
          "maturityDate": "07/19/2024",
          "maturityDuration": 3,
          "symbolDetail": {
              "symbol": "SPX 07/19/2024 5000.00 C",
              "description": "CALL S & P 500 INDEX $5000 EXP 07/19/24",
              "quoteSymbol": "SPX   240719C05000000",
              "defaultSymbol": "SPX   240719C05000000",
              "underlyingSymbol": "$SPX",
              "underlyingDescription": "S & P 500 INDEX",
              "schwabSecurityId": 90914410,
              "underlyingSchwabSecurityId": 1819771877,
              "isLink": true,
              "isOptionIndices": true,
              "securityGroupCode": "OPTION",
              "ruleSetSuffix": 0,
              "accountingRuleCode": 6,
              "positionType": 0,
              "securityType": 4,
              "symbolForDetailedQuotes": "SPX   240719C05000000"
          },
          "marginDetail": {
              "pegAmount": 0,
              "nakedQuantity": 0,
              "nakedRequirementAmount": 0,
              "spreadQuantity": -1,
              "spreadRequirementAmount": 0,
              "strangleQuantity": 0,
              "strangleRequirementAmount": 0,
              "coverQuantity": 0
          },
          "marginOptionStrategy": [
              {
                  "quantity": -1,
                  "name": "SBXS",
                  "sequence": 1,
                  "displayOptionRequirement": "N",
                  "isSequence": true
              }
          ],
      }
      */

      if (positions[0]) {
        const sboxPositions =
          positions[0].childOptionHoldings?.filter((leg: any) => {
            if (leg?.marginOptionStrategy) {
              return leg?.marginOptionStrategy[0]?.name === "SBXS";
            } else {
              return false;
            }
          }) ?? [];

        // [5000.00, 5000.00, 5100.00, 5100.00]
        const strikePrices = sboxPositions
          .map((leg: any) => {
            const symbol = leg?.symbolDetail?.symbol;

            if (symbol) {
              const parts = symbol.split(" ");
              const strike = parts[2]; // 5000.00
              return parseFloat(strike);
            } else {
              return null;
            }
          })
          .filter((x: any) => x !== null)
          .sort();

        costBasis = sboxPositions
          .map((leg: any) => leg?.costDetail?.costBasisDetail?.costBasis)
          .filter((x: any) => x !== null)
          .reduce((a: any, b: any) => a + b, 0);

        if (sboxPositions.length > 0 && strikePrices.length >= 4) {
          strikePrice1 = strikePrices[0];
          strikePrice2 = strikePrices[strikePrices.length - 1];

          if (strikePrice1 !== strikePrice2) {
            boxExpirationDate = sboxPositions[0]?.maturityDate;
            boxQuantity = Math.abs(sboxPositions[0]?.quantity);
          }
        }

        // return the total mark-to-market value
        const marketValues = sboxPositions.map(
          (leg: any) => leg?.priceDetail?.marketValue
        );

        const sum = marketValues.reduce((a: any, b: any) => a + b, 0);

        borrowedViaBox = -sum;
      }
    }

    return {
      isIra: balance?.info?.isIra,
      marginDebitBalance: balance?.marginsInfo?.balanceSubjectInterest,
      accountId: balance?.accountId,
      accountName: balance?.accountNickname,
      withdrawTotal: balance?.fundsAvailable?.withdrawFunds?.cashBorrowing,
      withdrawMargin: balance?.fundsAvailable?.withdrawFunds?.borrowing,
      optionsLevel: optionsLevel,
      boxSpreadDebitBalance: borrowedViaBox,
      boxExpirationDate: boxExpirationDate,
      boxQuantity: boxQuantity,
      strikePrice1: strikePrice1,
      strikePrice2: strikePrice2,
      costBasis: costBasis,
    };
  });

  // sort the result to put the ones with isIra = false first
  return results.sort((a, b) => {
    if (a.isIra && !b.isIra) {
      return 1;
    }

    if (!a.isIra && b.isIra) {
      return -1;
    }

    return 0;
  });
}
