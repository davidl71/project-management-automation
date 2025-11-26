import { Typography } from "@mui/material";
import { Box } from "@mui/system";

export function ExecuteTradePlaceholder() {
  return (
    <Box
      display={"flex"}
      justifyContent={"center"}
      alignContent={"center"}
      marginTop={2}
      marginLeft={1}
      marginRight={1}
      width={"100%"}
    >
      <Typography variant={"h6"} fontSize={"1.2rem"}>
        Click the "Place Order" button to continue
      </Typography>
    </Box>
  );
}
