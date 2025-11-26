import { Box, Button } from "@mui/material";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import dayjs from "dayjs";
import React from "react";

export interface DateOptionsProps {
  periodInDays?: number | undefined; // expiration period, starting from today
  setPeriodInDays: (periodInDays: number) => void;

  minDate?: dayjs.Dayjs;
  maxDate?: dayjs.Dayjs;
}

export function DateOptions(props: DateOptionsProps) {
  const { periodInDays, setPeriodInDays, minDate, maxDate } = props;

  const today = dayjs().startOf("day");
  const oneMonth = today.add(1, "month");
  const oneYear = today.add(1, "year");

  // if showCustom is true, show custom date picker
  // if showCustom is false, show predefined date badges
  const [showCustom, setShowCustom] = React.useState<boolean>(false);

  const [oneMonthSelected, setOneMonthSelected] =
    React.useState<boolean>(false);
  const [threeMonthsSelected, setThreeMonthsSelected] =
    React.useState<boolean>(false);

  const [datePickerError, setDatePickerError] = React.useState<boolean>(false);

  if (showCustom) {
    return (
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DatePicker
          minDate={minDate ?? oneMonth}
          maxDate={maxDate ?? oneYear}
          sx={{ width: "100%" }}
          value={periodInDays ? today.add(periodInDays, "days") : undefined}
          onChange={(newValue) => {
            setPeriodInDays(dayjs(newValue).diff(today, "days"));
          }}
          slotProps={{
            textField: {
              helperText: datePickerError
                ? "Select a date between 1 month and 1 year"
                : "",
            },
          }}
          onError={(newError) => {
            // when error is resolved, newError is null
            if (newError) {
              setDatePickerError(true);
            } else {
              setDatePickerError(false);
            }
          }}
        />
      </LocalizationProvider>
    );
  }

  return (
    <Box
      display={"flex"}
      flexDirection={"row"}
      gap={1}
      marginTop={1}
      justifyContent={"space-between"}
    >
      <Button
        variant={oneMonthSelected ? "contained" : "outlined"}
        onClick={() => {
          setOneMonthSelected(true);
          setThreeMonthsSelected(false);
          setPeriodInDays(35); // we could use 30 but want to be safe
        }}
      >
        1 month
      </Button>
      <Button
        variant={threeMonthsSelected ? "contained" : "outlined"}
        onClick={() => {
          setOneMonthSelected(false);
          setThreeMonthsSelected(true);
          setPeriodInDays(90);
        }}
      >
        3 months
      </Button>
      <Button
        variant={"outlined"}
        onClick={() => {
          setShowCustom(true);
        }}
      >
        Custom
      </Button>
    </Box>
  );
}
