export function getStrikePriceTargets(boxSizeTarget: number) {
  const strikePrice1 = 5000;

  const quantity = Math.ceil(boxSizeTarget / 200000);

  const strikePrice2Target = 5000 + (boxSizeTarget * 1.0) / quantity / 100;

  return {
    strikePrice1,
    strikePrice2Target,
    quantity,
  };
}
