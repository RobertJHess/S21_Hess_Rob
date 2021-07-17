library(tidyverse)
library(timetk)
library(dygraphs)
library(lubridate)

candles <- read_csv("D:\\Spring 2021\\Senior Project\\S21_Hess_Rob\\big_data\\candle_data.csv")

# candles <- candles %>% mutate(date = mdy_hm(.$date))

candles_filtered <- candles %>% 
  filter(fractal == 3 & interspace == "HOUR" & spreadoffer == "Ask") %>% 
  mutate(date = mdy_hm(date)) %>% 
  select(date,open,high,low,close)

candles_ts <- tk_xts(candles_filtered,
       order.by= as.POSIXct(candles_filtered$date))

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



atr_calc <- function(high.df, low.df){
  return(sum(high.df - low.df) / nrow(high.df))
}

contains_text <- function(df){
  return (nrow(filter(df, !is.na(text))) > 0)
}


raw_text_data <- read_csv("D:\\Spring 2021\\Senior Project\\S21_Hess_Rob\\data\\derived\\raw_text_with_datetime_manual.csv")

raw_text_data <- raw_text_data %>% mutate(date_time = mdy_hms(str_c(date, " ", time)))

raw_text_data <- raw_text_data %>% mutate(candle_date_time = floor_date(date_time, "30 minutes"))

text_candle_data <- candles_with_atr_30_min %>% left_join(raw_text_data, by = c('date'='candle_date_time'))

text_atr_candle <- text_candle_data %>% 
arrange(row_num) %>%
  rowwise() %>%
  mutate(atr_news_candle = contains_text(text_candle_data[abs(row_num-6):abs(row_num+84),]))

num <- 100
contains_text(text_candle_data[abs(num):abs(num+1000),])

text_atr_candle %>%
  filter(atr_news_candle) %>%
  write.csv("D:\\Spring 2021\\Senior Project\\S21_Hess_Rob\\data\\derived\\raw_text_atr_candles_2.csv")


applicable_candles_text <- text_atr_candle %>%
  filter(atr_news_candle)


applicable_candles_text %>%
  mutate(range = high - low) %>%
  mutate(is_above_average_range = (range - atr) > 0) %>%
  filter(!is.na(text)) %>% 
  group_by(is_above_average_range) %>% 
  summarise(count = n())



grouped_applicable_candles <- applicable_candles_text %>%
  mutate(range = high - low) %>%
  mutate(is_above_average_range = (range - atr) > 0) %>%
  add_column(sort(rep(seq(1,115),91))) %>%
  rename(group = "sort(rep(seq(1, 115), 91))")

ranked_candles <- grouped_applicable_candles %>%
  arrange(group, range) %>% group_by(group) %>% 
  mutate(rank = row_number())

graph_data <- ranked_candles %>% filter(!is.na(text)) %>% ungroup()

  
  ggplot(graph_data) +
  geom_histogram(aes(x = rank), binwidth = 1) +
  geom_vline(aes(xintercept = 15 / 2, col = "expected")) +
  theme_bw() +
  labs(title = "Distribution of Relative Range-Rank") +
  geom_vline(aes(xintercept = mean(rank), col = "mean"), show.legend = T) +
  geom_vline(aes(xintercept = median(rank), col = "median"), show.legend = T) +
  scale_colour_manual(name = '', values =c('median'='blue','mean'='red', 'expected'='black'), guide = "legend")

ranked_candles %>% filter(!is.na(text)) %>% ungroup() %>% 
summarise(median(rank))







three_hour_news_custom_built <- applicable_candles_text %>%
  ungroup() %>%
  arrange(date) %>%
  mutate(row_num = row_number()) %>%
  filter(row_num %% 91  != 0) %>%
  add_column(sort(rep(seq(1,1725),6))) %>%
  rename(three_hour_candle_group = "sort(rep(seq(1, 1725), 6))") %>% 
  group_by(three_hour_candle_group) %>%
  summarise(date = first(date), high = max(high), low = min(low),open =  first(open), close = last(close), text = first(text))

three_hour_atr <- three_hour_news_custom_built %>% ungroup() %>% 
  arrange(date) %>% 
  mutate(row_num = row_number()) %>% 
  rowwise() %>% 
mutate(atr = atr_calc(three_hour_news_custom_built[(abs(row_num-14)):abs(row_num-1),3], three_hour_news_custom_built[abs(row_num-14):abs(row_num-1),4]))


grouped_applicable_candles <- three_hour_atr %>% 
mutate(range = high - low) %>%
  mutate(is_above_average_range = (range - atr) > 0) %>%
  add_column(sort(rep(seq(1,115),15))) %>%
  rename(group = "sort(rep(seq(1, 115), 15))")


three_hour_atr %>%
  mutate(range = high - low) %>%
  mutate(is_above_average_range = (range - atr) > 0) %>%
  filter(!is.na(text)) %>% 
  group_by(is_above_average_range) %>% 
  summarise(count = n())

ranked_candles <- grouped_applicable_candles %>%
  arrange(group, range) %>% group_by(group) %>% 
  mutate(rank = row_number())

graph_data <- ranked_candles %>% filter(!is.na(text)) %>% ungroup()


ggplot(graph_data) +
  geom_histogram(aes(x = rank), binwidth = 1) +
  geom_vline(aes(xintercept = 15 / 2, col = "expected")) +
  theme_bw() +
  labs(title = "Distribution of Relative Range-Rank") +
  geom_vline(aes(xintercept = mean(rank), col = "mean"), show.legend = T) +
  geom_vline(aes(xintercept = median(rank), col = "median"), show.legend = T) +
  scale_colour_manual(name = '', values =c('median'='blue','mean'='red', 'expected'='black'), guide = "legend")


