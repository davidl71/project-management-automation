// try to load the fidelity balance
console.log("load schwab balance");

const extensionId = "goafkfbcophbmilleaooddlklhjmeifb";

async function getBearerToken() {
  const resp = await fetch(
    "https://client.schwab.com/api/auth/authorize/scope/api",
    { method: "GET" }
  );
  if (resp.status !== 200) {
    console.log("Not able to get bearer token. Status: ", resp.status);
    throw new Error("Not able to get bearer token. Status: ", resp.status);
  }
  /*
  {
      "token": "I0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.RvGvAXyLm6MdEuzI51hZChrZB_k81szWFQNjAuaKwnU@",
      "time": 1573 // seconds
  }
  */
  const json = await resp.json();
  return json.token;
}

async function getAccounts(bearerToken) {
  const resp = await fetch(
    "https://ausgateway.schwab.com/api/is.Balances/V1/Balances/accounts/accounts-details",
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${bearerToken}`,
        "Schwab-Channelcode": window["Api-context"].channelCode,
        "Schwab-Client-Appid": "AD00002298",
        "Schwab-Client-Correlid": window["Api-context"].correlationId,
        "Schwab-Clientapp-Name": "Balances",
        "Schwab-Env": "DEFAULT",
        "Schwab-Environment": "DEFAULT",
        "Schwab-Environment-Region": "", // This key was present but with no value given
        "Schwab-Resource-Version": "1",
      },
    }
  );
  if (resp.status !== 200) {
    console.log("Not able to get bearer token. Status: ", resp.status);
    throw new Error("Not able to get bearer token. Status: ", resp.status);
  }
  /*
  {
    "accountsData": {
        "accountDetails": [
            {
                "accountType": "S1",
                "groupName": "CUSTACCS",
                "type": "Brokerage",
                "encodedAccountId": null,
                "isEmployeeBranch": false,
                "id": "25699585",
                "nickName": "Converge Fashion LLC",
                "isIncludeInList": true,
                "isSPC": false
            },
          ]
        }
  }
  */
  const json = await resp.json();
  const accountDetails = json.accountsData.accountDetails.filter(
    (acct) => acct.type === "Brokerage"
  );

  return accountDetails;
}

async function getSchwabBalances(bearerToken, accounts) {
  const accountIds = accounts.map((acct) => acct.id).join(",");

  const resp = await fetch(
    `https://ausgateway.schwab.com/api/is.Balances/V1/Balances/balances/brokerage?selectionType=Brokerage`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${bearerToken}`,
        "Schwab-Channelcode": window["Api-context"].channelCode,
        "Schwab-Client-Appid": "AD00002298",
        "Schwab-Client-Correlid": window["Api-context"].correlationId,
        "Schwab-Client-Ids": accountIds,
        "Schwab-Clientapp-Name": "Balances",
        "Schwab-Env": "DEFAULT",
        "Schwab-Environment": "DEFAULT",
        "Schwab-Environment-Region": "", // This key was present but with no value given
        "Schwab-Resource-Version": "1",
      },
    }
  );
  if (resp.status !== 200) {
    console.log("Not able to get balance. Status: ", resp.status);
    throw new Error("Not able to get balance. Status: ", resp.status);
  }
  const json = await resp.json();

  /*
  {
    "brokerageAccountList": [
        {
            "dayChange": -62210.35,
            "dayChangePercent": -6.85,
            "encryptedAccountId": "OqBgVbVAhfLZZ0s7gPloKmw8dZ0IIla6j20IdOZqj8c=",
            "dayChangePercentRender": -0.0685,
            "accountId": "95634901",
            "accountNickname": "Living Trust",
            "bankSweepLabel": null,
            "total": 845554.47,
            "marketValue": 836614.21,
            "totalIncludingFutures": 0,
            "cashInvestments": {
                "total": 8940.26,
                "totalIncludingFutures": null,
                "insuredBankSweep": 0,
                "sweepMoneyMarketFund": 0,
                "schwabBankSweepFeature": 0,
                "bankSweepLabel": "Bank Sweep Feature",
                "sweeps": [],
                "purchasedMmf": [],
                "purchasedMmfTotal": 0,
                "cashBalance": 0,
                "marginBalance": 8940.26,
                "isBankSweepEligible": false
            },
            "investments": {
                "total": 836614.21,
                "securitiesMarketValue": 905244.21,
                "optionsMarketValue": -68630,
                "securityShort": {
                    "nonMargin": 0,
                    "margin": 0,
                    "total": 0
                },
                "securityLong": {
                    "nonMargin": 0,
                    "margin": 905244.21,
                    "total": 905244.21
                },
                "optionsShort": {
                    "nonMargin": 0,
                    "margin": -176260,
                    "total": -176260
                },
                "optionsLong": {
                    "nonMargin": 0,
                    "margin": 107630,
                    "total": 107630
                }
            },
            "fundsAvailable": {
                "tradeFunds": {
                    "cashInvestments": 8940.26,
                    "cashInvestmentsWithFutures": 8940.26,
                    "settled": 470995,
                    "settledFutures": 470995,
                    "cashBorrowing": 941990,
                    "cashBorrowingWithFutures": 941990,
                    "sma": 470995,
                    "dayBuyPower": 2716446,
                    "dayBuyPowerWithFutures": 2716446,
                    "availableToDayTrade": 2716446
                },
                "withdrawFunds": {
                    "cashInvestments": 8940.26,
                    "cashInvestmentsWithFutures": 8940.26,
                    "cashHeld": 0,
                    "cashBorrowing": 470994.26,
                    "cashBorrowingWithFutures": 470994.26,
                    "moneyDue": 0,
                    "moneyDueRender": "$0.00",
                    "borrowing": 462054
                }
            },
            "fundsDetails": {
                "total": 460.76,
                "balance": 460.76,
                "accountId": "440025659150",
                "accountType": "Savings",
                "serviceError": false,
                "errorCode": null,
                "baqsServiceError": false,
                "accountStatus": "Active",
                "availableBalance": 460.76,
                "holdTotal": 0,
                "interestPaidPreviousYear": 0.41,
                "interestPaidYearToDate": 0.57,
                "interestRate": 0.45,
                "interestYield": 0.45,
                "minimumPegAmount": 0,
                "earnedThisPeriod": 0.1136,
                "postedTransactionAmount": 0,
                "postedTransactionsHistory": [
                    {
                        "date": "2024-05-31T00:00:00",
                        "type": "Interest Paid",
                        "withdrawal": 0,
                        "deposit": 0.18
                    }
                ],
                "pendingTransactionAmount": 0,
                "pendingTransaction": {
                    "pendingCredit": 0,
                    "pendingDebit": 0
                },
                "balanceHistory": {
                    "pendingTransactionAmount": 0,
                    "pendingCredit": 0,
                    "pendingDebit": 0,
                    "pendingTransactionsHistory": null,
                    "postedTransactionAmount": 0,
                    "postedTransactionsHistory": null
                },
                "isFormerTdaClient": false
            },
            "marginsInfo": {
                "marginEquity": 914184.47,
                "equityPercent": 0.99,
                "tradeDateBalance": 0,
                "balanceSubjectInterest": 0,
                "mtdInterestOwed": 0,
                "marginSecurity": {
                    "equities": 941990,
                    "equitiesWithFutures": 941990,
                    "mutualFunds": 470995,
                    "mutualFundsFutures": 470995,
                    "shortSell": 941990
                },
                "nonMarginSecurity": {
                    "equities": 470995,
                    "equitiesFutures": 470995,
                    "mutualFunds": 470995,
                    "pennyStocks": 470995,
                    "pennyStocksFutures": 470995
                },
                "fixedIncome": {
                    "treasuries": 4709950,
                    "governmentAgency": 2354975,
                    "municipalBonds": 1883980,
                    "nonConvertCorporates": 1569983.33,
                    "convertCorporates": 941990,
                    "treasuriesFutures": 4709950,
                    "governmentAgencyFutures": 2354975,
                    "municipalBondsFutures": 1883980,
                    "nonConvertCorporatesFutures": 1569983.3333333333,
                    "convertCorporatesFutures": 941990
                },
                "options": {
                    "long": 470995,
                    "longWithFutures": 470995,
                    "short": 470995,
                    "shortFutures": 470995
                },
                "marginEquityPm": 845554.47
            },
            "peggedOptionMarketValue": {
                "coveredCalls": 0,
                "coveredPuts": 0,
                "total": 0
            },
            "optionDetails": {
                "cashSecuredEquityPut": 0,
                "optionRequirement": 10000,
                "optionsApprovalCode": "3"
            },
            "iraDetails": {
                "currentYear": null,
                "priorYear": null,
                "currentYearGrossAmount": 0,
                "priorYearGrossAmount": 0,
                "currentYearDistributionAmount": 0,
                "currentYearRmd": 0,
                "priorYearDistributionAmount": null,
                "priorYearRmd": null,
                "priorYearContributionAmount": null,
                "currYearContributionAmount": 0,
                "priorYearRemRMDAmount": null,
                "currYearRemRMDAmount": null,
                "twoYearPriorRMDAmount": 0,
                "isRmdEligible": false,
                "checkDateForPrevRemRMD": false,
                "rmdMessage": "0",
                "currYearRMDDistribution": 0,
                "priorYearRMDDistribution": null,
                "isCurrYearIraInfoIncomplete": false,
                "isPriorYearIraInfoIncomplete": false
            },
            "pledgedAssets": {
                "requiredAmount": 0,
                "eligibleMarketValue": 0,
                "deficitDue": 0,
                "excess": 0,
                "deficitDueExcessTotal": 0
            },
            "futures": {
                "futuresAccountName": "Living Trust",
                "futuresAccountNumber": "67000426",
                "accountValue": 0,
                "initialMarginRequirement": 0,
                "buyingPower": 470995,
                "totalEquity": 0
            },
            "preferences": null,
            "info": {
                "accountType": 3,
                "country": "USA",
                "isMargin": true,
                "isPatternDayTrader": false,
                "isIra": false,
                "isSpreadIra": false,
                "isCharitable": false,
                "isInheritedIra": false,
                "isSimpleIra": false,
                "isSpreadsInIraAccount": false,
                "isSepIra": false,
                "registrationTypeCode": "LT",
                "isViewOnly": false,
                "isGroupView": false,
                "isDI": false,
                "isPrimaryAccount": false,
                "isUK": false,
                "isSiIra": false,
                "encryptedAccountIndex": 0,
                "accountIndex": 0,
                "isPASSB": false,
                "isMiniLogoVisible": false,
                "isPtisEnabled": false,
                "asPtisEnabled": false,
                "isS3": true,
                "isFutures": true,
                "isOnlyOneHyicAccount": true,
                "isAggregateMarginDetailsAvailable": false,
                "aggregateMarginDetailIndex": 0,
                "indexInAccountList": 0,
                "isAlliance": false,
                "isPCRA": false,
                "productType": "Schwab One with Investor Checking Account",
                "branchCode": "KA",
                "isPrimaryDI": false,
                "isPrimaryUK": false,
                "isPrimaryAlliance": false,
                "acctProductCode": "S3",
                "isIncludeInList": true,
                "isSip": false,
                "isSipp": false,
                "isIip": false,
                "isActiveTrader": true,
                "isRmdCenterEligible": false,
                "phoneNumber": "800-435-4000",
                "primaryPhoneNumber": "800-435-4000"
            },
            "cobrandingDetails": {
                "isMiniLogoClickable": false,
                "isAllianceCobrandingVisible": false,
                "emailAddress": null,
                "webLogo": null,
                "webAddress": null,
                "masterAddress": null,
                "masterName": null,
                "masterPhone": null,
                "isAllianceCoBranding": false,
                "isPCRACoBranding": false
            },
            "errors": {
                "generalError": false,
                "iraError": false,
                "cmtFailure": false,
                "bankServiceFailure": false
            },
            "securitiesDue": false,
            "relatedBankAccountId": "440025659150",
            "areOpenOrdersIncluded": true,
            "isPendingPurchaseEnabled": true,
            "bankSweepResponseDetails": {
                "accounts": null,
                "isServiceError": false
            },
            "isFormerTdaClient": true
        }
    ],
    "aggregateMarginAccountList": [
        {
            "accountId": 0,
            "accountsGroupId": 0,
            "accountsGroupList": [],
            "isAggregate": false,
            "isServiceError": false,
            "aggregateMarginDetailIndex": 0,
            "totalAccountsValue": 0,
            "cash": 0,
            "cashSweepFeature": 0,
            "marginBalance": 0,
            "shortBalance": 0,
            "total": 0,
            "cashAvailableWithdraw": 0,
            "settledFunds": 0,
            "nonMarginSecurities": {
                "securitiesMarketValueLong": 0,
                "securitiesMarketValueShort": 0,
                "optionsMarketValueLong": 0,
                "optionsMarketValueShort": 0
            },
            "marginSecurities": {
                "securitiesMarketValueLong": 0,
                "securitiesMarketValueShort": 0,
                "optionsMarketValueLong": 0,
                "optionsMarketValueShort": 0
            },
            "securitiesTotal": 0,
            "securitiesMarketLongTotal": 0,
            "securitiesMarketShortTotal": 0,
            "optionsMarketLongTotal": 0,
            "optionsMarketShortTotal": 0,
            "optionsTotal": 0,
            "investmentsTotal": 0,
            "moneyDue": 0,
            "marginEquity": 0,
            "equityPercentage": 0,
            "equityOptionMarketValue": 0,
            "marginBuyingPower": 0,
            "dayTradingBuyingPowerDynamic": 0,
            "optionRequirement": 0,
            "monthDateInterest": 0,
            "marginableEquities": 0,
            "nonMarginableSecurities": 0,
            "nonMarginableMutualFunds": 0,
            "pennyStocks": 0,
            "fixedIncome": {
                "treasuriesMaturingYears": 0,
                "governmentAgencies": 0,
                "municipal": 0,
                "nonConvertibleCorporates": 0,
                "convertibleCorporates": 0
            },
            "longOptionsClearedFunds": 0,
            "shortOptionsMinimumEquityRequired": 0
        }
    ],
    "account529List": [],
    "annuityAccountList": [],
    "globalAccountList": [],
    "isAffiliateAccount": false,
    "totals": {
        "accountValue": 845554.47,
        "sumOfDayChange": -62210.35,
        "sumOfDayChangePercent": -6.8531351545436625314472971094,
        "sumOfDayChangePercentRender": -0.0685313515454366253144729711,
        "cashInvestments": 8940.26,
        "marketValue": 836614.21
    },
    "isSameAdvisorLogoVisible": false
  }
  */

  return json.brokerageAccountList;
}

async function getSchwabHoldings(bearerToken, accounts) {
  const accountIds = accounts.map((acct) => acct.id).join(",");

  const resp = await fetch(
    "https://ausgateway.schwab.com/api/is.Holdings/V1/Holdings/Holdings?&includeCostBasis=true&includeRatings=true&includeUnderlyingOption=true",
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${bearerToken}`,
        "Schwab-Accounts-Grp": "Brokerage",
        "Schwab-Channelcode": window["Api-context"].channelCode,
        "Schwab-Client-Appid": "AD00002298",
        "Schwab-Client-Correlid": window["Api-context"].correlationId,
        "Schwab-Client-Ids": accountIds,
        "Schwab-Client-Channel": "IO",
        "Schwab-Env": "PROD",
        "Schwab-Environment": "PROD",
        "Schwab-Environment-Region": "", // This key was present but with no value given
      },
    }
  );
  if (resp.status !== 200) {
    console.log("Not able to get holdings. Status: ", resp.status);
    throw new Error("Not able to get holdings. Status: ", resp.status);
  }

  const json = await resp.json();

  /*
  {
  "accounts": [
  {
      "accountDetail": {
        "isAlliance": true,
        "isAllianceView0": true,
        "isGainLoss": true,
        "isMargin": true,
        "isFuture": true,
        "nickname": "Living Trust",
        "coBrandingOfferDetails": {
          "name": "SYNTHETICFI LLC",
          "address": [
            "156 2ND ST #610",
            "",
            "",
            "",
            "",
            "SAN FRANCISCO, CA 94105",
            "US",
            "UNITED STATES"
          ],
          "phone": [
            "510",
            "646",
            "5424"
          ]
        },
        "isMinilogovisible": true,
        "groupName": "CUSTACCS",
        "role": "TTEE",
        "isGreenAccount": true
      },
      "accountId": "95634901",
      "balances": {
        "marginBalance": 3206.86,
        "schwabBankSweepFeature": 0,
        "sweepMoneyMarketFund": 0,
        "sweepCashBalance": 0,
        "cashSecuredEquityPut": 0
      },
      "groupedPositions": [
        {
          "groupName": "Equity",
          "securityType": 1,
          "positionsCount": 10,
          "positions": [
            {
              "quantity": 440,
              "quantityBeforeSplit": 440,
              "marginRequirement": 24482,
              "percentageOfAccount": 8.28,
              "exDividendDate": "06/10/2024",
              "symbolDetail": {
                "symbol": "GOOG",
                "cusip": "02079K107",
                "description": "ALPHABET INC. CLASS C",
                "quoteSymbol": "GOOG",
                "defaultSymbol": "GOOG",
                "schwabSecurityId": 31930645,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "GOOG"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-31930645-L",
                "price": 0,
                "quantity": 440,
                "sparksId": "18019412",
                "costBasisDetail": {
                  "costBasis": 42682.08,
                  "costPerShare": 97.004727272727,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 38924.72,
                  "gainLossPercent": 91.2
                }
              },
              "priceDetail": {
                "price": 185.47,
                "priceChange": -2.72,
                "priceChangePercent": -1.45,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 81606.8,
                "dayChange": -1196.8,
                "dayChangePercent": -1.45
              },
              "ratingDetail": {
                "rating": "A"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 140,
              "quantityBeforeSplit": 140,
              "marginRequirement": 9845,
              "percentageOfAccount": 3.33,
              "exDividendDate": "05/10/2024",
              "symbolDetail": {
                "symbol": "AAPL",
                "cusip": "037833100",
                "description": "APPLE INC",
                "quoteSymbol": "AAPL",
                "defaultSymbol": "AAPL",
                "schwabSecurityId": 1973757747,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "AAPL"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-1973757747-L",
                "price": 0,
                "quantity": 140,
                "sparksId": "119913",
                "costBasisDetail": {
                  "costBasis": 25325.35,
                  "costPerShare": 180.895357142857,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 7491.35,
                  "gainLossPercent": 29.58
                }
              },
              "priceDetail": {
                "price": 234.405,
                "priceChange": 0.005,
                "priceChangePercent": 0,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 32816.7,
                "dayChange": 0.7,
                "dayChangePercent": 0
              },
              "ratingDetail": {
                "rating": "B"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 185,
              "quantityBeforeSplit": 185,
              "marginRequirement": 13644,
              "percentageOfAccount": 4.61,
              "exDividendDate": "08/23/2024",
              "symbolDetail": {
                "symbol": "AMAT",
                "cusip": "038222105",
                "description": "APPLIED MATERIALS",
                "quoteSymbol": "AMAT",
                "defaultSymbol": "AMAT",
                "schwabSecurityId": 1444854003,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "AMAT"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-1444854003-L",
                "price": 0,
                "quantity": 185,
                "sparksId": "92199",
                "costBasisDetail": {
                  "costBasis": 16533.99,
                  "costPerShare": 89.372918918919,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 28944.56,
                  "gainLossPercent": 175.06
                }
              },
              "priceDetail": {
                "price": 245.83,
                "priceChange": 0.28,
                "priceChangePercent": 0.11,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 45478.55,
                "dayChange": 51.8,
                "dayChangePercent": 0.11
              },
              "ratingDetail": {
                "rating": "A"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 31,
              "quantityBeforeSplit": 31,
              "marginRequirement": 9930,
              "percentageOfAccount": 3.36,
              "exDividendDate": "04/26/2024",
              "symbolDetail": {
                "symbol": "ASML",
                "cusip": "N07059210",
                "description": "ASML HOLDING N V FSPONSORED ADR 1 ADR REPS 1 ORD SHS",
                "quoteSymbol": "ASML",
                "defaultSymbol": "ASML",
                "schwabSecurityId": 337154690,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "ASML"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-337154690-L",
                "price": 0,
                "quantity": 31,
                "sparksId": "9641304",
                "costBasisDetail": {
                  "costBasis": 14786.93,
                  "costPerShare": 476.997741935484,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 18311.77,
                  "gainLossPercent": 123.84
                }
              },
              "priceDetail": {
                "price": 1067.7,
                "priceChange": 4.07,
                "priceChangePercent": 0.38,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 33098.7,
                "dayChange": 126.17,
                "dayChangePercent": 0.38
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 75,
              "quantityBeforeSplit": 75,
              "marginRequirement": 24093,
              "percentageOfAccount": 8.14,
              "exDividendDate": "06/18/2024",
              "symbolDetail": {
                "symbol": "LRCX",
                "cusip": "512807108",
                "description": "LAM RESEARCH CORP",
                "quoteSymbol": "LRCX",
                "defaultSymbol": "LRCX",
                "schwabSecurityId": 1778968234,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "LRCX"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-1778968234-L",
                "price": 0,
                "quantity": 75,
                "sparksId": "109724",
                "costBasisDetail": {
                  "costBasis": 27467.18,
                  "costPerShare": 366.229066666667,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 52843.57,
                  "gainLossPercent": 192.39
                }
              },
              "priceDetail": {
                "price": 1070.81,
                "priceChange": 1.7,
                "priceChangePercent": 0.16,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 80310.75,
                "dayChange": 127.5,
                "dayChangePercent": 0.16
              },
              "ratingDetail": {
                "rating": "B"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 86,
              "quantityBeforeSplit": 86,
              "marginRequirement": 12076,
              "percentageOfAccount": 4.08,
              "exDividendDate": "09/03/2024",
              "symbolDetail": {
                "symbol": "LMT",
                "cusip": "539830109",
                "description": "LOCKHEED MARTIN CORP",
                "quoteSymbol": "LMT",
                "defaultSymbol": "LMT",
                "schwabSecurityId": 334952175,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "LMT"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-334952175-L",
                "price": 0,
                "quantity": 86,
                "sparksId": "23527",
                "costBasisDetail": {
                  "costBasis": 28328.81,
                  "costPerShare": 329.40476744186,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 11924.35,
                  "gainLossPercent": 42.09
                }
              },
              "priceDetail": {
                "price": 468.06,
                "priceChange": 4.18,
                "priceChangePercent": 0.9,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 40253.16,
                "dayChange": 359.48,
                "dayChangePercent": 0.9
              },
              "ratingDetail": {
                "rating": "C"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 303,
              "quantityBeforeSplit": 303,
              "marginRequirement": 40851,
              "percentageOfAccount": 13.81,
              "exDividendDate": "08/16/2024",
              "symbolDetail": {
                "symbol": "MSFT",
                "cusip": "594918104",
                "description": "MICROSOFT CORP",
                "quoteSymbol": "MSFT",
                "defaultSymbol": "MSFT",
                "schwabSecurityId": 1688643765,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "MSFT"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-1688643765-L",
                "price": 0,
                "quantity": 303,
                "sparksId": "104939",
                "costBasisDetail": {
                  "costBasis": 70808.08,
                  "costPerShare": 233.6900330033,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 65361.42,
                  "gainLossPercent": 92.31
                }
              },
              "priceDetail": {
                "price": 449.4043,
                "priceChange": -4.5557,
                "priceChangePercent": -1,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 136169.5,
                "dayChange": -1380.38,
                "dayChangePercent": -1
              },
              "ratingDetail": {
                "rating": "A"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 250,
              "quantityBeforeSplit": 250,
              "marginRequirement": 32595,
              "percentageOfAccount": 11.02,
              "exDividendDate": "05/24/2024",
              "symbolDetail": {
                "symbol": "NOC",
                "cusip": "666807102",
                "description": "NORTHROP GRUMMAN CO",
                "quoteSymbol": "NOC",
                "defaultSymbol": "NOC",
                "schwabSecurityId": 2097719277,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "NOC"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-2097719277-L",
                "price": 0,
                "quantity": 250,
                "sparksId": "126403",
                "costBasisDetail": {
                  "costBasis": 71746.55,
                  "costPerShare": 286.9862,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 36904.7,
                  "gainLossPercent": 51.44
                }
              },
              "priceDetail": {
                "price": 434.605,
                "priceChange": 2.685,
                "priceChangePercent": 0.62,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 108651.25,
                "dayChange": 671.25,
                "dayChangePercent": 0.62
              },
              "ratingDetail": {
                "rating": "C"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 57,
              "quantityBeforeSplit": 57,
              "marginRequirement": 9493,
              "percentageOfAccount": 3.21,
              "exDividendDate": "09/13/2024",
              "symbolDetail": {
                "symbol": "TMO",
                "cusip": "883556102",
                "description": "THERMO FISHER SCNTFC",
                "quoteSymbol": "TMO",
                "defaultSymbol": "TMO",
                "schwabSecurityId": 451470159,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "TMO"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-451470159-L",
                "price": 0,
                "quantity": 57,
                "sparksId": "30738",
                "costBasisDetail": {
                  "costBasis": 24081.52,
                  "costPerShare": 422.482807017544,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 7560.32,
                  "gainLossPercent": 31.39
                }
              },
              "priceDetail": {
                "price": 555.12,
                "priceChange": 10.44,
                "priceChangePercent": 1.92,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 31641.84,
                "dayChange": 595.08,
                "dayChangePercent": 1.92
              },
              "ratingDetail": {
                "rating": "A"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 306,
              "quantityBeforeSplit": 306,
              "marginRequirement": 6437,
              "percentageOfAccount": 2.18,
              "exDividendDate": "08/16/2024",
              "symbolDetail": {
                "symbol": "WMT",
                "cusip": "931142103",
                "description": "WALMART INC",
                "quoteSymbol": "WMT",
                "defaultSymbol": "WMT",
                "schwabSecurityId": 480796792,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "COMNEQTY",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 1,
                "symbolForDetailedQuotes": "WMT"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-480796792-L",
                "price": 0,
                "quantity": 306,
                "sparksId": "32559",
                "costBasisDetail": {
                  "costBasis": 12115.06,
                  "costPerShare": 39.591699346405,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 9340.13,
                  "gainLossPercent": 77.1
                }
              },
              "priceDetail": {
                "price": 70.115,
                "priceChange": 0.505,
                "priceChangePercent": 0.73,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 21455.19,
                "dayChange": 154.53,
                "dayChangePercent": 0.73
              },
              "ratingDetail": {
                "rating": "C"
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            }
          ],
          "totals": {
            "dayChangeDollar": -490.67,
            "dayChangePercent": -0.08017835947072904,
            "marketValue": 611482.44,
            "marketValueLong": 611482.44,
            "percentageOfAccount": 62.01,
            "costBasis": 333875.55,
            "gainLossDollar": 277606.89,
            "gainLossPercent": 83.14681623137724,
            "isMarketValueAvailable": true,
            "isPriceAvailable": true,
            "isCostAvailable": true,
            "isPriceChangeAvailable": true,
            "isGainLossAvailable": true
          }
        },
        {
          "groupName": "ETF",
          "securityType": 2,
          "positionsCount": 6,
          "positions": [
            {
              "quantity": 1127,
              "quantityBeforeSplit": 1127,
              "marginRequirement": 31827,
              "percentageOfAccount": 10.76,
              "exDividendDate": "07/01/2024",
              "symbolDetail": {
                "symbol": "TLT",
                "cusip": "464287432",
                "description": "ISHARES 20 PLS YEAR TREASURY BND ETF",
                "quoteSymbol": "TLT",
                "defaultSymbol": "TLT",
                "schwabSecurityId": 1712707094,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "ETF",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 2,
                "symbolForDetailedQuotes": "TLT"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-1712707094-L",
                "price": 0,
                "quantity": 1127,
                "sparksId": "106203",
                "costBasisDetail": {
                  "costBasis": 111223.39,
                  "costPerShare": 98.689787045253,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": -5133.24,
                  "gainLossPercent": -4.62
                }
              },
              "priceDetail": {
                "price": 94.135,
                "priceChange": 1.275,
                "priceChangePercent": 1.37,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 106090.15,
                "dayChange": 1436.93,
                "dayChangePercent": 1.37
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 496,
              "quantityBeforeSplit": 496,
              "marginRequirement": 17365,
              "percentageOfAccount": 5.87,
              "exDividendDate": "06/11/2024",
              "symbolDetail": {
                "symbol": "IJR",
                "cusip": "464287804",
                "description": "ISHARES CORE S&P SMALL CAP ETF",
                "quoteSymbol": "IJR",
                "defaultSymbol": "IJR",
                "schwabSecurityId": 1835204038,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "ETF",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 2,
                "symbolForDetailedQuotes": "IJR"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-1835204038-L",
                "price": 0,
                "quantity": 496,
                "sparksId": "112676",
                "costBasisDetail": {
                  "costBasis": 49629.73,
                  "costPerShare": 100.059939516129,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 8253.47,
                  "gainLossPercent": 16.63
                }
              },
              "priceDetail": {
                "price": 116.7,
                "priceChange": 3.89,
                "priceChangePercent": 3.45,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 57883.2,
                "dayChange": 1929.44,
                "dayChangePercent": 3.45
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 200,
              "quantityBeforeSplit": 200,
              "marginRequirement": 4661,
              "percentageOfAccount": 1.58,
              "exDividendDate": "06/24/2024",
              "symbolDetail": {
                "symbol": "XLP",
                "cusip": "81369Y308",
                "description": "SPDR FUND CONSUMER STAPLES ETF",
                "quoteSymbol": "XLP",
                "defaultSymbol": "XLP",
                "schwabSecurityId": 110775469,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "ETF",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 2,
                "symbolForDetailedQuotes": "XLP"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-110775469-L",
                "price": 0,
                "quantity": 200,
                "sparksId": "9811",
                "costBasisDetail": {
                  "costBasis": 13731.63,
                  "costPerShare": 68.65815,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 1803.37,
                  "gainLossPercent": 13.13
                }
              },
              "priceDetail": {
                "price": 77.675,
                "priceChange": 0.675,
                "priceChangePercent": 0.88,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 15535,
                "dayChange": 135,
                "dayChangePercent": 0.88
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 75,
              "quantityBeforeSplit": 75,
              "marginRequirement": 12697,
              "percentageOfAccount": 4.29,
              "exDividendDate": "09/19/2024",
              "symbolDetail": {
                "symbol": "SPY",
                "cusip": "78462F103",
                "description": "SPDR S&P 500 ETF",
                "quoteSymbol": "SPY",
                "defaultSymbol": "SPY",
                "schwabSecurityId": 1281357639,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "ETF",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 2,
                "symbolForDetailedQuotes": "SPY"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-1281357639-L",
                "price": 0,
                "quantity": 75,
                "sparksId": "82299",
                "costBasisDetail": {
                  "costBasis": 31305,
                  "costPerShare": 417.4,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 11018.25,
                  "gainLossPercent": 35.2
                }
              },
              "priceDetail": {
                "price": 564.31,
                "priceChange": 2.78,
                "priceChangePercent": 0.5,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 42323.25,
                "dayChange": 208.5,
                "dayChangePercent": 0.5
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 425,
              "quantityBeforeSplit": 425,
              "marginRequirement": 13529,
              "percentageOfAccount": 4.57,
              "exDividendDate": "03/22/2024",
              "symbolDetail": {
                "symbol": "VFH",
                "cusip": "92204A405",
                "description": "VANGUARD FINANCIALS ETF",
                "quoteSymbol": "VFH",
                "defaultSymbol": "VFH",
                "schwabSecurityId": 523909557,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "ETF",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 2,
                "symbolForDetailedQuotes": "VFH"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-523909557-L",
                "price": 0,
                "quantity": 425,
                "sparksId": "1339617",
                "costBasisDetail": {
                  "costBasis": 42053.71,
                  "costPerShare": 98.949905882353,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 3043.04,
                  "gainLossPercent": 7.24
                }
              },
              "priceDetail": {
                "price": 106.11,
                "priceChange": 1.49,
                "priceChangePercent": 1.42,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 45096.75,
                "dayChange": 633.25,
                "dayChangePercent": 1.42
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            },
            {
              "quantity": 174,
              "quantityBeforeSplit": 174,
              "marginRequirement": 14378,
              "percentageOfAccount": 4.86,
              "exDividendDate": "03/22/2024",
              "symbolDetail": {
                "symbol": "VHT",
                "cusip": "92204A504",
                "description": "VANGUARD HEALTH CARE ETF",
                "quoteSymbol": "VHT",
                "defaultSymbol": "VHT",
                "schwabSecurityId": 2033167956,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "isMarginable": true,
                "securityGroupCode": "ETF",
                "ruleSetSuffix": 0,
                "accountingRuleCode": 2,
                "positionType": 0,
                "securityType": 2,
                "symbolForDetailedQuotes": "VHT"
              },
              "costDetail": {
                "isCertified": true,
                "costMethod": "I",
                "positionId": "95634901-2033167956-L",
                "price": 0,
                "quantity": 174,
                "sparksId": "1339733",
                "costBasisDetail": {
                  "costBasis": 43203.43,
                  "costPerShare": 248.295574712644,
                  "isCostFullyKnown": true
                },
                "gainLossDetail": {
                  "isGainLossFullyKnown": true,
                  "gainLoss": 4723.7,
                  "gainLossPercent": 10.93
                }
              },
              "priceDetail": {
                "price": 275.4433,
                "priceChange": 4.1533,
                "priceChangePercent": 1.53,
                "priceDate": "07/16/2024",
                "isPriceRealTime": true,
                "marketValue": 47927.13,
                "dayChange": 722.67,
                "dayChangePercent": 1.53
              },
              "reinvestDetail": {},
              "marginDetail": {
                "pegAmount": 0,
                "nakedQuantity": 0,
                "nakedRequirementAmount": 0,
                "spreadQuantity": 0,
                "spreadRequirementAmount": 0,
                "strangleQuantity": 0,
                "strangleRequirementAmount": 0,
                "coverQuantity": 0
              },
              "marginOptionStrategy": []
            }
          ],
          "totals": {
            "dayChangeDollar": 5065.79,
            "dayChangePercent": 1.6352351816485564,
            "marketValue": 314855.48,
            "marketValueLong": 314855.48,
            "percentageOfAccount": 31.93,
            "costBasis": 291146.89,
            "gainLossDollar": 23708.59,
            "gainLossPercent": 8.143171304354308,
            "isMarketValueAvailable": true,
            "isPriceAvailable": true,
            "isCostAvailable": true,
            "isPriceChangeAvailable": true,
            "isGainLossAvailable": true
          }
        },
        {
          "groupName": "Indices",
          "securityType": 6,
          "positionsCount": 1,
          "positions": [
            {
              "quantity": 0,
              "symbolDetail": {
                "symbol": "$SPX",
                "description": "S & P 500 INDEX",
                "schwabSecurityId": 1819771877,
                "underlyingSchwabSecurityId": 0,
                "isLink": true,
                "ruleSetSuffix": 0,
                "accountingRuleCode": 0,
                "positionType": 10,
                "securityType": 6,
                "symbolForDetailedQuotes": "$SPX"
              },
              "priceDetail": {
                "price": 5661.47,
                "priceChange": 30.25,
                "priceChangePercent": 0.5371837719002277,
                "priceDate": "07/16/2024",
                "isDayChangeNotAvailable": true,
                "marketValue": 0,
                "dayChange": 0,
                "dayChangePercent": 0
              },
              "detailedQuote": {
                "dividendYield": 0,
                "lastDividend": 0,
                "low52Week": 0,
                "high52Week": 0,
                "dailyVolume": 0,
                "priceEarningsRatio": 0,
                "price": 0,
                "priceChange": 0,
                "priceChangePercent": 0
              },
              "childOptionHoldings": [
                {
                  "quantity": -1,
                  "quantityBeforeSplit": -1,
                  "marginRequirement": 0,
                  "intrinsicValue": 661.4700000000003,
                  "inTheMoneyValue": "ITM",
                  "percentageOfAccount": -6.74,
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
                  "costDetail": {
                    "isCertified": true,
                    "costMethod": "I",
                    "positionId": "95634901-90914410-S",
                    "price": 0,
                    "quantity": -1,
                    "sparksId": "59878240",
                    "costBasisDetail": {
                      "costBasis": -48800.71,
                      "costPerShare": 488.0071,
                      "isCostFullyKnown": true
                    },
                    "gainLossDetail": {
                      "isGainLossFullyKnown": true,
                      "gainLoss": -17709.29,
                      "gainLossPercent": -36.29
                    }
                  },
                  "priceDetail": {
                    "price": 665.1,
                    "priceChange": 29.0996,
                    "priceChangePercent": 4.58,
                    "priceDate": "07/16/2024",
                    "isPriceRealTime": true,
                    "marketValue": -66510,
                    "dayChange": -2909.96,
                    "dayChangePercent": -4.58,
                    "underlyingPrice": 5661.47,
                    "underlyingPriceChange": 30.25,
                    "underlyingPriceChangePercent": 0.5371837719002277
                  },
                  "reinvestDetail": {},
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
                  "isMarginRequirementFootNote": true
                },
                {
                  "quantity": -1,
                  "quantityBeforeSplit": -1,
                  "marginRequirement": 0,
                  "intrinsicValue": -561.4700000000003,
                  "inTheMoneyValue": "OTM",
                  "percentageOfAccount": 0,
                  "maturityDate": "07/19/2024",
                  "maturityDuration": 3,
                  "symbolDetail": {
                    "symbol": "SPX 07/19/2024 5100.00 P",
                    "description": "PUT S & P 500 INDEX $5100 EXP 07/19/24",
                    "quoteSymbol": "SPX   240719P05100000",
                    "defaultSymbol": "SPX   240719P05100000",
                    "underlyingSymbol": "$SPX",
                    "underlyingDescription": "S & P 500 INDEX",
                    "schwabSecurityId": 90914517,
                    "underlyingSchwabSecurityId": 1819771877,
                    "isLink": true,
                    "isOptionIndices": true,
                    "securityGroupCode": "OPTION",
                    "ruleSetSuffix": 0,
                    "accountingRuleCode": 6,
                    "positionType": 0,
                    "securityType": 4,
                    "symbolForDetailedQuotes": "SPX   240719P05100000"
                  },
                  "costDetail": {
                    "isCertified": true,
                    "costMethod": "I",
                    "positionId": "95634901-90914517-S",
                    "price": 0,
                    "quantity": -1,
                    "sparksId": "59959621",
                    "costBasisDetail": {
                      "costBasis": -240.71,
                      "costPerShare": 2.4071,
                      "isCostFullyKnown": true
                    },
                    "gainLossDetail": {
                      "isGainLossFullyKnown": true,
                      "gainLoss": 213.21,
                      "gainLossPercent": 88.58
                    }
                  },
                  "priceDetail": {
                    "price": 0.275,
                    "priceChange": 0.1415,
                    "priceChangePercent": 105.99,
                    "priceDate": "07/16/2024",
                    "isPriceRealTime": true,
                    "marketValue": -27.5,
                    "dayChange": -14.15,
                    "dayChangePercent": -105.99,
                    "underlyingPrice": 5661.47,
                    "underlyingPriceChange": 30.25,
                    "underlyingPriceChangePercent": 0.5371837719002277
                  },
                  "reinvestDetail": {},
                  "marginDetail": {
                    "pegAmount": 0,
                    "nakedQuantity": 0,
                    "nakedRequirementAmount": 0,
                    "spreadQuantity": -1,
                    "spreadRequirementAmount": 10000,
                    "strangleQuantity": 0,
                    "strangleRequirementAmount": 0,
                    "coverQuantity": 0
                  },
                  "marginOptionStrategy": [
                    {
                      "quantity": -1,
                      "name": "SBXS",
                      "sequence": 1,
                      "displayOptionRequirement": "Y",
                      "isSequence": true
                    }
                  ],
                  "isMarginRequirementFootNote": true
                },
                {
                  "quantity": 1,
                  "quantityBeforeSplit": 1,
                  "marginRequirement": 0,
                  "intrinsicValue": -661.4700000000003,
                  "inTheMoneyValue": "OTM",
                  "percentageOfAccount": 0,
                  "maturityDate": "07/19/2024",
                  "maturityDuration": 3,
                  "symbolDetail": {
                    "symbol": "SPX 07/19/2024 5000.00 P",
                    "description": "PUT S & P 500 INDEX $5000 EXP 07/19/24",
                    "quoteSymbol": "SPX   240719P05000000",
                    "defaultSymbol": "SPX   240719P05000000",
                    "underlyingSymbol": "$SPX",
                    "underlyingDescription": "S & P 500 INDEX",
                    "schwabSecurityId": 90914615,
                    "underlyingSchwabSecurityId": 1819771877,
                    "isLink": true,
                    "isOptionIndices": true,
                    "securityGroupCode": "OPTION",
                    "ruleSetSuffix": 0,
                    "accountingRuleCode": 2,
                    "positionType": 0,
                    "securityType": 4,
                    "symbolForDetailedQuotes": "SPX   240719P05000000"
                  },
                  "costDetail": {
                    "isCertified": true,
                    "costMethod": "I",
                    "positionId": "95634901-90914615-L",
                    "price": 0,
                    "quantity": 1,
                    "sparksId": "59892477",
                    "costBasisDetail": {
                      "costBasis": 168.29,
                      "costPerShare": 1.6829,
                      "isCostFullyKnown": true
                    },
                    "gainLossDetail": {
                      "isGainLossFullyKnown": true,
                      "gainLoss": -145.79,
                      "gainLossPercent": -86.63
                    }
                  },
                  "priceDetail": {
                    "price": 0.225,
                    "priceChange": 0.2004,
                    "priceChangePercent": 814.63,
                    "priceDate": "07/16/2024",
                    "isPriceRealTime": true,
                    "marketValue": 22.5,
                    "dayChange": 20.04,
                    "dayChangePercent": 814.63,
                    "underlyingPrice": 5661.47,
                    "underlyingPriceChange": 30.25,
                    "underlyingPriceChangePercent": 0.5371837719002277
                  },
                  "reinvestDetail": {},
                  "marginDetail": {
                    "pegAmount": 0,
                    "nakedQuantity": 0,
                    "nakedRequirementAmount": 0,
                    "spreadQuantity": 0,
                    "spreadRequirementAmount": 0,
                    "strangleQuantity": 0,
                    "strangleRequirementAmount": 0,
                    "coverQuantity": 0
                  },
                  "marginOptionStrategy": [
                    {
                      "quantity": 1,
                      "name": "SBXS",
                      "sequence": 1,
                      "displayOptionRequirement": "N",
                      "isSequence": true
                    }
                  ],
                  "isMarginRequirementFootNote": true
                },
                {
                  "quantity": 1,
                  "quantityBeforeSplit": 1,
                  "marginRequirement": 0,
                  "intrinsicValue": 561.4700000000003,
                  "inTheMoneyValue": "ITM",
                  "percentageOfAccount": 5.73,
                  "maturityDate": "07/19/2024",
                  "maturityDuration": 3,
                  "symbolDetail": {
                    "symbol": "SPX 07/19/2024 5100.00 C",
                    "description": "CALL S & P 500 INDEX $5100 EXP 07/19/24",
                    "quoteSymbol": "SPX   240719C05100000",
                    "defaultSymbol": "SPX   240719C05100000",
                    "underlyingSymbol": "$SPX",
                    "underlyingDescription": "S & P 500 INDEX",
                    "schwabSecurityId": 90914918,
                    "underlyingSchwabSecurityId": 1819771877,
                    "isLink": true,
                    "isOptionIndices": true,
                    "securityGroupCode": "OPTION",
                    "ruleSetSuffix": 0,
                    "accountingRuleCode": 2,
                    "positionType": 0,
                    "securityType": 4,
                    "symbolForDetailedQuotes": "SPX   240719C05100000"
                  },
                  "costDetail": {
                    "isCertified": true,
                    "costMethod": "I",
                    "positionId": "95634901-90914918-L",
                    "price": 0,
                    "quantity": 1,
                    "sparksId": "59868851",
                    "costBasisDetail": {
                      "costBasis": 38918.29,
                      "costPerShare": 389.1829,
                      "isCostFullyKnown": true
                    },
                    "gainLossDetail": {
                      "isGainLossFullyKnown": true,
                      "gainLoss": 17606.71,
                      "gainLossPercent": 45.24
                    }
                  },
                  "priceDetail": {
                    "price": 565.25,
                    "priceChange": 29.0815,
                    "priceChangePercent": 5.42,
                    "priceDate": "07/16/2024",
                    "isPriceRealTime": true,
                    "marketValue": 56525,
                    "dayChange": 2908.15,
                    "dayChangePercent": 5.42,
                    "underlyingPrice": 5661.47,
                    "underlyingPriceChange": 30.25,
                    "underlyingPriceChangePercent": 0.5371837719002277
                  },
                  "reinvestDetail": {},
                  "marginDetail": {
                    "pegAmount": 0,
                    "nakedQuantity": 0,
                    "nakedRequirementAmount": 0,
                    "spreadQuantity": 0,
                    "spreadRequirementAmount": 0,
                    "strangleQuantity": 0,
                    "strangleRequirementAmount": 0,
                    "coverQuantity": 0
                  },
                  "marginOptionStrategy": [
                    {
                      "quantity": 1,
                      "name": "SBXS",
                      "sequence": 1,
                      "displayOptionRequirement": "N",
                      "isSequence": true
                    }
                  ],
                  "isMarginRequirementFootNote": true
                }
              ]
            }
          ],
          "totals": {
            "dayChangeDollar": 4.079999999999927,
            "dayChangePercent": 0.040824167907400455,
            "marketValue": -9990,
            "marketValueLong": 56547.5,
            "percentageOfAccount": 5.73,
            "costBasis": -9954.839999999997,
            "gainLossDollar": -35.16000000000349,
            "gainLossPercent": -0.35319502874986947,
            "isMarketValueAvailable": true,
            "isPriceAvailable": true,
            "isCostAvailable": true,
            "isPriceChangeAvailable": true,
            "isGainLossAvailable": true
          }
        },
        {
          "groupName": "Futures",
          "securityType": 7,
          "positionsCount": 2,
          "positions": [
            {
              "quantity": 0,
              "quantityBeforeSplit": 0,
              "percentageOfAccount": 0,
              "symbolDetail": {
                "schwabSecurityId": 0,
                "underlyingSchwabSecurityId": 0,
                "ruleSetSuffix": 0,
                "accountingRuleCode": 0,
                "positionType": 4,
                "securityType": 7
              },
              "priceDetail": {
                "price": 0,
                "priceChange": 0,
                "priceChangePercent": 0,
                "marketValue": 0,
                "dayChange": 0,
                "dayChangePercent": 0
              }
            },
            {
              "quantity": 0,
              "quantityBeforeSplit": 0,
              "percentageOfAccount": 0,
              "symbolDetail": {
                "schwabSecurityId": 0,
                "underlyingSchwabSecurityId": 0,
                "ruleSetSuffix": 0,
                "accountingRuleCode": 0,
                "positionType": 3,
                "securityType": 7
              },
              "priceDetail": {
                "price": 0,
                "priceChange": 0,
                "priceChangePercent": 0,
                "marketValue": 0,
                "dayChange": 0,
                "dayChangePercent": 0
              }
            }
          ],
          "totals": {
            "dayChangeDollar": 0,
            "dayChangePercent": 0,
            "marketValue": 0,
            "marketValueLong": 0,
            "percentageOfAccount": 0,
            "costBasis": 0,
            "gainLossDollar": 0,
            "gainLossPercent": 0,
            "isMarketValueAvailable": true,
            "isPriceAvailable": true,
            "isPriceChangeAvailable": true
          }
        },
        {
          "groupName": "Cash",
          "securityType": 9,
          "positionsCount": 1,
          "positions": [
            {
              "quantity": 0,
              "quantityBeforeSplit": 0,
              "percentageOfAccount": 0.33,
              "symbolDetail": {
                "symbol": "",
                "schwabSecurityId": 0,
                "underlyingSchwabSecurityId": 0,
                "ruleSetSuffix": 0,
                "accountingRuleCode": 0,
                "positionType": 3,
                "securityType": 9,
                "symbolForDetailedQuotes": ""
              },
              "priceDetail": {
                "price": 0,
                "priceChange": 0,
                "priceChangePercent": 0,
                "marketValue": 3206.86,
                "dayChange": 0,
                "dayChangePercent": 0
              }
            }
          ],
          "totals": {
            "dayChangeDollar": 0,
            "dayChangePercent": 0,
            "marketValue": 3206.86,
            "marketValueLong": 3206.86,
            "percentageOfAccount": 0.33,
            "costBasis": 0,
            "gainLossDollar": 0,
            "gainLossPercent": 0,
            "isMarketValueAvailable": true,
            "isPriceAvailable": true,
            "isPriceChangeAvailable": true
          }
        }
      ],
      "totals": {
        "marketValueLong": 986092.2799999999,
        "cashInvestments": 3206.86,
        "costBasis": 615067.6,
        "isCostFullyKnown": true,
        "isGainLossFullyKnown": true,
        "gainLossDollar": 301280.32,
        "gainLossPercent": 48.98,
        "accountValue": 919554.78,
        "marketValue": 916347.92,
        "dayChangeDollar": 4579.2,
        "dayChangePercent": 0.5,
        "totalDayChangeDollar": 4579.2,
        "totalDayChangePercent": 0.5004723732626831
      }
    }
  ],
  "accountTotals": {
    "marketValueLong": 1055511.5499999998,
    "cashInvestments": 3351.15,
    "costBasis": 621145.31,
    "isCostFullyKnown": true,
    "isGainLossFullyKnown": true,
    "gainLossDollar": 301268.04,
    "gainLossPercent": 48.5,
    "accountValue": 988974.05,
    "marketValue": 985622.9,
    "dayChangeDollar": 4951.34,
    "dayChangePercent": 0.5031733464769323
  },
  "conditionalFootNotes": {
    "isMarginRequirementFootNote": true,
    "containsOptions": true,
    "hasFractionPairingIn": false
  },
  "columnsMetaData": {
    "symbol": {
      "isOption": false,
      "maxLength": 24,
      "sampleMaxText": "SPX 07/19/2024 5000.00 C"
    },
    "name": {
      "isOption": false,
      "maxLength": 52,
      "sampleMaxText": "ASML HOLDING N V FSPONSORED ADR 1 ADR REPS 1 ORD SHS"
    },
    "marginRequirement": {
      "isOption": false,
      "maxLength": 0
    },
    "quoteSymbols": [
      "FLOT",
      "EQR",
      "VUG",
      "VYMI",
      "VNQ",
      "GOOG",
      "AAPL",
      "AMAT",
      "ASML",
      "LRCX",
      "LMT",
      "MSFT",
      "NOC",
      "TMO",
      "WMT",
      "TLT",
      "IJR",
      "XLP",
      "SPY",
      "VFH",
      "VHT",
      "SPX   240719C05000000",
      "$SPX",
      "SPX   240719P05100000",
      "SPX   240719P05000000",
      "SPX   240719C05100000"
    ],
    "totalPositionCount": 30
  },
  "entitlement": "NP",
  "hasThemes": false
}
  */

  const holdings = json.accounts;

  return holdings;
}

async function main() {
  const bearerToken = await getBearerToken();

  const accounts = await getAccounts(bearerToken);

  const balances = await getSchwabBalances(bearerToken, accounts);

  const holdings = await getSchwabHoldings(bearerToken, accounts);

  const results = balances.map((balance) => {
    const accountHolding = holdings.find(
      (h) => h.accountId === balance.accountId
    );

    return {
      ...balance,
      holdings: accountHolding.groupedPositions,
    };
  });

  // send the result to service worker
  chrome.runtime.sendMessage(
    extensionId,
    {
      type: "schwab_balance",
      data: results,
    },
    function (response) {
      if (!response.success) console.log(response);
    }
  );
}

window.addEventListener("load", function () {
  main();
});
