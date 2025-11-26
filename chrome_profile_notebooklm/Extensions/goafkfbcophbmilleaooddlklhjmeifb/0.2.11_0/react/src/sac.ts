import {
  BrowserClient,
  defaultStackParser,
  getDefaultIntegrations,
  makeFetchTransport,
  Scope,
} from "@sentry/browser";

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

function getKKey() {
  // @ts-ignore
  return document.getElementById("kKey").value;
}

async function cancelOrder(
  kKey: string,
  accountId: string,
  orderId: string,
  expandedOrderId: string
) {
  const params = {
    kKey: kKey,
    OrderDetails: JSON.stringify([
      {
        AccountId: accountId,
        SecurityType: "Option",
        OrderId: orderId,
        OrderType: "Limit",
        ExpandedOrderId: expandedOrderId,
      },
    ]),
    OrderType: "Option",
    caller: "CANCEL ORDER",
    accountId: accountId,
  };

  const queryString = new URLSearchParams(params).toString();

  const resp = await fetch(
    "https://si2.schwabinstitutional.com/SI2/WebTrade/OrderService.mvc/PatchOrder",
    {
      headers: {
        accept: "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        pragma: "no-cache",
        priority: "u=1, i",
        "sec-ch-ua":
          '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
      },
      body: queryString,
      method: "POST",
      mode: "cors",
      credentials: "include",
    }
  );

  /* Sample response
  {
    "SucessOrders": 1,
    "FailureOrders": 0,
    "OrderIDs": "87809017",
    "OrderQty": null,
    "OrderSecurityType": null
  }
  */

  return await resp.json();
}

async function getOrderStatus(kKey: string) {
  const params = {
    AccountType: "",
    kKey: kKey,
    Action: "NotSpecified",
    OrderType: "NotSpecified",
    TimeLimit: "ALL",
    Status: "NotSpecified",
    SecurityTypes: "NotSpecified",
    DateRange: "Today",
    SymbolCusip: "",
    UserId: "",
    ExcludeCanceledOrders: "true",
    ExcludeAllocatedTrades: "false",
    FilterBy: "OrderEntryDate",
    PageSize: "50",
    PageNumber: "1",
    SortColumn: "NotSpecified",
    SortDirection: "Ascending",
    IsDisplaySpecified: "true",
    IsSymbolSpecified: "false",
    StartDate: "",
    EndDate: "",
    GridMode: "Expanded",
    IdsExceptionToCollapsedMode: "",
    SelectAllMode: "NoneSelected",
    SelectAllModeExceptionIds: "",
  };

  const queryString = new URLSearchParams(params).toString();

  const resp = await fetch(
    "https://si2.schwabinstitutional.com/SI2/WebTrade/OrderStatus.mvc/FilterOrderStatus",
    {
      headers: {
        accept: "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        pragma: "no-cache",
        priority: "u=1, i",
        "sec-ch-ua":
          '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
      },
      body: queryString,
      method: "POST",
      mode: "cors",
      credentials: "include",
    }
  );

  /* Sample response
  {
    "isEmptyRow": false,
    "IsTimeStampNotRequired": false,
    "ShowMessage": false,
    "Message": null,
    "Pager": {
        "StartingOrderNumber": 1,
        "EndingOrderNumber": 1,
        "TotalNumberOfOrders": 1,
        "CurrentPage": 1,
        "TotalNumberOfPages": 1,
        "PagerText": "Displaying 1 to 1 of 1",
        "ShowPreviousLink": false,
        "ShowNextLink": false,
        "DisplayPager": false,
        "SelectedOrdersPerPage": 3
    },
    "TimeStamp": "Data as of 02:14 AM ET 08/13/2024",
    "IsTradeOnlyMutualFunds": false,
    "IsTradeAdvancedoptions": true,
    "EnableSelectAllOrPage": true,
    "EnableOrderExpirationColumn": false,
    "EnableAllocationError": true,
    "IsAllocationErrorReturned": false,
    "IsAccountNameSortable": 1,
    "Orders": [
        {
            "IsExecution": false,
            "Id": "551340558400",
            "OrderId": "551340558400",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": "551340558400",
            "ExpansionSymbol": " ",
            "AccountId": "9563-4901",
            "AccountName": "YUCHENG YANG TTEE",
            "Symbol": "SPX 09/20/2024 5000.00 P",
            "Status": "Open",
            "StatusTime": null,
            "Action": "Buy to Open",
            "ActionCode": "Buy to Open",
            "Quantity": "1 cts",
            "ExecutionPrice": null,
            "ExecutedValue": null,
            "OrderType": "Limit($994.05)",
            "TimeLimit": "DAY",
            "SubmitTime": "08-13-2024 02:14:04",
            "SpecialCondition": "None",
            "SecurityName": "PUT S \u0026 P 500 INDEX",
            "SecurityType": "Option",
            "DivReinvestment": "N",
            "TranFee": "",
            "LotInstruction": "Default",
            "SchwabNumber": "551340558400",
            "UserId": "yucheng.yang",
            "AllocationComplete": "N",
            "RegLine1": "LIVING TRUST OF YUCHENG YANG D",
            "RegLine2": "U/A DTD 01/13/2024",
            "HasExecutions": false,
            "IsExpanded": true,
            "PriceType": "Limit",
            "LimitPrice": "994.05",
            "StopPrice": "0",
            "LeavesQuantity": "1",
            "IsClosedOrder": false,
            "OptionMultiplier": 100,
            "TriggerPrice": null,
            "TrailingAmt": "",
            "ContingentId": "",
            "ExpandedOrderID": "551340558400",
            "ShortOrderID": "87812072",
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": "651340558400",
            "OrderId": "651340558400",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": "551340558400",
            "ExpansionSymbol": " ",
            "AccountId": "9563-4901",
            "AccountName": "YUCHENG YANG TTEE",
            "Symbol": "SPX 09/20/2024 5000.00 C",
            "Status": "Open",
            "StatusTime": null,
            "Action": "Sell to Open",
            "ActionCode": "Sell to Open",
            "Quantity": "1 cts",
            "ExecutionPrice": null,
            "ExecutedValue": null,
            "OrderType": "Limit($994.05)",
            "TimeLimit": "DAY",
            "SubmitTime": "08-13-2024 02:14:04",
            "SpecialCondition": "None",
            "SecurityName": "CALL S \u0026 P 500 INDEX",
            "SecurityType": "Option",
            "DivReinvestment": "N",
            "TranFee": "",
            "LotInstruction": "Default",
            "SchwabNumber": "651340558400",
            "UserId": "yucheng.yang",
            "AllocationComplete": "N",
            "RegLine1": "LIVING TRUST OF YUCHENG YANG D",
            "RegLine2": "U/A DTD 01/13/2024",
            "HasExecutions": false,
            "IsExpanded": true,
            "PriceType": "Limit",
            "LimitPrice": "994.05",
            "StopPrice": "0",
            "LeavesQuantity": "1",
            "IsClosedOrder": false,
            "OptionMultiplier": 100,
            "TriggerPrice": null,
            "TrailingAmt": "",
            "ContingentId": "",
            "ExpandedOrderID": "651340558400",
            "ShortOrderID": "87812073",
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": "751340558400",
            "OrderId": "751340558400",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": "551340558400",
            "ExpansionSymbol": " ",
            "AccountId": "9563-4901",
            "AccountName": "YUCHENG YANG TTEE",
            "Symbol": "SPX 09/20/2024 6000.00 P",
            "Status": "Open",
            "StatusTime": null,
            "Action": "Sell to Open",
            "ActionCode": "Sell to Open",
            "Quantity": "1 cts",
            "ExecutionPrice": null,
            "ExecutedValue": null,
            "OrderType": "Limit($994.05)",
            "TimeLimit": "DAY",
            "SubmitTime": "08-13-2024 02:14:04",
            "SpecialCondition": "None",
            "SecurityName": "PUT S \u0026 P 500 INDEX",
            "SecurityType": "Option",
            "DivReinvestment": "N",
            "TranFee": "",
            "LotInstruction": "Default",
            "SchwabNumber": "751340558400",
            "UserId": "yucheng.yang",
            "AllocationComplete": "N",
            "RegLine1": "LIVING TRUST OF YUCHENG YANG D",
            "RegLine2": "U/A DTD 01/13/2024",
            "HasExecutions": false,
            "IsExpanded": true,
            "PriceType": "Limit",
            "LimitPrice": "994.05",
            "StopPrice": "0",
            "LeavesQuantity": "1",
            "IsClosedOrder": false,
            "OptionMultiplier": 100,
            "TriggerPrice": null,
            "TrailingAmt": "",
            "ContingentId": "",
            "ExpandedOrderID": "751340558400",
            "ShortOrderID": "87812074",
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": "851340558400",
            "OrderId": "851340558400",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": "551340558400",
            "ExpansionSymbol": " ",
            "AccountId": "9563-4901",
            "AccountName": "YUCHENG YANG TTEE",
            "Symbol": "SPX 09/20/2024 6000.00 C",
            "Status": "Open",
            "StatusTime": null,
            "Action": "Buy to Open",
            "ActionCode": "Buy to Open",
            "Quantity": "1 cts",
            "ExecutionPrice": null,
            "ExecutedValue": null,
            "OrderType": "Limit($994.05)",
            "TimeLimit": "DAY",
            "SubmitTime": "08-13-2024 02:14:04",
            "SpecialCondition": "None",
            "SecurityName": "CALL S \u0026 P 500 INDEX",
            "SecurityType": "Option",
            "DivReinvestment": "N",
            "TranFee": "",
            "LotInstruction": "Default",
            "SchwabNumber": "851340558400",
            "UserId": "yucheng.yang",
            "AllocationComplete": "N",
            "RegLine1": "LIVING TRUST OF YUCHENG YANG D",
            "RegLine2": "U/A DTD 01/13/2024",
            "HasExecutions": false,
            "IsExpanded": true,
            "PriceType": "Limit",
            "LimitPrice": "994.05",
            "StopPrice": "0",
            "LeavesQuantity": "1",
            "IsClosedOrder": false,
            "OptionMultiplier": 100,
            "TriggerPrice": null,
            "TrailingAmt": "",
            "ContingentId": "",
            "ExpandedOrderID": "851340558400",
            "ShortOrderID": "87812075",
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": null,
            "OrderId": "",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": null,
            "ExpansionSymbol": null,
            "AccountId": "",
            "AccountName": "",
            "Symbol": "",
            "Status": "",
            "StatusTime": "",
            "Action": "",
            "ActionCode": null,
            "Quantity": "",
            "ExecutionPrice": "",
            "ExecutedValue": "",
            "OrderType": "",
            "TimeLimit": "",
            "SubmitTime": "",
            "SpecialCondition": "",
            "SecurityName": "",
            "SecurityType": "",
            "DivReinvestment": "",
            "TranFee": "",
            "LotInstruction": "",
            "SchwabNumber": "",
            "UserId": "",
            "AllocationComplete": "",
            "RegLine1": null,
            "RegLine2": null,
            "HasExecutions": false,
            "IsExpanded": false,
            "PriceType": null,
            "LimitPrice": null,
            "StopPrice": null,
            "LeavesQuantity": null,
            "IsClosedOrder": false,
            "OptionMultiplier": 0,
            "TriggerPrice": "",
            "TrailingAmt": null,
            "ContingentId": null,
            "ExpandedOrderID": null,
            "ShortOrderID": null,
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": null,
            "OrderId": "",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": null,
            "ExpansionSymbol": null,
            "AccountId": "",
            "AccountName": "",
            "Symbol": "",
            "Status": "",
            "StatusTime": "",
            "Action": "",
            "ActionCode": null,
            "Quantity": "",
            "ExecutionPrice": "",
            "ExecutedValue": "",
            "OrderType": "",
            "TimeLimit": "",
            "SubmitTime": "",
            "SpecialCondition": "",
            "SecurityName": "",
            "SecurityType": "",
            "DivReinvestment": "",
            "TranFee": "",
            "LotInstruction": "",
            "SchwabNumber": "",
            "UserId": "",
            "AllocationComplete": "",
            "RegLine1": null,
            "RegLine2": null,
            "HasExecutions": false,
            "IsExpanded": false,
            "PriceType": null,
            "LimitPrice": null,
            "StopPrice": null,
            "LeavesQuantity": null,
            "IsClosedOrder": false,
            "OptionMultiplier": 0,
            "TriggerPrice": "",
            "TrailingAmt": null,
            "ContingentId": null,
            "ExpandedOrderID": null,
            "ShortOrderID": null,
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": null,
            "OrderId": "",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": null,
            "ExpansionSymbol": null,
            "AccountId": "",
            "AccountName": "",
            "Symbol": "",
            "Status": "",
            "StatusTime": "",
            "Action": "",
            "ActionCode": null,
            "Quantity": "",
            "ExecutionPrice": "",
            "ExecutedValue": "",
            "OrderType": "",
            "TimeLimit": "",
            "SubmitTime": "",
            "SpecialCondition": "",
            "SecurityName": "",
            "SecurityType": "",
            "DivReinvestment": "",
            "TranFee": "",
            "LotInstruction": "",
            "SchwabNumber": "",
            "UserId": "",
            "AllocationComplete": "",
            "RegLine1": null,
            "RegLine2": null,
            "HasExecutions": false,
            "IsExpanded": false,
            "PriceType": null,
            "LimitPrice": null,
            "StopPrice": null,
            "LeavesQuantity": null,
            "IsClosedOrder": false,
            "OptionMultiplier": 0,
            "TriggerPrice": "",
            "TrailingAmt": null,
            "ContingentId": null,
            "ExpandedOrderID": null,
            "ShortOrderID": null,
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": null,
            "OrderId": "",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": null,
            "ExpansionSymbol": null,
            "AccountId": "",
            "AccountName": "",
            "Symbol": "",
            "Status": "",
            "StatusTime": "",
            "Action": "",
            "ActionCode": null,
            "Quantity": "",
            "ExecutionPrice": "",
            "ExecutedValue": "",
            "OrderType": "",
            "TimeLimit": "",
            "SubmitTime": "",
            "SpecialCondition": "",
            "SecurityName": "",
            "SecurityType": "",
            "DivReinvestment": "",
            "TranFee": "",
            "LotInstruction": "",
            "SchwabNumber": "",
            "UserId": "",
            "AllocationComplete": "",
            "RegLine1": null,
            "RegLine2": null,
            "HasExecutions": false,
            "IsExpanded": false,
            "PriceType": null,
            "LimitPrice": null,
            "StopPrice": null,
            "LeavesQuantity": null,
            "IsClosedOrder": false,
            "OptionMultiplier": 0,
            "TriggerPrice": "",
            "TrailingAmt": null,
            "ContingentId": null,
            "ExpandedOrderID": null,
            "ShortOrderID": null,
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": null,
            "OrderId": "",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": null,
            "ExpansionSymbol": null,
            "AccountId": "",
            "AccountName": "",
            "Symbol": "",
            "Status": "",
            "StatusTime": "",
            "Action": "",
            "ActionCode": null,
            "Quantity": "",
            "ExecutionPrice": "",
            "ExecutedValue": "",
            "OrderType": "",
            "TimeLimit": "",
            "SubmitTime": "",
            "SpecialCondition": "",
            "SecurityName": "",
            "SecurityType": "",
            "DivReinvestment": "",
            "TranFee": "",
            "LotInstruction": "",
            "SchwabNumber": "",
            "UserId": "",
            "AllocationComplete": "",
            "RegLine1": null,
            "RegLine2": null,
            "HasExecutions": false,
            "IsExpanded": false,
            "PriceType": null,
            "LimitPrice": null,
            "StopPrice": null,
            "LeavesQuantity": null,
            "IsClosedOrder": false,
            "OptionMultiplier": 0,
            "TriggerPrice": "",
            "TrailingAmt": null,
            "ContingentId": null,
            "ExpandedOrderID": null,
            "ShortOrderID": null,
            "SettlementDate": null,
            "OrderExpiration": null
        },
        {
            "IsExecution": false,
            "Id": null,
            "OrderId": "",
            "ExecutionId": null,
            "CheckedState": false,
            "LinkId": null,
            "ExpansionSymbol": null,
            "AccountId": "",
            "AccountName": "",
            "Symbol": "",
            "Status": "",
            "StatusTime": "",
            "Action": "",
            "ActionCode": null,
            "Quantity": "",
            "ExecutionPrice": "",
            "ExecutedValue": "",
            "OrderType": "",
            "TimeLimit": "",
            "SubmitTime": "",
            "SpecialCondition": "",
            "SecurityName": "",
            "SecurityType": "",
            "DivReinvestment": "",
            "TranFee": "",
            "LotInstruction": "",
            "SchwabNumber": "",
            "UserId": "",
            "AllocationComplete": "",
            "RegLine1": null,
            "RegLine2": null,
            "HasExecutions": false,
            "IsExpanded": false,
            "PriceType": null,
            "LimitPrice": null,
            "StopPrice": null,
            "LeavesQuantity": null,
            "IsClosedOrder": false,
            "OptionMultiplier": 0,
            "TriggerPrice": "",
            "TrailingAmt": null,
            "ContingentId": null,
            "ExpandedOrderID": null,
            "ShortOrderID": null,
            "SettlementDate": null,
            "OrderExpiration": null
        }
    ]
}
  */

  return await resp.json();
}

async function placeOrder(
  kKey: string,
  accountId: string,
  expDate: string, // MM/DD/YYYY
  strike1: number, // strike 1 < strike 2
  strike2: number,
  limitPrice: number, // assume is CL
  quantity: number
) {
  const formData = new URLSearchParams();

  const priceDirection = "CL"; // CL = credit. change to DL for debit

  const operation = "Submit";

  const overrides = [
    {
      ReferenceCode: "DO459",
      MessageTypeCode: "Informational",
      ModuleShortName: "DO0459",
      MessageNumber: 459,
      Code: "DO",
    },
    {
      ReferenceCode: "DO3016",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName: "DO3016",
      MessageNumber: 3016,
      Code: "DO",
    },
    {
      ReferenceCode: "AC4404",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName:
        " PM Principal and Quantity check.IssuePMEdit.IssuePM4404 (25:Info)",
      MessageNumber: 4404,
      Code: "AC",
    },
    {
      ReferenceCode: "AC4406",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName:
        " PM Principal and Quantity check.IssuePMEdit.IssuePM4406 (90:Info)",
      MessageNumber: 4406,
      Code: "AC",
    },
    {
      ReferenceCode: "AC4411",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName:
        " PM Principal and Quantity check.IssuePMEdit.IssuePM4411 (35:Info)",
      MessageNumber: 4411,
      Code: "AC",
    },
    {
      ReferenceCode: "AC4412",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName:
        " PM Principal and Quantity check.IssuePMEdit.IssuePM4412 (45:Info)",
      MessageNumber: 4412,
      Code: "AC",
    },
    {
      ReferenceCode: "AC143",
      MessageTypeCode: "Informational",
      ModuleShortName:
        " PM Option General Position Checks.IssuePMEdit.IssuePM0143 (30:Info)",
      MessageNumber: 143,
      Code: "AC",
    },
    {
      ReferenceCode: "AC142",
      MessageTypeCode: "Informational",
      ModuleShortName:
        " PM Option General Position Checks.IssuePMEdit.IssuePM0142 (20:Info)",
      MessageNumber: 142,
      Code: "AC",
    },
    {
      ReferenceCode: "AC1200",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName:
        "Master Account Balance Check.IssueEquityEdit.IssueAC1200 (35:Info)",
      MessageNumber: 1200,
      Code: "AC",
    },
    {
      ReferenceCode: "AC1125",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName:
        "Master SellPosition Checks Options.IssueEquityEdit.IssueAC1125 (45:Info)",
      MessageNumber: 1125,
      Code: "AC",
    },
    {
      ReferenceCode: "AC1143",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName:
        "Master Account General Position Options-Options.IssueEquityEdit.IssueAC1143 (75:Info)",
      MessageNumber: 1143,
      Code: "AC",
    },
    {
      ReferenceCode: "AC1142",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName:
        "Master Account General Position Options-Options.IssueEquityEdit.IssueAC1142 (85:Info)",
      MessageNumber: 1142,
      Code: "AC",
    },
    {
      ReferenceCode: "OE254",
      MessageTypeCode: "Informational",
      ModuleShortName:
        "Master Dup Checks.IssueEquityEdit.IssueAC0254 (60:Info)",
      MessageNumber: 254,
      Code: "OE",
    },
    {
      ReferenceCode: "DO3139",
      MessageTypeCode: "BusinessWarning",
      ModuleShortName: "DO3139",
      MessageNumber: 3139,
      Code: "DO",
    },
    {
      ReferenceCode: "DO0722",
      MessageTypeCode: "Informational",
      ModuleShortName: "DO0722",
      MessageNumber: 722,
      Code: "DO",
    },
    {
      ReferenceCode: "DO0723",
      MessageTypeCode: "Informational",
      ModuleShortName: "DO0723",
      MessageNumber: 723,
      Code: "DO",
    },
    {
      ReferenceCode: "DO405",
      MessageTypeCode: "Informational",
      ModuleShortName: "DO405",
      MessageNumber: 405,
      Code: "DO",
    },
  ];

  formData.append("kKey", kKey);
  formData.append(
    "OrderDetails",
    JSON.stringify([
      {
        TrNo: 1,
        Action: "Buy To Open",
        AccountID: accountId,
        Quantity: quantity,
        SecuritySymbol: `SPX ${expDate} ${strike2.toFixed(2)} C`,
        Symbol: `SPX ${expDate} ${strike2.toFixed(2)} C`,
        Price: priceDirection,
        TimeLimit: "Day",
        PriceTime: "",
        Discretionary: "No",
        ProcRtnCode: 0,
        RowId: 1,
        MultiLegType: "Spread",
        GroupingSymbol: "D001",
        OptionLeg: "Leg1",
        CustomerOwnAffirmCode: "NotSpecified",
        SecurityType: "Option",
        LinkID: "O1",
        OrderType: priceDirection,
        SuppresssEdit: false,
        OrderId: 0,
        OrderTankId: 0,
        LimitPrice: limitPrice.toFixed(2),
        SpecialConditions: "-",
        doOperationOf: operation,
        AccountId: accountId,
        Timing: "Day",
        AsEditOverrides: overrides,
        AsOrderId: "",
        AsOrderNumber: "",
        ExpandedOrderId: "",
      },
      {
        TrNo: 2,
        Action: "Sell To Open",
        AccountID: accountId,
        Quantity: quantity,
        SecuritySymbol: `SPX ${expDate} ${strike1.toFixed(2)} C`,
        Symbol: `SPX ${expDate} ${strike1.toFixed(2)} C`,
        Price: priceDirection,
        TimeLimit: "Day",
        PriceTime: "",
        Discretionary: "No",
        ProcRtnCode: 0,
        RowId: 2,
        MultiLegType: "Spread",
        GroupingSymbol: "D001",
        CustomerOwnAffirmCode: "NotSpecified",
        SecurityType: "Option",
        LinkID: "O1",
        OptionLeg: "Leg2",
        OrderType: priceDirection,
        SuppresssEdit: false,
        OrderId: 0,
        OrderTankId: 0,
        LimitPrice: limitPrice.toFixed(2),
        SpecialConditions: "-",
        doOperationOf: operation,
        AccountId: accountId,
        Timing: "Day",

        AsEditOverrides: overrides,
        AsOrderId: "",
        AsOrderNumber: "",
        ExpandedOrderId: "",
      },
      {
        TrNo: 3,
        Action: "Buy To Open",
        AccountID: accountId,
        Quantity: quantity,
        SecuritySymbol: `SPX ${expDate} ${strike1.toFixed(2)} P`,
        Symbol: `SPX ${expDate} ${strike1.toFixed(2)} P`,
        Price: priceDirection,
        TimeLimit: "Day",
        PriceTime: "",
        Discretionary: "No",
        ProcRtnCode: 0,
        RowId: 3,
        MultiLegType: "Spread",
        GroupingSymbol: "D001",
        OptionLeg: "Leg3",
        CustomerOwnAffirmCode: "NotSpecified",
        SecurityType: "Option",
        LinkID: "O1",
        OrderType: priceDirection,
        SuppresssEdit: false,
        OrderId: 0,
        OrderTankId: 0,
        LimitPrice: limitPrice.toFixed(2),
        SpecialConditions: "-",
        doOperationOf: operation,
        AccountId: accountId,
        Timing: "Day",
        AsEditOverrides: overrides,
        AsOrderId: "",
        AsOrderNumber: "",
        ExpandedOrderId: "",
      },
      {
        TrNo: 4,
        Action: "Sell To Open",
        AccountID: accountId,
        Quantity: quantity,
        SecuritySymbol: `SPX ${expDate} ${strike2.toFixed(2)} P`,
        Symbol: `SPX ${expDate} ${strike2.toFixed(2)} P`,
        Price: priceDirection,
        TimeLimit: "Day",
        PriceTime: "",
        Discretionary: "No",
        ProcRtnCode: 0,
        RowId: 3,
        MultiLegType: "Spread",
        GroupingSymbol: "D001",
        OptionLeg: "Leg4",
        CustomerOwnAffirmCode: "NotSpecified",
        SecurityType: "Option",
        LinkID: "O1",
        OrderType: priceDirection,
        SuppresssEdit: false,
        OrderId: 0,
        OrderTankId: 0,
        LimitPrice: limitPrice.toFixed(2),
        SpecialConditions: "-",
        doOperationOf: operation,
        AccountId: accountId,
        Timing: "Day",
        AsEditOverrides: overrides,
        AsOrderId: "",
        AsOrderNumber: "",
        ExpandedOrderId: "",
      },
    ])
  );
  formData.append("OrderType", "Option");
  formData.append("caller", "NEW MULTILEG ORDER");

  const resp = await fetch(
    "https://si2.schwabinstitutional.com/SI2/WebTrade/OrderService.mvc/ProcessMultiLegOrder",
    {
      headers: {
        accept: "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        pragma: "no-cache",
        priority: "u=1, i",
        "sec-ch-ua":
          '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
      },
      body: formData.toString(),
      method: "POST",
      mode: "cors",
      credentials: "include",
    }
  );

  return await resp.json();
}

async function sacTrade(
  account: string,
  expDate: string,
  strike1: number,
  strike2: number,
  limitPrice: number,
  quantity: number
) {
  const kkey = getKKey();

  placeOrder(kkey, account, expDate, strike1, strike2, limitPrice, quantity);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  const asyncListener = async function (
    request: any,
    sender: any,
    sendResponse: any
  ) {
    try {
      /*
  {
      platform: "sac",
      action: "trade",
      data: {
        accountId: string,
        expDate: string,
        strike1: number,
        strike2: number,
        limitPrice: number,
        quantity: number,
      }
  }
  */
      if (request.platform === "sac" && request.action === "trade") {
        const { accountId, expDate, strike1, strike2, limitPrice, quantity } =
          request.data;

        const resp = await sacTrade(
          accountId,
          expDate,
          strike1,
          strike2,
          limitPrice,
          quantity
        );

        sendResponse({ result: "ok", data: resp });
      }

      /*
  {
      platform: "sac",
      action: "refresh_order_status",
  }
  */
      if (
        request.platform === "sac" &&
        request.action === "refresh_order_status"
      ) {
        sendResponse({ result: "ok" });
        const kKey = getKKey();

        const orderStatus = await getOrderStatus(kKey);

        // put it in local storage
        await chrome.storage.local.set({ sac_order_status: orderStatus });

        console.log("Order status saved to local storage");
        console.log(orderStatus);
      }

      /*
    {
        platform: "sac",
        action: "cancel_order",
        data: {
            accountId: string,
            orderId: string,
            expandedOrderId: string,
        }
    }
  */
      if (request.platform === "sac" && request.action === "cancel_order") {
        const kKey = getKKey();

        const { accountId, orderId, expandedOrderId } = request.data;

        const resp = await cancelOrder(
          kKey,
          accountId,
          orderId,
          expandedOrderId
        );

        sendResponse({ result: "ok", resp: resp });
      }
    } catch (error) {
      scope.captureException(error);
    }
  };

  asyncListener(request, sender, sendResponse);

  return true;
});
