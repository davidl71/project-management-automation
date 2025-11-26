export async function saveTrade(
  platform: string,
  data: any,
  token: string,
  userId: string
) {
  const resp = await fetch("https://app.syntheticfi.com/api/chrome/trade", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      id: userId,
      platform: platform,
      data: data,
    }),
  });

  if (resp.ok) {
    console.log("Trade data saved successfully to SyntheticFi");
  } else {
    console.error(`Failed to save ${platform} balance`);
    throw new Error("Failed to save trade data");
  }
}
