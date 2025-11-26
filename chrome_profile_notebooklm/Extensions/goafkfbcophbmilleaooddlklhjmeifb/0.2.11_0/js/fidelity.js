// try to load the fidelity balance
console.log("load fidelity balance");

const extensionId = "goafkfbcophbmilleaooddlklhjmeifb";

async function getFidelityAccountDetails() {
  const payload = {
    operationName: "GetContext",
    variables: {},
    query: `query GetContext {
      getContext {
        sysStatus {
          balance
          backend {
            account
            feature
            __typename
          }
          account {
            Brokerage
            StockPlans
            ExternalLinked
            ExternalManual
            WorkplaceContributions
            WorkplaceBenefits
            Annuity
            FidelityCreditCards
            Charitable
            BrokerageLending
            InternalDigital
            ExternalDigital
            __typename
          }
          __typename
        }
        person {
          id
          sysMsgs {
            message
            source
            code
            type
            __typename
          }
          relationships {
            type
            subType
            __typename
          }
          balances {
            hasIntradayPricing
            isPriorDayGainLossReset
            balanceDetail {
              gainLossBalanceDetail {
                totalMarketVal
                todaysGainLoss
                todaysGainLossPct
                fidelityTotalMktVal
                hasUnpricedPositions
                __typename
              }
              __typename
            }
            __typename
          }
          assets {
            acctNum
            acctType
            acctSubType
            acctSubTypeDesc
            acctCreationDate
            parentBrokAcctNum
            linkedAcctDetails {
              acctNum
              isLinked
              __typename
            }
            brokerageLendingAcctDetail {
              institutionName
              creditLineAmount
              lineAvailablityAmount
              endInterestRate
              baseInterestRate
              spreadToBaseRate
              baseIndexName
              nextPaymentDueDate
              lastPaymentDate
              paymentAmountDue
              loanStatus
              pledgedAccountNumber
              fullLoanId
              __typename
            }
            acctStateDetail {
              statusCode
              __typename
            }
            preferenceDetail {
              name
              isHidden
              isDefaultAcct
              acctGroupId
              __typename
            }
            gainLossBalanceDetail {
              totalMarketVal
              todaysGainLoss
              todaysGainLossPct
              asOfDateTime
              hasUnpricedPositions
              hasIntradayPricing
              __typename
            }
            acctRelAttrDetail {
              relCategoryCode
              relRoleTypeCode
              __typename
            }
            acctLegacyAttrDetail {
              legacyHouseHoldCostBasisCode
              __typename
            }
            annuityProductDetail {
              systemOfRecord
              planTypeCode
              planCode
              productCode
              productDesc
              __typename
            }
            workplacePlanDetail {
              planInTransitionInd
              planTypeName
              planTypeCode
              planId
              clientId
              clientTickerSymbol
              enrollmentStatusCode
              isCrossoverEnabled
              isEnrollmentEligible
              nonQualifiedInd
              isRollup
              planName
              navigationKey
              url
              vestedAcctValEOD
              isVested100Pct
              __typename
            }
            acctTypesIndDetail {
              isRetailHSA
              isRetirement
              isYouthAcct
              hasSPSPlans
              __typename
            }
            acctAttrDetail {
              regTypeDesc
              costBasisCode
              addlBrokAcctCode
              taxTreatmentCode
              coreSymbolCode
              __typename
            }
            acctIndDetail {
              isAdvisorAcct
              isAuthorizedAcct
              isMultiCurrencyAllowed
              isGuidedPortfolioSummEnabled
              isFFOSAcct
              isPrimaryCustomer
              __typename
            }
            acctTrustIndDetail {
              isAdvisorTrustTLAAcct
              isTrustAcct
              __typename
            }
            acctLegalAttrDetail {
              accountTypeCode
              legalConstructCode
              legalConstructModifierCode
              offeringCode
              serviceSegmentCode
              lineOfBusinessCode
              __typename
            }
            acctTradeAttrDetail {
              optionAgrmntCode
              optionLevelCode
              borrowFullyPaidCode
              portfolioMarginCode
              isTradable
              mrgnAgrmntCode
              isSpecificShrTradingEligible
              isSpreadsAllowed
              limitedMrgnCode
              __typename
            }
            annuityPolicyDetail {
              policyStatus
              isImmediateLiquidityEnabled
              regTypeCode
              __typename
            }
            externalAcctDetail {
              acctType
              acctSubType
              isManualAccount
              __typename
            }
            creditCardDetail {
              creditCardAcctNumber
              memberId
              twelveMonthRewards
              webIdPrefix
              __typename
            }
            managedAcctDetail {
              invstApproach
              invstUniverse
              productCode
              svcModelCode
              smaStrategy
              isTaxable
              productFullName
              strategyName
              __typename
            }
            acctFeature {
              featureDetails {
                established {
                  marginOptionSpreadsDetail {
                    hasMargin
                    hasLimitedMargin
                    hasOption
                    hasMarginDebtProtection
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            digiAcctAttrDetail {
              fdasAcctReg
              fdasAcctSubReg
              __typename
            }
            __typename
          }
          groups {
            id
            name
            items {
              acctNum
              acctType
              acctSubType
              acctSubTypeDesc
              acctCreationDate
              parentBrokAcctNum
              linkedAcctDetails {
                acctNum
                isLinked
                __typename
              }
              acctStateDetail {
                statusCode
                __typename
              }
              acctTradeAttrDetail {
                isTradable
                __typename
              }
              acctAttrDetail {
                addlBrokAcctCode
                regTypeDesc
                cryptoAssociatedCode
                taxTreatmentCode
                __typename
              }
              acctIndDetail {
                isAdvisorAcct
                isAuthorizedAcct
                isMultiCurrencyAllowed
                isGuidedPortfolioSummEnabled
                isFFOSAcct
                isPrimaryCustomer
                __typename
              }
              acctTrustIndDetail {
                isAdvisorTrustTLAAcct
                isTrustAcct
                isAdvisorTrustTLAAcct
                __typename
              }
              acctTypesIndDetail {
                isRetailHSA
                isRetirement
                isYouthAcct
                hasSPSPlans
                __typename
              }
              acctRelAttrDetail {
                relCategoryCode
                relRoleTypeCode
                __typename
              }
              acctEligibilityDetail {
                isEligibleForMoneyMovement
                __typename
              }
              acctLegacyAttrDetail {
                legacyHouseHoldCostBasisCode
                __typename
              }
              preferenceDetail {
                name
                isHidden
                isDefaultAcct
                acctGroupId
                __typename
              }
              acctLegalAttrDetail {
                legalConstructCode
                legalConstructModifierCode
                serviceSegmentCode
                accountTypeCode
                offeringCode
                lineOfBusinessCode
                __typename
              }
              workplacePlanDetail {
                planTypeName
                planTypeCode
                planId
                clientId
                clientTickerSymbol
                enrollmentStatusCode
                isCrossoverEnabled
                isEnrollmentEligible
                nonQualifiedInd
                isRollup
                planName
                navigationKey
                url
                vestedAcctValEOD
                isVested100Pct
                __typename
              }
              gainLossBalanceDetail {
                totalMarketVal
                todaysGainLoss
                todaysGainLossPct
                asOfDateTime
                hasUnpricedPositions
                hasIntradayPricing
                __typename
              }
              annuityProductDetail {
                systemOfRecord
                planTypeCode
                planCode
                productCode
                productDesc
                __typename
              }
              annuityPolicyDetail {
                policyStatus
                isImmediateLiquidityEnabled
                __typename
              }
              externalAcctDetail {
                acctType
                acctSubType
                isManualAccount
                __typename
              }
              managedAcctDetail {
                invstApproach
                invstUniverse
                productCode
                svcModelCode
                smaStrategy
                isTaxable
                __typename
              }
              digiAcctAttrDetail {
                fdasAcctReg
                fdasAcctSubReg
                __typename
              }
              __typename
            }
            balanceDetail {
              hasIntradayPricing
              gainLossBalanceDetail {
                totalMarketVal
                todaysGainLoss
                todaysGainLossPct
                fidelityTotalMktVal
                hasUnpricedPositions
                __typename
              }
              __typename
            }
            __typename
          }
          customerAttrDetail {
            externalCustomerID
            isShowWorkplaceSavingAccts
            isShowExternalAccts
            pledgedAcctNums
            __typename
          }
          groupDetails {
            groupId
            groupName
            typeCode
            __typename
          }
          __typename
        }
        __typename
      }
    }
    `,
  };

  const resp = await fetch(
    "https://digital.fidelity.com/ftgw/digital/portfolio/api/graphql?ref_at=portsum",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );
  if (resp.status !== 200) {
    console.log(
      "Not able to get accounts from Fidelity details. Status: ",
      resp.status
    );
    return;
  }

  /* Sample:
{
    "brokerageAcctDetails": [
        {
            "acctNum": "262019136",
            "acctName": "ROTH IRA",
            "acctSubType": "Brokerage",
            "acctSubTypeDesc": "Brokerage Retirement Individual",
            "regTypeCode": "ROTH",
            "regTypeDesc": "ROTH IRA",
            "relTypeCode": "BENE",
            "isAdvisorAcct": false,
            "isHiddenAcct": false,
            "isRetirementAcct": true,
            "isMarginAccount": false,
            "rmdDetail": {
                "isRMDQualified": false,
                "isQCDEligible": false
            },
            "distribDetail": {
                "isEFTAllowed": true,
                "isCheckAllowed": true,
                "isWireAllowed": true,
                "isVenmoAllowed": false,
                "isPaypalAllowed": false,
                "isCreditCardPaymentAllowed": false
            },
            "balanceDetail": {
                "totalAcctVal": 0,
                "totalAcctCashToWithdraw": 0,
                "totalCashWithMargin": 0,
                "asOfDateTime": 1720993261,
                "cashWithoutEquity": 0
            },
            "restrictionDetail": {
                "moneyOutDetail": {
                    "isRestricted": false
                },
                "sharesOutDetail": {
                    "isRestricted": false
                }
            },
            "isYouthAcct": false,
            "acctLegalAttrDetail": {
                "legalConstructCode": "ROTHIRA",
                "accountTypeCode": "RETIREPERSON",
                "lineOfBusinessCode": "PI"
            },
            "isFFOSAcct": false,
            "isTradable": true,
            "acctRelAttrDetail": {
                "relCategoryCode": "PRINC",
                "relRoleTypeCode": "OWNRBENE"
            },
            "isCryptoLinkedAcct": false
        },
        {
            "acctNum": "652228359",
            "acctName": "BrokerageLink Roth",
            "acctSubType": "Brokerage Link",
            "acctSubTypeDesc": "Self-Directed Brokerage",
            "regTypeCode": "NP",
            "regTypeDesc": "Non-Prototype",
            "relTypeCode": "LBEN",
            "isAdvisorAcct": false,
            "isHiddenAcct": false,
            "isRetirementAcct": false,
            "isMarginAccount": false,
            "rmdDetail": {
                "isRMDQualified": false,
                "isQCDEligible": false
            },
            "distribDetail": {
                "isEFTAllowed": false,
                "isCheckAllowed": false,
                "isWireAllowed": false,
                "isVenmoAllowed": false,
                "isPaypalAllowed": false,
                "isCreditCardPaymentAllowed": false
            },
            "balanceDetail": {
                "totalAcctVal": 0,
                "totalAcctCashToWithdraw": 0,
                "totalCashWithMargin": 0,
                "asOfDateTime": 1720993261,
                "cashWithoutEquity": 0
            },
            "restrictionDetail": {
                "moneyOutDetail": {
                    "isRestricted": false
                },
                "sharesOutDetail": {
                    "isRestricted": false
                }
            },
            "brokerageLinkDetail": {
                "planId": "34232",
                "planName": "STRIPE"
            },
            "addlBrokAcctCode": "SDRTH",
            "isYouthAcct": false,
            "acctLegalAttrDetail": {
                "legalConstructCode": "NONPROTOTYPE",
                "accountTypeCode": "RETIREBUS",
                "serviceSegmentCode": "SDBROTH",
                "lineOfBusinessCode": "WI"
            },
            "isFFOSAcct": false,
            "isTradable": true,
            "acctRelAttrDetail": {
                "relCategoryCode": "PRINC",
                "relRoleTypeCode": "ACCOUNTBENE"
            },
            "isCryptoLinkedAcct": false
        },
        {
            "acctNum": "236859610",
            "acctName": "Health Savings Account",
            "acctSubType": "Health Savings",
            "acctSubTypeDesc": "Brokerage Health Savings",
            "regTypeCode": "HSA",
            "regTypeDesc": "Health Savings Account",
            "relTypeCode": "BENE",
            "isAdvisorAcct": false,
            "isHiddenAcct": false,
            "isRetirementAcct": false,
            "isMarginAccount": false,
            "rmdDetail": {
                "isRMDQualified": false,
                "isQCDEligible": false
            },
            "distribDetail": {
                "isEFTAllowed": true,
                "isCheckAllowed": true,
                "isWireAllowed": false,
                "isVenmoAllowed": false,
                "isPaypalAllowed": false,
                "isCreditCardPaymentAllowed": false
            },
            "balanceDetail": {
                "totalAcctVal": 25323.13,
                "totalAcctCashToWithdraw": 229.05,
                "totalCashWithMargin": 229.05,
                "asOfDateTime": 1720993261,
                "cashWithoutEquity": 229.05
            },
            "restrictionDetail": {
                "moneyOutDetail": {
                    "isRestricted": false
                },
                "sharesOutDetail": {
                    "isRestricted": false
                }
            },
            "brokerageLinkDetail": {
                "planId": "HSARG"
            },
            "addlBrokAcctCode": "WITRM",
            "isYouthAcct": false,
            "acctLegalAttrDetail": {
                "legalConstructCode": "INDIVIDUAL",
                "legalConstructModifierCode": "HSA",
                "accountTypeCode": "INVESTPERSON",
                "lineOfBusinessCode": "PI"
            },
            "isFFOSAcct": false,
            "isTradable": true,
            "acctRelAttrDetail": {
                "relCategoryCode": "PRINC",
                "relRoleTypeCode": "OWNRBENE"
            },
            "isCryptoLinkedAcct": false
        },
        {
            "acctNum": "652228358",
            "acctName": "BrokerageLink",
            "acctSubType": "Brokerage Link",
            "acctSubTypeDesc": "Self-Directed Brokerage",
            "regTypeCode": "NP",
            "regTypeDesc": "Non-Prototype",
            "relTypeCode": "LBEN",
            "isAdvisorAcct": false,
            "isHiddenAcct": false,
            "isRetirementAcct": false,
            "isMarginAccount": false,
            "rmdDetail": {
                "isRMDQualified": false,
                "isQCDEligible": false
            },
            "distribDetail": {
                "isEFTAllowed": false,
                "isCheckAllowed": false,
                "isWireAllowed": false,
                "isVenmoAllowed": false,
                "isPaypalAllowed": false,
                "isCreditCardPaymentAllowed": false
            },
            "balanceDetail": {
                "totalAcctVal": 0,
                "totalAcctCashToWithdraw": 0,
                "totalCashWithMargin": 0,
                "asOfDateTime": 1720993261,
                "cashWithoutEquity": 0
            },
            "restrictionDetail": {
                "moneyOutDetail": {
                    "isRestricted": false
                },
                "sharesOutDetail": {
                    "isRestricted": false
                }
            },
            "brokerageLinkDetail": {
                "planId": "34232",
                "planName": "STRIPE"
            },
            "isYouthAcct": false,
            "acctLegalAttrDetail": {
                "legalConstructCode": "NONPROTOTYPE",
                "accountTypeCode": "RETIREBUS",
                "serviceSegmentCode": "SDB",
                "lineOfBusinessCode": "WI"
            },
            "isFFOSAcct": false,
            "isTradable": true,
            "acctRelAttrDetail": {
                "relCategoryCode": "PRINC",
                "relRoleTypeCode": "ACCOUNTBENE"
            },
            "isCryptoLinkedAcct": false
        },
        {
            "acctNum": "Z31446986",
            "acctName": "Individual",
            "acctSubType": "Brokerage",
            "acctSubTypeDesc": "Brokerage General Investing Person",
            "regTypeCode": "I",
            "regTypeDesc": "Individual",
            "relTypeCode": "INDV",
            "isAdvisorAcct": false,
            "isHiddenAcct": false,
            "isRetirementAcct": false,
            "isMarginAccount": true,
            "rmdDetail": {
                "isRMDQualified": false,
                "isQCDEligible": false
            },
            "distribDetail": {
                "isEFTAllowed": true,
                "isCheckAllowed": true,
                "isWireAllowed": true,
                "isVenmoAllowed": true,
                "isPaypalAllowed": true,
                "isCreditCardPaymentAllowed": true
            },
            "balanceDetail": {
                "totalAcctVal": 10664.69,
                "totalAcctCashToWithdraw": 0,
                "totalCashWithMargin": 4723.25,
                "asOfDateTime": 1720993261,
                "cashWithoutEquity": 0
            },
            "restrictionDetail": {
                "moneyOutDetail": {
                    "isRestricted": false
                },
                "sharesOutDetail": {
                    "isRestricted": false
                }
            },
            "isYouthAcct": false,
            "acctLegalAttrDetail": {
                "legalConstructCode": "INDIVIDUAL",
                "accountTypeCode": "INVESTPERSON",
                "lineOfBusinessCode": "PI"
            },
            "isFFOSAcct": false,
            "isTradable": true,
            "acctRelAttrDetail": {
                "relCategoryCode": "PRINC",
                "relRoleTypeCode": "INDIVIDUAL"
            },
            "isCryptoLinkedAcct": false
        }
    ],
}
    */

  const json = await resp.json();

  const accounts = json.data.getContext.person.assets;

  const filteredAccounts = accounts.filter(
    (acct) =>
      acct.acctType == "Brokerage" &&
      acct.acctSubType == "Brokerage" &&
      acct.acctTradeAttrDetail?.isTradable &&
      acct.acctStateDetail?.statusCode === "ACTIV"
  );

  return filteredAccounts;
}

async function getFidelityBalance(acctNum) {
  const resp = await fetch(
    "https://digital.fidelity.com/ftgw/digital/trade-equity/balance",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": window.EQUITY_ENV_MAP.CSURF_TOKEN,
      },
      body: JSON.stringify([
        {
          acctNum: acctNum,
        },
      ]),
    }
  );
  if (resp.status !== 200) {
    console.log("Not able to get balance from Fidelity. Status: ", resp.status);
    return;
  }
  const json = await resp.json();

  return json.balances[0];
}

async function getFidelityPositions(acctNum) {
  const resp = await fetch(
    "https://digital.fidelity.com/ftgw/digital/trade-equity/positions",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": window.EQUITY_ENV_MAP.CSURF_TOKEN,
      },
      body: JSON.stringify({
        acctNum: acctNum,
      }),
    }
  );
  if (resp.status !== 200) {
    console.log("Not able to get balance from Fidelity. Status: ", resp.status);
    return;
  }
  const json = await resp.json();

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

  return json;
}

async function main() {
  // wait for the CSRF token to be set
  while (!window.EQUITY_ENV_MAP) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  const accounts = await getFidelityAccountDetails();
  if (!accounts) {
    console.log("No accounts found");
    return;
  }

  var result = {};

  for (const acct of accounts) {
    const balance = await getFidelityBalance(acct.acctNum);
    const positions = await getFidelityPositions(acct.acctNum);
    result[acct.acctNum] = {
      ...balance,
      acctDetails: acct,
      positions: positions,
    };
    console.log(result[acct.acctNum]);
  }

  // send the result to service worker
  chrome.runtime.sendMessage(
    extensionId,
    {
      type: "fidelity_balance",
      data: result,
    },
    function (response) {
      if (!response.success) console.log(response);
    }
  );
}

window.addEventListener("load", function () {
  main();
});
