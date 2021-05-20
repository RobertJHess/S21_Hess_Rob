library(tidyverse)
library(timetk)
library(dygraphs)
library(lubridate)
library(RColorBrewer)

candles <- read_csv("D:\\Spring 2021\\Senior Project\\S21_Hess_Rob\\big_data\\candle_data.csv")

# candles <- candles %>% mutate(date = mdy_hm(.$date))

candles_filtered <- candles %>% 
  filter(fractal == 30 & interspace == "MINUTE" & spreadoffer == "Ask") %>% 
  select(date,open,high,low,close)

candles_ts <- tk_xts(candles_filtered,
       order.by= as.POSIXct(mdy_hm(candles_filtered$date)))

m <- tail(candles_ts, n = 32)
dygraph(candles_ts) %>%
  dyCandlestick() %>% 
  dyUnzoom()





m <- tail(candles_filtered, n = 32)

candles_with_atr_30_min <- candles_filtered %>%
  arrange(date) %>%
  mutate(row_num = row_number()) %>%
  rowwise() %>% 
  mutate(atr = atr_calc(candles_filtered[(abs(row_num-14)):abs(row_num-1),3], candles_filtered[abs(row_num-14):abs(row_num-1),4]))

View(candles_with_atr_30_min)

test <- atr_calc(m[1,],m, 14)

32 %/% 14

atr_calc <- function(high.df, low.df){
  return(sum(high.df - low.df) / nrow(high.df))
}

atr_calc(m[(1-14):(1-1),3], m[(1-14):(1-1),4])
